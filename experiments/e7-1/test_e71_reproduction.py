import gzip,importlib.util,json,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('e71_reproduction',ROOT/'run.py'); r=importlib.util.module_from_spec(spec); spec.loader.exec_module(r)
# E7 reuse adds its directory; restore this discovery directory for sibling tests.
sys.path.insert(0,str(ROOT))
class Reproduction(unittest.TestCase):
    def test_refit_and_all_7680_outputs(self):
        folder=ROOT/'results/run-001'; dev,producers,consumers,training,checks=r.fit()
        self.assertEqual(dev,json.loads((folder/'development.json').read_text()))
        spec=importlib.util.spec_from_file_location('e71_new_cases',ROOT/'evaluation.py'); data=importlib.util.module_from_spec(spec); spec.loader.exec_module(data)
        cases=data.cases(); self.assertEqual(cases,json.loads((folder/'evaluation.json').read_text()))
        lookup={c['id']:c for c in cases}
        self.assertEqual(training,[json.loads(l) for l in gzip.open(folder/'training.jsonl.gz','rt')])
        states={'producer':{f:r.e7.state(m) for f,m in producers.items()},'consumer':{reg:{f:r.e7.state(m) for f,m in models.items()} for reg,models in consumers.items()}}
        self.assertEqual(states,json.load(gzip.open(folder/'model-state.json.gz','rt')))
        self.assertEqual(checks,json.loads((folder/'summary.json').read_text())['training_checks'])
        volatile={'inference_ns','tool_ns'}
        for old in map(json.loads,gzip.open(folder/'raw.jsonl.gz','rt')):
            new=r.evaluate_case(lookup[old['case']],*(old[k] for k in ['regime','producer','consumer','arm','access','orientation']),producers,consumers)
            self.assertEqual({k:v for k,v in new.items() if k not in volatile},{k:v for k,v in old.items() if k not in volatile})
if __name__=='__main__': unittest.main()
