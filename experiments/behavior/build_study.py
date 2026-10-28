"""Freeze a controlled, synthetic media benchmark before inference.

Produces source HTML, model-safe visible-content manifests, and a separate
analysis-only plan. No expected outcomes enter scene evidence or viewer cards.
"""
import argparse
import hashlib
import html
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROJECT = HERE/'video-project'


def save(path,value):
    path.write_text(json.dumps(value,indent=2,ensure_ascii=False),encoding='utf-8')


def opaque(value):
    return hashlib.sha256(('behavior-study-v1:'+value).encode()).hexdigest()[:12]


def clean(value):
    return ' '.join(value.split())


def deduplicate(rows):
    return list(dict.fromkeys(rows))


BASE = {'proof':True,'language':'plain','payoff':'early','processing':'device','clicks':1,'undo':True,'interaction':'button','blank':False}
FACTORS = [
    ('proof','proof',False,True,'p02','p01'),
    ('language','language','dense','plain','p01','p02'),
    ('pace','payoff','late','early','p01','p02'),
    ('privacy','processing','hosted','device','p03','p04'),
    ('friction','clicks',3,1,'p04','p03'),
    ('recovery','undo',False,True,'p05','p06'),
    ('interaction','interaction','button','voice','p06','p05'),
]


def clip_scenes(config,task):
    before = '  Send   the   draft  today.  ' if task=='notes' else 'A12, B07, A12, C04, B07'
    after = clean(before) if task=='notes' else ', '.join(deduplicate(before.split(', ')))
    benefit = 'Clean messy notes' if task=='notes' else 'Remove duplicate rows'
    dense = 'Canonicalize whitespace tokens' if task=='notes' else 'Apply stable row deduplication'
    title = dense if config['language']=='dense' else benefit
    if config['blank']:
        return [{'title':'...','body':['//// //// ////'],'footer':'...'}, {'title':'...','body':['//// //// ////'],'footer':'...'}]
    settings = [
        'Processing: on this device' if config['processing']=='device' else 'Processing: hosted service',
        'Undo restores the original' if config['undo'] else 'No undo: replaces the original',
        'One action: Clean' if config['clicks']==1 else 'Three actions: Select, Confirm, Clean',
        'Click Clean' if config['interaction']=='button' else 'Voice command: Clean this',
    ]
    result = {'title':title,'body':(['INPUT',before,'OUTPUT',after] if config['proof'] else ['Clean results, instantly.','A simpler way to finish.']),
              'footer':'Result from this toy transformation'}
    explanation = {'title':'How the operation works','body':settings,'footer':('Trim ends and collapse repeated spaces.' if task=='notes' else 'Keep the first occurrence of each row.')}
    # Same two shots and fixed total duration; only their order changes for pace.
    return [result,explanation] if config['payoff']=='early' else [explanation,result]


def escape(value):
    return html.escape(str(value))


