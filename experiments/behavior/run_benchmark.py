"""Repeated blinded viewer-policy benchmark using the actual scene scheduler.

The analysis plan is deliberately not imported. No expected effect, factor,
variant, split or other viewer's response appears in the inference payload.
"""
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import hashlib
import json
from pathlib import Path
import random
import subprocess
import sys
import time

sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from meta_pipeline import PipelineClient, MODEL, read, simulate, ffmpeg
from meta_smoke import STR, BOOL, obj, digest, write_json

HERE=Path(__file__).resolve().parent
SCHEMA=obj({'verdicts':{'type':'array','items':obj({
    'persona_id':STR,'still_watching':BOOL,'reason':STR,'impression':STR,
    'interest':{'type':'string','enum':['low','medium','high']},
    'would_try':{'type':'string','enum':['no','unsure','yes']},
    'primary_concern':{'type':'string','enum':['usefulness','clarity','evidence','privacy','friction','recovery','interaction','relevance','other']},
    'evidence_ids':{'type':'array','items':STR},
})}})


def prepare(out,film):
    spec=read(HERE/'stimuli-runtime.json')
    out.mkdir(parents=True,exist_ok=True)
    media={}
    def one(pair):
        index,clip=pair
        cid=clip['id']
        path=out/f'{cid}.mp4'
        ffmpeg('-ss',index*8,'-i',film,'-t',8,'-an','-r',24,'-c:v','libx264','-preset','fast','-crf',18,path)
        item={'id':cid,'path':str(path),'sha256':digest(path.read_bytes()),'duration_sec':8,'scenes':[]}
        for source in clip['scenes']:
            i=source['index']; start,end=source['start_sec'],source['end_sec']
            visual=out/f'{cid}-s{i}.mp4'; frame=out/f'{cid}-s{i}.png'
            ffmpeg('-ss',start,'-i',path,'-t',end-start,'-an','-c:v','libx264','-preset','fast','-crf',18,visual)
            ffmpeg('-ss',(end-start)/2,'-i',visual,'-frames:v',1,frame)
            visible=source['visible_content']
            lines=['CLIPDESK LAB',visible['title'],*visible['body'],visible['footer'],'Constructed test stimulus · toy operation']
            features={'source':'verbatim content from deterministic rendered card, not an evaluative summary',
                      'frame_evidence_id':f's{i}-frame',
                      'observations':[{'id':f's{i}-o{j}','description':line} for j,line in enumerate(lines)],
                      'source_interval':{'start_sec':start,'end_sec':end,'granularity':'source card interval'}}
            item['scenes'].append({'index':i,'start_sec':start,'end_sec':end,'path':str(visual),
                'sha256':digest(visual.read_bytes()),'frame_path':str(frame),'frame_sha256':digest(frame.read_bytes()),
                'features':features,'features_sha256':digest(json.dumps(features,sort_keys=True).encode()),
                'audio_sha256':digest(b'no audio stream by controlled design'),
                'audio':{'audio_track_present':False,'non_silent':False,'speech_detected':False,'speech_transcript':''},
                'file_id':None})
        return cid,item
    with ThreadPoolExecutor(max_workers=2) as pool:
        media=dict(pool.map(one,enumerate(spec['clips'])))
    write_json(out/'media.json',media)
    write_json(out/'preparation.json',{'render_sha256':digest(Path(film).read_bytes()),'clips':len(media),
        'source_manifest_sha256':digest((HERE/'stimuli-runtime.json').read_bytes()),'duration_sec':len(media)*8})
    print(json.dumps({'prepared_clips':len(media),'api_calls':0}))


def make_cards(policies,alias=False):
    entries=list(policies['policies'])
    if alias:
        entries.append(dict(entries[-1],id='baseline-alias',label='Identical baseline card, different instance ID'))
    cards=[]; mapping={}
    for i,p in enumerate(entries):
        pid=f'v{i+1:03d}'
        mapping[pid]={'policy_id':p['id'],'card_sha256':digest(json.dumps(p['card'],sort_keys=True).encode())}
        cards.append({'id':pid,'card':p['card'],'impression':'','context':policies['context']+
            ' This is a constructed toy-operation demo, not a claim of a shipping product. Judge the depicted workflow on its own terms. '+
            'No forced disagreement or test outcome. Interest is low/medium/high and willingness to try is no/unsure/yes. '+
            'Cite only exact current observation IDs or the current frame_evidence_id provided in the scene; do not cite a priority as evidence that a flaw exists.'})
    return cards,mapping


