"""Read-only integrity and preregistered contrast reconstruction, no inference."""
import gzip,hashlib,importlib.util,json
from pathlib import Path
ROOT=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('e71_audit',ROOT/'run.py'); run=importlib.util.module_from_spec(spec); spec.loader.exec_module(run)
def verify():
    folder=ROOT/'results/run-001'
    for line in (folder/'SHA256SUMS').read_text().splitlines():
        expected,name=line.split('  ',1)
        content=gzip.decompress((folder/(name[:-len(' (decompressed)')]+'.gz')).read_bytes()) if name.endswith(' (decompressed)') else (folder/name).read_bytes()
        assert hashlib.sha256(content).hexdigest()==expected,name
    cfg=json.loads((folder/'configuration.json').read_text())
    for name,h in cfg['source_hashes'].items(): assert run.sha((ROOT.parent.parent/name).read_bytes())==h,name
    rows=[json.loads(l) for l in gzip.open(folder/'raw.jsonl.gz','rt')]
    assert len(rows)==7680
    keys=[tuple(r[k] for k in ['case','regime','producer','consumer','arm','access','orientation']) for r in rows]
    assert len(set(keys))==len(rows)
    summary=json.loads((folder/'summary.json').read_text())
    assert run.aggregate(rows)==summary['groups']
    assert run.causal_analysis(rows)==summary['analysis']
    assert run.manipulation_checks(rows)==summary['manipulation_checks']
    print('E7.1 archive/source integrity, 7680 unique crossed rows and all aggregates/causal criteria reconstructed; verdict',summary['analysis']['pooled_classification'])
    return rows
if __name__=='__main__': verify()
