import copy,importlib.util,json,sys,unittest
from pathlib import Path
spec=importlib.util.spec_from_file_location('e71',Path(__file__).with_name('run.py')); r=importlib.util.module_from_spec(spec); spec.loader.exec_module(r)
class BoundaryChecks(unittest.TestCase):
    def public(self):
        base=r.e7.e4.producer({'id':'test'},'predicates')
        return dict(version=1,beliefs={'review_assessment':'release permitted','clear_probability':.9,'review_scope':['reviewer_note','supporting_note']},proposal='release',uncertainty={'clear':.9,'blocked':.1,'calibrated':False},observations={'target':base['target']},authorization={'grant_reference':base['grant']},attempted_effect={'attempt_identity':None},observed_outcome={'reported_status':'proposed'},evidence=base['evidence'],unresolved_state=[])
    def test_masks_every_assessment_channel(self):
        c=self.public(); a=r.transform(c,masked=True); b=r.transform(c,complement=True,masked=True)
        self.assertEqual(a,b)
        for path in r.ASSESSMENT_PATHS:
            value=a
            for key in path: value=value[key]
            self.assertIsNone(value)
        for key in ['observations','authorization','attempted_effect','observed_outcome','evidence']: self.assertEqual(a[key],c[key])
        self.assertEqual(a['beliefs']['review_scope'],c['beliefs']['review_scope']); self.assertEqual(c['proposal'],'release')
    def test_supporting_context_equal(self):
        source={'reviewer_note':'release permitted','new_rule':'release blocked'}; case={'source':source}; c=self.public(); c['unresolved_state']=['new_rule']
        for arm in r.e7.ARMS:
            outputs=[r.e7.boundary(case,r.transform(c,complement=flip,masked=mask),arm) for flip in [False,True] for mask in [False,True]]
            supports=[json.loads(o[0]).get('supporting_artifact',json.loads(o[0]).get('shared_context')) for o in outputs]
            self.assertTrue(all(s==supports[0] for s in supports)); self.assertTrue(all(o[1]==outputs[0][1] for o in outputs))
    def test_stratified_flips(self):
        dev=r.e7.development()
        for seed in r.SEEDS.values():
            selected=r.allocations(dev,seed)
            for label in [True,False]: self.assertEqual(sum(x['id'] in selected for x in dev if x['clear']==label),sum(x['clear']==label for x in dev)//2)
    def test_authority_unchanged(self):
        case=dict(id='gate',source={},world={'grant':'g-forged'},clear=True)
        base=r.e7.e4.producer(dict(id='gate',grant='g-forged'),'predicates')
        self.assertEqual(r.e7.execute(case,base,'release')['new_effects'],0)
    def test_new_case_integrity(self):
        spec=importlib.util.spec_from_file_location('newcases',Path(__file__).with_name('evaluation.py')); data=importlib.util.module_from_spec(spec); spec.loader.exec_module(data)
        cases=data.cases(); self.assertEqual(len(cases),40); self.assertEqual(len({c['id'] for c in cases}),40)
        old=json.loads((Path(__file__).parent.parent/'e7/results/run-001/heldout.json').read_text())
        old_sources={r.e7.dump(x['source']) for x in old}
        self.assertFalse(any(r.e7.dump(x['source']) in old_sources for x in cases))
        grouped={}
        for c in cases:
            if c['pair']: grouped.setdefault(c['pair'],[]).append(c)
        self.assertEqual(len(grouped),12); self.assertTrue(all(len(pair)==2 and {c['clear'] for c in pair}=={False,True} for pair in grouped.values()))
if __name__=='__main__': unittest.main()
