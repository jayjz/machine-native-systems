"""Re-fit frozen models and replay preserved wires; never tune on failures."""
import gzip,json,sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent)); import run as r
class Reproduction(unittest.TestCase):
    def test_frozen_fit_and_all_recorded_outputs(self):
        folder=Path(__file__).parent/'results/run-001'; dev,ps,cs,_=r.fit()
        self.assertEqual(dev,json.loads((folder/'development.json').read_text()))
        from heldout import cases
        self.assertEqual(cases(),json.loads((folder/'heldout.json').read_text()))
        states={role:{f:r.state(m) for f,m in models.items()} for role,models in [('producer',ps),('consumer',cs)]}
        self.assertEqual(states,json.loads((folder/'model-state.json').read_text()))
        rows=[json.loads(l) for l in gzip.decompress((folder/'raw.jsonl.gz').read_bytes()).splitlines()]
        for row in rows:
            case=dict(id=row['case'],source=row['source'],world=row['world'],clear=row['clear_oracle'])
            base,contract,pp=r.public(case,ps[row['producer']]); wire,requests,exceeded=r.boundary(case,contract,row['arm']); cp=r.prob(cs[row['consumer']],wire)
            self.assertEqual(wire,row['wire']); self.assertEqual(requests,row['requests']); self.assertAlmostEqual(cp,row['consumer_probability'],places=12)
            decision='release' if cp>=.6 else 'withhold' if cp<=.4 else 'escalate'
            if exceeded or (row['arm']!='rich' and contract['version']!=1): decision='escalate'
            self.assertEqual(decision,row['decision']); self.assertEqual(r.execute(case,base,decision),row['execution'])
if __name__=='__main__': unittest.main()
