"""The benchmark must not reward row uniqueness, duplicates or forced agreement."""
import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0,str(Path(__file__).parent/'behavior'))
from build_study import clean,deduplicate
from run_benchmark import HERE, make_cards,validate_evidence
from analyze_benchmark import differential_effect,stable
from meta_pipeline import persona_prompt,read
from meta_pipeline import simulate
from test_pipeline import ExternalStub,scenes


class BehaviorContract(unittest.TestCase):
    def test_custom_policy_cards_use_the_actual_scheduler_without_mutation(self):
        with tempfile.TemporaryDirectory() as temp:
            cards,_=make_cards(read(HERE/'policies.json'))
            summary,records=simulate(ExternalStub(Path(temp)),{'scenes':scenes()},'custom',2,workers=2,persona_cards=cards[:2])
            self.assertEqual({r['persona_id'] for r in records},{'v001','v002'})
            self.assertEqual(summary['requested_personas'],2)
            self.assertTrue(all(c['impression']=='' for c in cards))

    def test_counterfactuals_change_exactly_one_declared_field(self):
        plan=read(HERE/'analysis-plan.json')
        self.assertEqual(len(plan['pairs']),14)
        for pair in plan['pairs']:
            a,b=plan['designs'][pair['low_clip']],plan['designs'][pair['high_clip']]
            self.assertEqual([k for k in a if a[k]!=b[k]],[pair['changed_config_field']])

    def test_toy_outputs_are_computed(self):
        self.assertEqual(clean('  Send   the   draft  today.  '),'Send the draft today.')
        self.assertEqual(deduplicate(['A12','B07','A12','C04','B07']),['A12','B07','C04'])

    def test_matched_timing_and_heldout_task(self):
        clips=read(HERE/'stimuli-runtime.json')['clips']
        self.assertEqual(len(clips),30)
        self.assertTrue(all(c['duration_sec']==8 for c in clips))
        self.assertTrue(all([(s['start_sec'],s['end_sec']) for s in c['scenes']]==[(0,3),(3,8)] for c in clips))
        self.assertTrue(all(c['task']=='rows' for c in clips if c['phase']=='heldout'))

    def test_duplicate_label_does_not_create_a_distinct_definition(self):
        cards,mapping=make_cards(read(HERE/'policies.json'),alias=True)
        self.assertEqual(len(cards),8)
        self.assertEqual(len({x['id'] for x in cards}),8)
        self.assertEqual(cards[-1]['card'],cards[-2]['card'])
        self.assertEqual(mapping['v007']['card_sha256'],mapping['v008']['card_sha256'])

    def test_runtime_prompt_has_no_expected_outcome_or_other_viewer(self):
        cards,_=make_cards(read(HERE/'policies.json'),alias=True)
        scene={'index':0,'start_sec':0,'end_sec':3,'audio':{'speech_transcript':''},
               'features':{'observations':[{'id':'s0-o0','description':'Current visible words'}]}}
        prompt=persona_prompt(cards[0],scene)
        for key in ('sensitive_policy','reference_policy','hypothesis','low_clip','high_clip','heldout','v002'):
            self.assertNotIn(key,prompt)

    def test_future_evidence_reference_is_rejected(self):
        item={'scenes':[{'features':{'observations':[{'id':'s0-o0'}]}}]}
        with self.assertRaises(ValueError):
            validate_evidence([{'scene':0,'evidence_ids':['s1-o0']}],item)
        validate_evidence([{'scene':0,'evidence_ids':['s0-o0']}],item)

    def test_repetition_noise_is_not_declared_stable(self):
        self.assertIsNone(stable(['high']))
        self.assertIsNone(stable(['low','high']))
        self.assertIsNone(stable(['low','medium','high']))
        self.assertEqual(stable(['high','high','low']),'high')

    def test_generic_quality_effect_cannot_pass_as_persona_differentiation(self):
        self.assertEqual(differential_effect([2,2,2],[2,2,2]),([0,0,0],False))
        self.assertTrue(differential_effect([2,1,2],[0,0,0])[1])
        self.assertFalse(differential_effect([2,None,2],[0,0,0])[1])


if __name__=='__main__': unittest.main()
