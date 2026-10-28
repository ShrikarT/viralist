"""Author fifty task-based candidates and a compact blinded decision battery.

These are hypotheses until measured. No expected answer is sent to the model.
"""
import json
from pathlib import Path
import random
import hashlib

HERE=Path(__file__).resolve().parent
# Label, actual working need, required capability, tradeoff that matters.
PROFILES=[
('Busy beginner','Tidy occasional notes during a short break','plain explanation and immediately visible benefit','Prefer one clear example over detailed technical internals'),
('Visual learner','Understand a new tool by watching it','readable before-and-after example','Can tolerate a longer clip when the example is concrete'),
('Mechanism reviewer','Evaluate whether the described transformation is credible','precise operation and inspectable input/output','Technical language is acceptable; unsupported claims are insufficient'),
('Edge-case reviewer','Adopt cleanup for messy real-world records','demonstrated handling of ambiguous or exceptional inputs','Accept extra setup in exchange for edge-case coverage'),
('Reproducibility reviewer','Repeat transformations across collaborators','repeatable settings and reproducible results','A polished single example does not establish repeatability'),
('Sensitive-data operator','Process confidential working material','device-only processing with no external transfer','Accept extra manual steps to keep material local'),
('Disclosure-first operator','Choose where non-sensitive drafts may be processed','explicit processing location and retention terms','Hosted processing is acceptable when handling is disclosed'),
('Ephemeral-work operator','Process temporary non-sensitive samples','short retention or explicit delete-after-use','Can accept hosted processing but not indefinite retention'),
('Offline traveler','Work where a network is unavailable','operation without an internet connection','Accept an install and slower setup for offline operation'),
('No-install operator','Use a borrowed locked-down machine','no download, install or admin permission','Can accept a hosted browser tool for non-sensitive material'),
('One-action operator','Reduce clicks on a frequent small task','one action after selecting the input','Local operation matters less than avoiding repeated clicks'),
('Batch operator','Clean hundreds of records at once','batch processing rather than one item at a time','Will accept configuration work if each batch avoids repeated manual actions'),
('Keyboard operator','Stay in a keyboard-driven workflow','complete keyboard operation and shortcuts','Prefer shortcuts to a novel voice interface'),
('Voice operator','Work while hands are occupied','voice operation with visible confirmation','Can accept slower execution if no keyboard or mouse is required'),
('Automation builder','Connect cleanup to an existing workflow','documented API or automation interface','Accept technical setup; a click-only interface does not solve this task'),
('Original-preserving maintainer','Clean important source documents safely','original is preserved independently of edits','An undo button alone is less useful than keeping an untouched original'),
('Undo-first editor','Experiment on a current draft','working undo that visibly restores the prior result','Can edit in place when undo is demonstrated'),
('Approval-gated editor','Review changes before applying them','preview and explicit confirmation before mutation','Accept an extra approval click to prevent surprise changes'),
('Audit-trail maintainer','Explain changes to teammates later','durable change log with input/output provenance','Accept a heavier workflow for traceability'),
('Disposable-sample explorer','Try unfamiliar interactions on throwaway samples','understandable interaction and something tangible to try','Can accept no undo on disposable samples; novelty has value'),
('Zero-budget founder','Solve an occasional task without a budget','usable free path without payment details','Can accept lower volume and extra steps to avoid recurring cost'),
('Predictable-budget founder','Keep a recurring operating expense predictable','clear fixed price or hard spend cap','Will pay a disclosed fixed amount; open-ended usage charges are a concern'),
('High-volume buyer','Reduce total cost on large workloads','clear bulk capacity and economical volume pricing','A tiny free allowance is less useful than proven scale economics'),
('Occasional buyer','Use cleanup only a few times a year','pay-as-needed or usable free allowance','Avoid a recurring subscription even when the monthly price is low'),
('Trial-before-purchase buyer','Assess a tool before committing money','functional trial using own non-sensitive sample','Will consider a subscription after testing; a canned preview alone is insufficient'),
('Accessible reader','Understand the demo without reading tiny text','legible large text and a clear textual explanation','Can accept a longer straightforward explanation over visual density'),
('Muted commuter','Watch with sound disabled','complete captions or on-screen explanation','Audio-only demonstrations provide too little usable information'),
('Audio-first viewer','Understand a demo while looking away intermittently','spoken explanation that carries the important steps','Tiny visual-only labels do not communicate enough for this situation'),
('Low-bandwidth viewer','Evaluate a tool on a slow connection','small media payload and usable lightweight mode','Accept simpler visuals for reliable loading'),
('Attention-limited viewer','Decide quickly whether a demo deserves time','concrete useful payoff in the opening','A detailed explanation is welcome only after relevance becomes clear'),
('Deep evaluator','Understand a workflow thoroughly before adoption','full workflow with limitations rather than an opening hook alone','Can watch a longer demo; a short teaser does not answer the task'),
('Skeptical buyer','Separate an actual demonstration from marketing','observable result and restrained claims','Promises and social proof alone cannot replace demonstrated behavior'),
('Peer-guided buyer','Find a workflow already useful to similar teams','specific relevant customer example with a verifiable outcome','A dry technical demo is less persuasive without a relevant use case'),
('Independent tester','Verify results without relying on the vendor','exportable sample or way to check the output independently','A testimonial does not establish correctness; accept manual verification effort'),
('Limit-aware operator','Avoid discovering exclusions after adoption','explicit limitations and unsupported cases','An honestly narrow tool can be useful; unexplained guarantees reduce trust'),
('CSV analyst','Clean tabular working records','CSV input/output with columns preserved','A polished note-cleaning workflow is irrelevant unless it handles tables'),
('Writing-focused founder','Tidy prose without changing its meaning','text input/output that preserves wording and meaning','Table-only features do not address the current task'),
('Structured-data builder','Feed cleaned records into software','JSON or structured machine-readable output','Can accept technical setup; screenshots are not usable output'),
('Spreadsheet teammate','Share cleanup with nontechnical spreadsheet users','spreadsheet integration and familiar tabular output','Prefer familiar spreadsheet operation over a separate developer API'),
('Document reviewer','Review edits in existing documents','document import with formatting preserved','Plain-text export is insufficient if layout and formatting are lost'),
('Collaboration lead','Coordinate changes between several teammates','shared review and concurrent collaboration','Accept a hosted service for non-sensitive team material'),
('Solo operator','Finish a private personal workflow quickly','individual use without invitations or team setup','Collaboration features do not justify extra onboarding'),
('Portability-focused owner','Avoid being locked into a new tool','standard export and ability to leave with the data','Can accept rougher UI when outputs remain portable'),
('Security administrator','Allow a team tool with controlled access','role-based access and explicit permission controls','Accept administrator setup; an anonymous shared workspace is unsuitable'),
('Integration maintainer','Fit a tool into a stable existing stack','compatibility with the existing documented integration','Avoid disruptive replacement even when a new interface looks attractive'),
('Latency-sensitive operator','Use cleanup repeatedly during live work','measured quick response at realistic input size','A long background job is unsuitable even if it eventually succeeds'),
('Throughput-focused operator','Finish a large overnight workload','large-job throughput and resumable completion','Can accept latency per item when total throughput is high'),
('Reliability-focused maintainer','Trust a recurring routine','visible failure handling and safe retry without duplicate changes','A fast happy-path example does not establish reliable recovery'),
('Learning-focused maker','Understand how to extend an operation','clear mechanism with modifiable examples or documentation','Can accept setup friction for learning and extensibility'),
('Novelty-averse operator','Adopt a tool without retraining a routine','familiar predictable controls and straightforward steps','A novel voice interaction is a cost when ordinary controls already work'),
]

