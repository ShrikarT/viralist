"""Observable decision comparisons; no LLM judge and no forced diversity quota."""
import argparse
from collections import Counter,defaultdict
import csv
import itertools
import json
from pathlib import Path
import sys

sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from meta_pipeline import read
from meta_smoke import write_json

HERE=Path(__file__).resolve().parent
RANK={'low':0,'medium':1,'high':2}


def stable(values):
    if len(values)<2: return None
    mode,count=Counter(values).most_common(1)[0]
    return mode if count>=2 and (len(values)>2 or count==len(values)) else None


def differential_effect(target,reference):
    values=[a-b if a is not None and b is not None else None for a,b in zip(target,reference)]
    return values, None not in values and len(values)>=2 and sum(x>0 for x in values)>=2


def collect(dirs):
    trials=[]; rows=[]; reports=[]; seen_jobs=set()
    for directory in dirs:
        report=read(directory/'report.json'); reports.append(report)
        for job in report['jobs']:
            if job['id'] in seen_jobs: raise ValueError('duplicate cohort would inflate repeated evidence')
            seen_jobs.add(job['id'])
            records=read(directory/f"{job['id']}-reactions.json")
            grouped=defaultdict(list)
            for r in records:
                policy=job['mapping'][r['persona_id']]['policy_id']
                grouped[policy].append(r)
                rows.append({'phase':report['phase'],'clip_id':job['clip_id'],'repeat':job['repeat'],
                             'policy_id':policy,'job_id':job['id'],**r})
            for pid,values in grouped.items():
                values.sort(key=lambda r:r['scene'])
                final=values[-1]
                if any(f['persona_id']==final['persona_id'] for f in job['summary']['failures']):
                    continue
                trials.append({'phase':report['phase'],'clip_id':job['clip_id'],'repeat':job['repeat'],
                               'policy_id':pid,'reached_last':final['scene']==1,'interest':final['interest'],
                               'would_try':final['would_try'],'concern':final['primary_concern'],
                               'reason':final['reason'],'evidence_ids':final['evidence_ids'],'job_id':job['id']})
    return trials,rows,reports