def build():
    PROJECT.mkdir(parents=True,exist_ok=True)
    clips=[]; pairs=[]; designs={}
    for split,task,repeats in [('development','notes',2),('heldout','rows',3)]:
        for factor,key,low,high,sensitive,reference in FACTORS:
            ids=[]
            for value in (low,high):
                config=dict(BASE,**{key:value})
                cid=opaque(f'{split}:{factor}:{value}')
                designs[cid]=config
                scenes=clip_scenes(config,task)
                clips.append({'id':cid,'phase':split,'repetitions':repeats,'duration_sec':8,'task':task,
                              'scenes':[{'index':i,'start_sec':0 if i==0 else 3,'end_sec':3 if i==0 else 8,
                                         'visible_content':s} for i,s in enumerate(scenes)]})
                ids.append(cid)
            pairs.append({'id':f'{split}-{factor}','phase':split,'factor':factor,'low_clip':ids[0],'high_clip':ids[1],
                          'changed_config_field':key,'sensitive_policy':sensitive,'reference_policy':reference,
                          'hypothesis':'The sensitive policy responds more to this edit than the reference policy. Failure is allowed; do not force a winner.'})
    for label,blank in [('clear',False),('uninformative',True)]:
        cid=opaque('control:'+label)
        clips.append({'id':cid,'phase':'controls','repetitions':3,'duration_sec':8,'task':'notes',
                      'scenes':[{'index':i,'start_sec':0 if i==0 else 3,'end_sec':3 if i==0 else 8,'visible_content':s}
                                for i,s in enumerate(clip_scenes(dict(BASE,blank=blank),'notes'))]})
    runtime={'schema_version':'behavior-stimuli-v1','kind':'constructed media controls, not product proof',
             'canvas':[720,1280],'fps':24,'source_render_fps':1,
             'timing':'Two static cards, cuts on integer seconds; native encodes duplicate static frames at 24fps without changing visible information.',
             'sound':'deliberate silence in all conditions',
             'clips':clips,'controls':[c['id'] for c in clips if c['phase']=='controls']}
    analysis={'schema_version':'behavior-analysis-v1','policy_version':'behavior-policies-v1','pairs':pairs,
              'designs':designs,
              'rules':{'blinding':'No pair/factor/split/hypothesis/winner labels in model input.',
                       'stability':'A reaction category is stable only when at least two repeats agree; unanimous for two-repeat development cells.',
                       'differentiation':'Use observable watch/interest/try decisions, not descriptive row uniqueness or reason wording alone.',
                       'heldout':'Freeze policy and analysis hashes before development; do not tune after seeing heldout results.',
                       'consensus':'Agreement is allowed. Controls have no disagreement target.',
                       'deduplication':'Aliases with identical cards must not count as new policies. Similar signatures are provisional observed overlap, not proof of identical humans.',
                       'human_validity':'No human corpus or validation participants: evidence establishes synthetic behavior only.'}}
    save(HERE/'stimuli-runtime.json',runtime)
    save(HERE/'analysis-plan.json',analysis)
    sections=[]
    for j,clip in enumerate(clips):
        offset=j*8
        for scene in clip['scenes']:
            s=scene['visible_content']; start=offset+scene['start_sec']; duration=scene['end_sec']-scene['start_sec']
            paragraphs=''.join(f'<p>{escape(x)}</p>' for x in s['body'])
            sid=f'c{j:02d}-s{scene["index"]}'
            sections.append(f'''<section id="{sid}" class="clip" data-start="{start}" data-duration="{duration}" data-track-index="1" data-track-kind="graphics" data-hold="true"><div class="card"><div class="brand">CLIPDESK LAB</div><h1>{escape(s['title'])}</h1><div class="panel">{paragraphs}</div><div class="context">{escape(s['footer'])}</div><div class="disclosure">Constructed test stimulus · toy operation</div></div></section>''')
    document='''<!doctype html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=720,height=1280"><title>Controlled viewer study</title><script src="assets/gsap.min.js"></script><style>
*{box-sizing:border-box}html,body{margin:0;width:720px;height:1280px;overflow:hidden;background:#111820;color:#f7fafc;font-family:Arial,sans-serif}#root{width:720px;height:1280px;position:relative;overflow:hidden}.clip{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;background:#111820}.card{width:100%;height:100%;padding:120px 78px;display:flex;flex-direction:column;gap:34px}.brand{font-size:28px;font-weight:700;color:#9ed8c8;letter-spacing:2px}h1{font-size:54px;line-height:1.08;margin:0;min-height:128px}.panel{min-height:490px;padding:32px;background:#23313f;border:2px solid #8aa4b8;border-radius:16px;display:flex;flex-direction:column;justify-content:center;gap:22px}.panel p{font-size:34px;line-height:1.25;margin:0;white-space:pre-wrap;overflow-wrap:anywhere}.panel p:nth-child(odd){font-weight:700}.context{font-size:30px;line-height:1.25;min-height:90px}.disclosure{font-size:24px;color:#b7c6d4;margin-top:auto}</style></head><body>'''
    document+=f'<div id="root" data-composition-id="study" data-start="0" data-duration="{len(clips)*8}" data-width="720" data-height="1280">'+''.join(sections)+'</div>'
    document+='''<script>const tl=gsap.timeline({paused:true});window.__timelines["study"]=tl;</script></body></html>'''
    (PROJECT/'index.html').write_text(document,encoding='utf-8')
    (PROJECT/'BRIEF.md').write_text('''# Controlled behavioral-diversity fixtures

Purpose: paired, deterministic synthetic media for a viewer-policy benchmark.
Automation/no stops is inherited from the owner's instruction to execute the benchmark.
Every stimulus is 8 seconds, muted, 720x1280 at 24fps, with a 0-3s hook and 3-8s follow-up.
Each pair changes exactly one declared configuration field. Identical style is intentional control, not a launch-film treatment.
Toy results are computed by `clean` and `deduplicate` in the source generator. These fixtures are not real-product proof footage.
No external media, identities, user uploads, music, narration or generated assets are needed.
Development and heldout rows are frozen before inference; expected behavior never appears in the pixels or runtime viewer payload.
''',encoding='utf-8')
    (PROJECT/'SPEC.md').write_text('''# Fixed visual specification

720x1280, 24fps; dark #111820; ink #f7fafc; Arial system font; 78px horizontal safe margin.
Title 54px; content 34px; context 30px; disclosure 24px. Two hard-cut cards per 8-second stimulus.
No gradients, stock imagery, music, decorative animation or condition-specific color changes.
All 30 stimuli share the same layout. Proof, language, shot order, processing location, action count, undo behavior or interaction mode are the only pairwise changes.
Render is local; no publication. Inspect snapshots and decoded scene frames before model runs.
''',encoding='utf-8')
    print(json.dumps({'clips':len(clips),'pairs':len(pairs),'duration_sec':len(clips)*8,'project':str(PROJECT)}))


if __name__=='__main__':
    build()