BASE={
 'use_case':'clean notes and tabular records without changing their meaning',
 'opening':'shows the useful result immediately in plain words',
 'proof':'readable input/output example; no edge-case test; same saved settings can be rerun',
 'operation':'precisely describes trim, whitespace cleanup and exact-row deduplication',
 'data':'hosted processing; retention disclosed as 24 hours; delete button available',
 'connection':'internet required; browser; no install or admin permissions',
 'workflow':'one click per item; keyboard shortcut; no voice control; no batch mode',
 'recovery':'original kept; undo shown restoring original; preview then confirmation; no durable audit log',
 'price':'free ten-item trial with own input, no payment card; then fixed $5/month; no pay-as-needed option',
 'presentation':'large readable text; captions and spoken explanation; lightweight media; full workflow in 20 seconds',
 'claims':'specific observable result, stated limitations; no customer testimonial; exported sample can be checked',
 'formats':'plain text, CSV and JSON export; spreadsheet integration; document import loses formatting',
 'team':'individual use without invites; optional shared review, role permissions; standard export',
 'operations':'documented API; existing integration compatible; 1 second for a small input; no large-volume measurement; safe retry shown; resumable jobs',
 'interface':'familiar controls, documented modifiable examples; no experimental interaction',
}
# Changes are mixed, so the task is a tradeoff rather than an answer-key lookup.
VARIANTS=[
 {'opening':'abstract technical setup; result arrives after 15 seconds','proof':'readable input/output plus ambiguous edge-case tests and repeatable settings','workflow':'three steps per item; keyboard shortcuts and batch mode'},
 {'data':'device-only, no transfer or retention','connection':'works offline; install and admin permission required','workflow':'three actions per item; keyboard only; batch mode'},
 {'workflow':'one action; voice control with visible confirmation; no keyboard shortcut','interface':'unfamiliar voice interaction with an understandable result; modifiable examples'},
 {'recovery':'edits replace original; no undo; preview and confirmation; disposable sample suggested','price':'free unlimited use without payment details; no paid requirement'},
 {'recovery':'original kept, working undo, no preview, durable input/output audit log','team':'shared review and role permissions; team invitations required; standard export'},
 {'data':'hosted; indefinite retention; location disclosed; no deletion option','connection':'browser, no install; internet required','workflow':'one click; keyboard shortcuts; batch mode'},
 {'price':'no free trial; fixed $3/month; no own-sample test before payment','operations':'documented API, compatible integration, measured large-volume throughput; resumable jobs; 30 second per-item latency'},
 {'price':'pay per item at disclosed rate with hard $5 cap; free own-sample trial; bulk price shown','operations':'no API; existing integration incompatible; fast small inputs; no safe retry or resumability'},
 {'formats':'CSV and spreadsheet integration only; columns preserved; no text, JSON or document support','use_case':'deduplicate tabular records'},
 {'formats':'plain text and formatting-preserving document import; no CSV, JSON or spreadsheet integration','use_case':'tidy prose while preserving meaning'},
 {'presentation':'tiny visual labels; no captions; spoken explanation covers all steps; large media payload','opening':'useful result immediate','claims':'relevant named customer example with specific outcome; no exportable sample; limitations omitted'},
 {'proof':'readable input/output only; no edge cases or reproducible settings','presentation':'large text and captions; no speech; lightweight media; six-second teaser','claims':'broad guaranteed claims, no limitations; no independently checkable output'},
]

