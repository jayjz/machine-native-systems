import importlib.util, json, unittest
from pathlib import Path
spec=importlib.util.spec_from_file_location('experiment',Path(__file__).with_name('run.py')); r=importlib.util.module_from_spec(spec); spec.loader.exec_module(r)
class Checks(unittest.TestCase):
    def test_legacy_equivalence(self):
        for c in json.loads((r.BASE/'fixtures.json').read_text())['cases']:
            v=r.e4.producer(c,'predicates'); w=r.encode(v,'optimistic:empty','ordered',c)
            for consumer in r.e4.CONSUMERS:
                if v['version']==3 or (v['version']==2 and consumer=='v1-only'): continue
                self.assertEqual(r.decode(w,'optimistic:empty',consumer),r.OLD_DECODE(r.OLD_ENCODE(v,'typed-compact','ordered',c),'typed-compact',consumer))
    def test_unknown_not_absent(self):
        c={'id':'a'}; v=r.e4.producer(c,'predicates'); decoded=r.decode(r.encode(v,'conservative:empty','ordered',c),'conservative:empty','compatible')
        self.assertIsNone(decoded['alternatives']); self.assertEqual(decoded['attempt'],r.UNKNOWN_ATTEMPT); self.assertIsNone(decoded['status'])
        self.assertFalse(r.e4.consume(decoded,r.e4.World(c))['verified'])
    def test_all_fields_exact(self):
        c={'id':'a'}; v=r.e4.producer(c,'graph'); arm=r.label('conservative',r.CONTEXT)
        self.assertEqual(v,r.decode(r.encode(v,arm,'reordered',c),arm,'compatible'))
if __name__=='__main__': unittest.main()
