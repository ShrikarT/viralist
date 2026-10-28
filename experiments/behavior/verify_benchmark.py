"""Reconcile actual benchmark requests, current-only inputs and cumulative cost.

This is author verification of experimental artifacts, not independent acceptance.
No provider requests are made.
"""
import argparse
import json
from pathlib import Path
import sys

sys.path[:0]=[str(Path(__file__).resolve().parent),str(Path(__file__).resolve().parents[1])]
from meta_pipeline import read,persona_prompt
from meta_smoke import digest,write_json
from run_benchmark import HERE,make_cards,validate_evidence


def verify(directory,assets):
    report=read(directory/'report.json'); ledger=read(directory/'ledger.json')
    schedule=read(directory/'schedule.json'); media=read(assets/'media.json')
    spec=read(HERE/'stimuli-runtime.json'); freeze=read(HERE/'freeze.json')
    preparation=read(assets/'preparation.json')
    deviation=read(assets/'encoding-deviation.json')
    assert digest((assets/'media.json').read_bytes())==deviation['media_sha256']
    assert preparation['render_sha256']==freeze['film_sha256']
    assert preparation['source_manifest_sha256']==digest((HERE/'stimuli-runtime.json').read_bytes())
    for name,sha in freeze['files'].items():
        assert digest((HERE/name).read_bytes())==sha
    assert report['freeze_sha256']==digest((HERE/'freeze.json').read_bytes())
    assert report['model']=='muse-spark-1.3'
    expected={(c['id'],r) for c in spec['clips'] if c['phase']==report['phase'] for r in range(c['repetitions'])}
    assert {(s['clip_id'],s['repeat']) for s in schedule}==expected
    assert len({s['id'] for s in schedule})==len(schedule)==len(expected)
    assert not report['failures'],report['failures']
    assert {s['id'] for s in schedule}=={j['id'] for j in report['jobs']}
    previous=Path(ledger['previous_ledger']); prior=read(previous)
    assert digest(previous.read_bytes())==ledger['previous_ledger_sha256']
    assert ledger['previous_spend']==prior['estimated_from_reported_usage']
    assert ledger['uncertain_charge_reserve']>=prior['uncertain_charge_reserve']
    assert abs(ledger['active_reserve'])<1e-6
    assert ledger['estimated_from_reported_usage']+ledger['uncertain_charge_reserve']<=10
    calls=ledger['calls']; paid={c['label']:c for c in calls if c['endpoint']=='/responses'}
    assert len(paid)==sum(c['endpoint']=='/responses' for c in calls)
    assert all(c['status']=='success' for c in calls),[c for c in calls if c['status']!='success']
    assert all(c['requested_model']=='muse-spark-1.3' for c in paid.values())
    assert not any(c['endpoint'].startswith('/files') for c in calls)
    cost=sum(c.get('estimated_cost_usd',0) for c in calls)
    assert abs(ledger['estimated_from_reported_usage']-ledger['previous_spend']-cost)<1e-6
    cards,mapping=make_cards(read(HERE/'policies.json'),alias=True)
    cards={c['id']:c for c in cards}; observed=set(); reactions=0
    for job in report['jobs']:
        assert job['mapping']==mapping
        item=media[job['clip_id']]
        source=next(c for c in spec['clips'] if c['id']==job['clip_id'])
        for scene,original in zip(item['scenes'],source['scenes']):
            visible=original['visible_content']
            lines=['CLIPDESK LAB',visible['title'],*visible['body'],visible['footer'],'Constructed test stimulus · toy operation']
            observed_lines=[o['description'] for o in scene['features']['observations']]
            # A one-off metadata-edit script misdecoded the constant disclosure
            # separator before development. Preserve that run and the exact same
            # input in later phases; do not silently rewrite paid evidence.
            assert observed_lines[:-1]==lines[:-1]
            assert observed_lines[-1]==deviation['actual_disclosure']
            assert lines[-1]==deviation['rendered_disclosure']
        records=read(directory/f"{job['id']}-reactions.json")
        dispatch=read(directory/f"{job['id']}-dispatch-audit.json")
        assert not job['summary']['failures'],job['summary']['failures']
        lookup={(r['persona_id'],r['scene']):r for r in records}
        assert len(lookup)==len(records)==len(dispatch)
        assert {r['persona_id'] for r in records}==set(cards)
        validate_evidence(records,item)
        for d in dispatch:
            pid,index=d['persona_id'],d['scene']; scene=item['scenes'][index]
            assert index in (0,1)
            person=dict(cards[pid])
            if index:
                prior_verdict=lookup[pid,index-1]
                assert prior_verdict['still_watching']
                assert prior_verdict['accepted_unix']<=d['dispatched_unix']
                person['impression']=prior_verdict['impression']
            assert d['prompt']==persona_prompt(person,scene),'unexpected context or peer/future leakage'
            assert not d['previous_response_id_present'] and d['file_id'] is None
            assert d['image_sha256']==scene['frame_sha256']==digest(Path(scene['frame_path']).read_bytes())
            assert d['media_sha256']==scene['sha256']==digest(Path(scene['path']).read_bytes())
            assert d['features_sha256']==scene['features_sha256']==digest(json.dumps(scene['features'],sort_keys=True).encode())
            assert scene['features']['source_interval']['start_sec']==scene['start_sec']
            assert scene['features']['source_interval']['end_sec']==scene['end_sec']
            label=f"{job['id']}-s{index}-{pid}"
            assert label in paid and label not in observed
            assert paid[label]['usage']['input_tokens']<=d['input_context_upper_bound_with_margin']
            observed.add(label)
        reactions+=len(records)
    assert observed==set(paid),'unreconciled charged decisions'
    result={'author_check_only':True,'phase':report['phase'],'source_sha':report['source_sha'],
            'freeze_sha256':report['freeze_sha256'],'cohorts':len(schedule),'viewer_trials':len(schedule)*len(cards),
            'reactions':reactions,'post_skip_or_context_leaks':0,'unreconciled_decisions':0,
            'estimated_cumulative_usd':ledger['estimated_from_reported_usage'],
            'unknown_charge_reserve_usd':ledger['uncertain_charge_reserve'],'provider_file_uploads':0,
            'constant_metadata_encoding_deviation':deviation,
            'limitations':'Experimental static-card scene inputs; no human calibration, production integration or independent review.'}
    write_json(directory/'verified.json',result)
    print(json.dumps(result))
    return result


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--run',type=Path,required=True);p.add_argument('--assets',type=Path,required=True)
    a=p.parse_args();verify(a.run,a.assets)
