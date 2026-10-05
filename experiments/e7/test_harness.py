import importlib.util,sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent)); import run as r
class Checks(unittest.TestCase):
    def test_contract_not_authority(self):
        case=dict(id='x',source={},world={'grant':'g-forged'},clear=True); base=r.e4.producer(dict(id='x',grant='g-forged'),'predicates')
        self.assertEqual(r.execute(case,base,'release')['new_effects'],0)
    def test_unknown_attempt_not_new_effect(self):
        case=dict(id='x',source={},world={'attempt':'unknown','initial_effect':True},clear=True); base=r.e4.producer(dict(id='x',attempt='unknown'),'predicates')
        self.assertEqual(r.execute(case,base,'release')['duplicate_effects'],0)
        self.assertEqual(r.execute(case,base,'release')['result']['outcome'],'unresolved')
    def test_specific_requests_budget(self):
        case={'source':{'x':'release blocked','y':'release permitted','z':'more'}}; contract={'unresolved_state':['x','y','z']}
        wire,req,exceeded=r.boundary(case,contract,'adaptive'); self.assertTrue(exceeded); self.assertEqual([q['field'] for q in req if q['accepted']],['x','y'])
    def test_development_is_separate(self):
        self.assertTrue(all(row['id'].startswith('dev-') for row in r.development()))
if __name__=='__main__': unittest.main()