def analyze(dirs,out):
    out.mkdir(parents=True,exist_ok=True)
    trials,rows,reports=collect(dirs)
    plan=read(HERE/'analysis-plan.json'); definitions=read(HERE/'policies.json')
    policies=[p['id'] for p in definitions['policies']]
    lookup={(t['policy_id'],t['clip_id'],t['repeat']):t for t in trials}
    cells=defaultdict(list)
    for t in trials: cells[t['policy_id'],t['clip_id']].append(t)
    matrix=[]
    for pair in plan['pairs']:
        expected=2 if pair['phase']=='development' else 3
        for pid in policies:
            for rep in range(expected):
                lo=lookup.get((pid,pair['low_clip'],rep)); hi=lookup.get((pid,pair['high_clip'],rep))
                matrix.append({'pair':pair['id'],'phase':pair['phase'],'factor':pair['factor'],'policy_id':pid,
                               'repeat':rep,'complete':bool(lo and hi),
                               'interest_delta':RANK[hi['interest']]-RANK[lo['interest']] if lo and hi else None,
                               'low_interest':lo['interest'] if lo else None,'high_interest':hi['interest'] if hi else None,
                               'low_reached_last':lo['reached_last'] if lo else None,'high_reached_last':hi['reached_last'] if hi else None,
                               'low_try':lo['would_try'] if lo else None,'high_try':hi['would_try'] if hi else None,
                               'low_reason':lo['reason'] if lo else None,'high_reason':hi['reason'] if hi else None,
                               'low_job':lo['job_id'] if lo else None,'high_job':hi['job_id'] if hi else None})
    effects={}
    for pair in plan['pairs']:
        sensitive=pair['sensitive_policy']; reference=pair['reference_policy']
        a=[x for x in matrix if x['pair']==pair['id'] and x['policy_id']==sensitive]
        b={x['repeat']:x for x in matrix if x['pair']==pair['id'] and x['policy_id']==reference}
        values,supported=differential_effect([x['interest_delta'] for x in a],[b[x['repeat']]['interest_delta'] for x in a])
        effects[pair['id']]={'factor':pair['factor'],'phase':pair['phase'],'sensitive_policy':sensitive,
                             'reference_policy':reference,'paired_differential_interest':values,
                             'positive_repeats':sum(v is not None and v>0 for v in values),
                             'requested_repeats':len(values),'supported':supported,
                             'interpretation':'exploratory ordinal direction check; not significance or human prediction accuracy'}
    status=[]
    for p in definitions['policies']:
        if p.get('baseline'): continue
        anchors=[x for x in effects.values() if x['sensitive_policy']==p['id']]
        factors={x['factor'] for x in anchors}
        paired=[f for f in factors if any(x['factor']==f and x['phase']=='development' and x['supported'] for x in anchors)
                and any(x['factor']==f and x['phase']=='heldout' and x['supported'] for x in anchors)]
        status.append({'policy_id':p['id'],'label':p['label'],'anchor_factors_supported_in_both_phases':sorted(paired),
                       'status':'retain-prototype' if paired else 'not-yet-demonstrated',
                       'reason':'At least one preregistered differential response replicated on an unseen task.' if paired else
                                'No preregistered anchor met the development and heldout criterion; do not count labels as behavioral diversity.'})
    signatures={}
    for pid in policies:
        signatures[pid]={cid:stable([(t['reached_last'],t['interest'],t['would_try']) for t in values])
                         for (p,cid),values in cells.items() if p==pid}
    separation=[]
    for a,b in itertools.combinations(policies,2):
        different=[]; unresolved=[]
        for cid in signatures[a].keys()|signatures[b].keys():
            x,y=signatures[a].get(cid),signatures[b].get(cid)
            if x is None or y is None: unresolved.append(cid)
            elif x!=y: different.append(cid)
        phases={pair['phase'] for pair in plan['pairs'] if pair['low_clip'] in different or pair['high_clip'] in different}
        separation.append({'policy_a':a,'policy_b':b,'stable_different_clips':different,'unresolved_clips':unresolved,
                           'observed_across_both_phases':len(different)>=2 and phases=={'development','heldout'},
                           'interpretation':'Observed synthetic response separation on this set only; not statistical independence.'})
    retained={x['policy_id'] for x in status if x['status']=='retain-prototype'}
    overlaps=[x for x in separation if x['policy_a'] in retained and x['policy_b'] in retained and not x['observed_across_both_phases']]
    # Merge only exact stable observational duplicates. Insufficient evidence is
    # marked unresolved, never mislabeled proof that two policies are identical.
    aliases=[]
    for x in overlaps:
        if not x['stable_different_clips'] and not x['unresolved_clips']:
            aliases.append({'alias':x['policy_b'],'representative':x['policy_a'],'scope':'exact observed signature on this benchmark'})
            retained.discard(x['policy_b'])
    failures=[f for report in reports for f in report['failures']]
    alias_checks=[]
    for cid in {t['clip_id'] for t in trials}:
        a=[t for t in trials if t['policy_id']=='baseline' and t['clip_id']==cid]
        b=[t for t in trials if t['policy_id']=='baseline-alias' and t['clip_id']==cid]
        sig=lambda values:stable([(t['reached_last'],t['interest'],t['would_try']) for t in values])
        x,y=sig(a),sig(b)
        alias_checks.append({'clip_id':cid,'baseline_stable':x,'alias_stable':y,
                             'stable_disagreement':x is not None and y is not None and x!=y})
    noise=sum(x['stable_disagreement'] for x in alias_checks)
    floor=max(2,noise+2)
    for item in separation:
        item['observed_across_both_phases'] = item['observed_across_both_phases'] and len(item['stable_different_clips'])>=floor
    # At most six candidates: choose a deterministic maximal fully separated
    # subset. Passing an anchor alone never earns another distinct persona count.
    separated={frozenset((s['policy_a'],s['policy_b'])) for s in separation if s['observed_across_both_phases']}
    candidate=sorted(retained); chosen=[]
    for size in range(len(candidate),-1,-1):
        matches=[list(group) for group in itertools.combinations(candidate,size)
                 if all(frozenset(pair) in separated for pair in itertools.combinations(group,2))]
        if matches: chosen=matches[0]; break
    retained=set(chosen)
    overlaps=[s for s in separation if s['policy_a'] in candidate and s['policy_b'] in candidate and not s['observed_across_both_phases']]
    for item in status:
        if item['status']=='retain-prototype' and item['policy_id'] not in retained:
            item['status']='anchor-supported-but-pairwise-unresolved'
    result={'kind':'SYNTHETIC_POLICY_DIFFERENTIATION_ONLY','frozen_study':read(HERE/'freeze.json'),
            'phases_observed':sorted({r['phase'] for r in reports}),'valid_trials':len(trials),'scene_reactions':len(rows),
            'failures':failures,'policy_status':status,'anchor_effects':effects,'pairwise_separation':separation,
            'identical_card_alias_checks':alias_checks,
            'stable_alias_disagreement_clips':noise,'minimum_pairwise_different_clips':floor,
            'provisional_aliases':aliases,'retained_policy_ids':sorted(retained),'candidate_pairwise_overlap':overlaps,
            'unresolved_retained_pair_overlap':[s for s in overlaps if s['policy_a'] in retained and s['policy_b'] in retained],
            'ready_for_50_distinct_claim':False,'reason_50_not_claimed':'At most six candidate decision policies were tested; unique combinations do not establish 50 distinguishable behaviors.',
            'no_forced_disagreement':True,'human_validation':False}
    write_json(out/'analysis.json',result)
    selected=[p for p in definitions['policies'] if p['id'] in retained]
    write_json(out/'retained-policies.json',{'status':'experimental prototypes supported on this benchmark only',
               'policies':selected,'aliases':aliases,'unproven':[s for s in status if s['status']!='retain-prototype']})
    with (out/'comparison-matrix.csv').open('w',encoding='utf-8',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=list(matrix[0])); writer.writeheader();writer.writerows(matrix)
    md=['# Behavioral-diversity evidence matrix','','Synthetic decisions, not real audience forecasts. No quota required disagreement.','',
        '| Policy | Status | Anchors reproduced on heldout task |','|---|---|---|']
    md.extend(f"| {s['label']} | {s['status']} | {', '.join(s['anchor_factors_supported_in_both_phases']) or 'none'} |" for s in status)
    md+=['','## Paired effects','','Interest is ordinal (low / medium / high); vectors show repeated changes relative to the preregistered reference policy.','',
         '| Pair | Target / reference | Differential directions | Supported |','|---|---|---|---|']
    md.extend(f"| {key} | {v['sensitive_policy']} / {v['reference_policy']} | {v['paired_differential_interest']} | {v['supported']} |" for key,v in effects.items())
    md+=['','## Supporting reactions','','All paired repetitions are included below, including agreement and failures; not selected best cases.']
    for pair in plan['pairs']:
        md+=['',f"### {pair['id']}",'']
        for x in matrix:
            if x['pair']!=pair['id'] or x['policy_id'] not in {pair['sensitive_policy'],pair['reference_policy']}: continue
            md+=[f"- {x['policy_id']} repeat {x['repeat']+1}: {x['low_interest']} → {x['high_interest']}; low: {x['low_reason']}; high: {x['high_reason']}. Evidence jobs: {x['low_job']} / {x['high_job']}."]
    (out/'comparison-matrix.md').write_text('\n'.join(md)+'\n',encoding='utf-8')
    write_json(out/'reaction-rows.json',rows)
    print(json.dumps({'valid_trials':len(trials),'scene_reactions':len(rows),'retained':sorted(retained),
                      '50_distinct_claim':False,'failures':len(failures)}))
    return result


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--runs',type=Path,nargs='+',required=True);parser.add_argument('--out',type=Path,required=True)
    a=parser.parse_args();analyze(a.runs,a.out)
