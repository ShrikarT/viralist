"""Explicit single-person repair after a terminal server error; never auto-retry.

Keep original failed requests, cleanup and full worst-case charge reservation.
"""
import argparse
import copy
from pathlib import Path
import subprocess

from meta_pipeline import PipelineClient, read, simulate, make_notes
from meta_smoke import write_json, digest


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    out = args.out
    if (out/'repair.json').exists():
        raise SystemExit('Explicit repair already attempted; inspect before further action')
    report = read(out/'report.json')
    ledger = read(out/'ledger.json')
    cleanup = read(out/'cleanup.json')
    assert not report['failures'] and abs(ledger['active_reserve']) < 1e-6
    assert all(x.get('retrieval_status') == 404 for x in cleanup)
    snapshot = out/'pre-repair-ledger.json'
    write_json(snapshot, ledger)
    write_json(out/'pre-repair-report.json', report)
    write_json(out/'pre-repair-cleanup.json', cleanup)
    media = read(out/'provider-media.json')
    client = PipelineClient(out, snapshot)
    client.ledger = ledger['calls']
    client.counter = max(c['number'] for c in client.ledger)
    client.save()
    repair = {'source_sha': subprocess.check_output(['git','rev-parse','HEAD']).decode().strip(),
              'previous_report_sha256': digest((out/'pre-repair-report.json').read_bytes()), 'people': [], 'failures': []}
    write_json(out/'repair.json', repair)
    try:
        for name, video in report['videos'].items():
            n = video['simulation']['requested_personas']
            failed = video['simulation']['failures']
            if not failed:
                continue
            prefix = f'{name}-{n}'
            original = read(out/f'{prefix}-reactions.json')
            audits = read(out/f'{prefix}-dispatch-audit.json')
            write_json(out/f'{prefix}-pre-repair-reactions.json', original)
            write_json(out/f'{prefix}-pre-repair-audit.json', audits)
            repaired_ids = set()
            replacements, new_audits = [], []
            for failure in failed:
                # Target only a persona whose request got a terminal server error.
                assert 'HTTP 500' in failure['error'] and failure['scene'] == 0
                pid = failure['persona_id']
                item = copy.deepcopy(media[name])
                for scene in item['scenes']:
                    scene['file_id'] = client.upload(Path(scene['path']), f'{name}-repair-s{scene["index"]}-upload')
                repair_prefix = prefix + '-repair-' + pid
                summary, records = simulate(client, item, name, n, workers=1,
                                            indices=[int(pid[1:])-1], prefix=repair_prefix)
                if summary['failed_personas']:
                    raise RuntimeError('Single repair failed; do not retry automatically')
                replacements.extend(records)
                new_audits.extend(read(out/f'{repair_prefix}-dispatch-audit.json'))
                repaired_ids.add(pid)
                repair['people'].append({'video': name, 'persona_id': pid, 'wall_sec': summary['wall_sec']})
            merged = [r for r in original if r['persona_id'] not in repaired_ids] + replacements
            merged.sort(key=lambda r: (r['persona_id'], r['scene']))
            combined = [a for a in audits if a['persona_id'] not in repaired_ids] + new_audits
            write_json(out/f'{prefix}-reactions.json', merged)
            write_json(out/f'{prefix}-dispatch-audit.json', combined)
            summary = video['simulation']
            summary['initial_failed_attempts'] = failed
            summary['failures'] = []
            summary['failed_personas'] = 0
            summary['valid_verdicts'] = len(merged)
            summary['initial_attempt_wall_sec'] = summary['wall_sec']
            summary['repair_wall_sec'] = sum(x['wall_sec'] for x in repair['people'] if x['video'] == name)
            summary['wall_sec'] = round(summary['initial_attempt_wall_sec'] + summary['repair_wall_sec'], 3)
            summary['reached_final_segment'] = len({r['persona_id'] for r in merged if r['scene'] == media[name]['scenes'][-1]['index']})
            summary['still_watching_after_final_segment'] = sum(r['scene'] == media[name]['scenes'][-1]['index'] and r['still_watching'] for r in merged)
            write_json(out/f'{prefix}-summary.json', summary)
            video['notes'] = make_notes(client, name, n, video['analysis'], merged)
    except Exception as exc:
        repair['failures'].append(client.safe(exc))
    finally:
        client.cleanup()
        cleanup.extend(read(out/'cleanup.json'))
        write_json(out/'cleanup.json', cleanup)
        write_json(out/'provider-files.json', [x['file_id'] for x in cleanup])
        report['repair_source_sha'] = repair['source_sha']
        report['cumulative_estimated_usd'] = round(client.spent, 8)
        report['uncertain_reserve_usd'] = client.uncertain
        report['stage_estimated_usd'] = round(client.spent-ledger['previous_spend'], 8)
        write_json(out/'report.json', report)
        write_json(out/'repair.json', repair)
        client.key = ''
        print({'repair_finished': True, 'people': repair['people'], 'failures': repair['failures'], 'cumulative_estimated_usd': client.spent}, flush=True)


if __name__ == '__main__':
    main()