def validate_evidence(records,item):
    for r in records:
        scene=item['scenes'][r['scene']]
        allowed={x['id'] for x in scene['features']['observations']}|{f's{r["scene"]}-frame'}
        if not r.get('evidence_ids') or not set(r['evidence_ids'])<=allowed:
            raise ValueError('missing, fabricated or future evidence reference')


def run(out,assets,previous,phase):
    if (out/'ledger.json').exists():
        raise SystemExit('Existing charged run: inspect its process and artifacts; never start a duplicate.')
    out.mkdir(parents=True,exist_ok=True)
    spec=read(HERE/'stimuli-runtime.json'); policies=read(HERE/'policies.json'); media=read(assets/'media.json')
    freeze=read(HERE/'freeze.json')
    for name,sha in freeze['files'].items():
        assert digest((HERE/name).read_bytes())==sha,'frozen study changed before inference'
    client=PipelineClient(out,previous)
    client.limit=9.5  # still below the owner's cumulative $10 ceiling
    report={'kind':'SYNTHETIC_BEHAVIOR_BENCHMARK_NOT_HUMAN_VALIDATION','model':MODEL,'phase':phase,
            'source_sha':subprocess.check_output(['git','rev-parse','HEAD']).decode().strip(),
            'freeze_sha256':digest((HERE/'freeze.json').read_bytes()),'jobs':[],'failures':[]}
    jobs=[]
    for clip in spec['clips']:
        if clip['phase']!=phase: continue
        for rep in range(clip['repetitions']):
            jid=hashlib.sha256(f"trial-v1:{clip['id']}:{rep}".encode()).hexdigest()[:16]
            jobs.append({'id':jid,'clip_id':clip['id'],'repeat':rep})
    random.Random(61028).shuffle(jobs)
    write_json(out/'schedule.json',jobs)
    started=time.monotonic()
    try:
        catalog=client.call('catalog','GET','/models'); assert MODEL in {x['id'] for x in catalog['data']}
        def one(job):
            clip=media[job['clip_id']]
            cards,mapping=make_cards(policies,alias=True)
            summary,records=simulate(client,clip,job['id'],len(cards),workers=7,prefix=job['id'],
                                     persona_cards=cards,verdict_schema=SCHEMA)
            validate_evidence(records,clip)
            return dict(job,mapping=mapping,summary=summary)
        # Four independently scheduled seven-viewer cohorts, bounded at 28 HTTP
        # generations; control alias cohorts use 32. Each viewer remains sequential.
        with ThreadPoolExecutor(max_workers=4) as pool:
            pending={pool.submit(one,job):job for job in jobs}
            for future in as_completed(pending):
                try:
                    result=future.result(); report['jobs'].append(result)
                except Exception as exc:
                    report['failures'].append({'job':pending[future], 'error':client.safe(exc)})
                write_json(out/'report.json',report)
    finally:
        client.cleanup()
        report.update(wall_sec=round(time.monotonic()-started,3),
                      phase_estimated_usd=round(client.spent-client.previous_spend,8),
                      cumulative_estimated_usd=round(client.spent,8),uncertain_reserve_usd=client.uncertain)
        write_json(out/'report.json',report); client.key=''
        print(json.dumps({'finished':phase,'jobs':len(report['jobs']),'failures':len(report['failures']),
                          'cumulative_estimated_usd':report['cumulative_estimated_usd'],'uncertain_reserve_usd':client.uncertain}),flush=True)


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('command',choices=['prepare','run'])
    parser.add_argument('--out',type=Path,required=True)
    parser.add_argument('--film',type=Path)
    parser.add_argument('--assets',type=Path)
    parser.add_argument('--previous-ledger',type=Path)
    parser.add_argument('--phase',choices=['development','heldout','controls'])
    args=parser.parse_args()
    if args.command=='prepare': prepare(args.out,args.film)
    else: run(args.out,args.assets,args.previous_ledger,args.phase)