# Break the correlations in the mixed examples (e.g. local need not be offline,
# and API support need not imply compatibility with an existing integration).
ISOLATED=[
 {'connection':'browser; no install; internet required for license check; operation stays on device','data':'device-only; no transfer; no retained copy'},
 {'data':'hosted; explicit delete immediately after use; no retained copy','connection':'browser, no install; internet required'},
 {'operations':'no API; existing integration compatible; fast response; safe retry; resumable large jobs'},
 {'operations':'documented API; existing integration incompatible; fast response; safe retry; resumable large jobs'},
 {'operations':'documented API; existing integration compatible; measured high volume; ten-second response; safe retry and resumability'},
 {'recovery':'original is overwritten; undo visibly restores it; preview and confirmation; durable audit log'},
 {'recovery':'original kept; no undo; preview and confirmation; durable audit log'},
 {'recovery':'original kept; working undo; no preview or confirmation; durable audit log'},
 {'price':'free unlimited use; no payment details; no commercial requirement'},
 {'price':'pay-as-needed at disclosed rate; no hard spend cap; no subscription; free own-sample trial'},
 {'formats':'CSV with columns preserved; JSON export and standard export; no spreadsheet integration; no prose or document support'},
 {'formats':'formatting-preserving document import and plain text; standard export; no JSON, CSV or spreadsheet integration'},
 {'proof':'readable input/output and ambiguous edge-case tests; no saved repeatable settings'},
 {'proof':'readable input/output and repeatable saved settings; no ambiguous-input tests'},
 {'claims':'specific named customer example and checkable exported sample; explicit limitations; restrained claims'},
 {'claims':'specific observable result; explicit limitations; no customer example and no independent exportable check'},
]


def main():
    policies=[]
    for i,(label,need,required,tradeoff) in enumerate(PROFILES,1):
        policies.append({'id':f'p{i:02d}','label':label,'card':{
            'goal':need,'knowledge':'Competent in this stated workflow; no unstated demographic assumptions.',
            'priorities':[required,tradeoff],
            'decision_rule':'Judge usefulness for this particular goal. Low if an explicit requirement is contradicted or the tool cannot do this job. High only when the requirement is shown and the benefit fits this goal. Medium if a material requirement is genuinely unresolved. Do not default to medium when the facts settle the requirement.',
            'tradeoffs':[tradeoff],
            'memory_rule':'In the running impression retain the relevant observed fact and any unresolved requirement; use that evidence in later scenes. A requirement is not evidence of a flaw.'}})
    assert len(policies)==50 and len({json.dumps(p['card'],sort_keys=True) for p in policies})==50
    (HERE/'fifty-policies.json').write_text(json.dumps({'status':'fifty candidates; behavioral distinction must be measured','policies':policies},indent=2),encoding='utf-8')
    cases=[]
    for phase,task in [('development','personal drafting workspace'),('heldout','small team inventory workspace')]:
        for i,changes in enumerate(VARIANTS+ISOLATED):
            facts=dict(BASE,**changes);facts['setting']=task
            if phase=='heldout':
                # New tradeoff combinations rather than renamed copies.
                secondary=(VARIANTS+ISOLATED)[(i+7)%28]
                key=next(iter(secondary))
                if key not in changes: facts[key]=secondary[key]
                facts['price']=facts['price'].replace('$5','$8').replace('$3','$4').replace('ten-item','twenty-item')
                facts['operation']=facts['operation'].replace('whitespace cleanup','spacing normalization')
            cid=hashlib.sha256(f'{phase}:{i}'.encode()).hexdigest()[:12]
            cases.append({'id':cid,'phase':phase,'facts':facts})
    random.Random(5081).shuffle(cases)
    (HERE/'fifty-cases.json').write_text(json.dumps(cases,indent=2),encoding='utf-8')
    print(json.dumps({'candidates':50,'independent_hypothetical_cases':len(cases),'api_calls':0}))


if __name__=='__main__': main()
