"""Validate preserved raw integrity and aggregate measures without inference."""
import gzip,hashlib,importlib.util,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent
for name in ('e4-boundary','e4-1','e7'):
    folder=ROOT/name/'results/run-001'; raw=gzip.decompress((folder/'raw.jsonl.gz').read_bytes()); rows=[json.loads(line) for line in raw.splitlines()]
    for line in (folder/'SHA256SUMS').read_text().splitlines():
        if line.startswith('# decompressed raw.jsonl SHA256: '): assert hashlib.sha256(raw).hexdigest()==line.rsplit(' ',1)[1]; continue
        if not line.strip(): continue
        expected,path=line.split('  ',1); content=raw if path.endswith('(decompressed)') else (folder/path).read_bytes()
        assert hashlib.sha256(content).hexdigest()==expected,(name,path)
    cfg=json.loads((folder/'configuration.json').read_text()); assert len({(r['case'],r['arm'],r['producer'],r['consumer'],r.get('style')) for r in rows})==len(rows)
    if 'source_hashes' in cfg:
        for path,h in cfg['source_hashes'].items(): assert hashlib.sha256((ROOT.parent/path).read_bytes()).hexdigest()==h,path
    summary=json.loads((folder/'summary.json').read_text())
    if name=='e7':
        for g in summary['groups']:
            group=[r for r in rows if (r['arm'],r['producer'],r['consumer'])==(g['arm'],g['producer'],g['consumer'])]
            assert g['n']==len(group)
            for key,fn in [('decision_correct',lambda r:r['decision_correct']),('proposal_correct',lambda r:r['proposal_correct']),('useful',lambda r:r['useful_completion']),('incoherent_effects',lambda r:r['execution']['incoherent_effects']),('authority_violations',lambda r:r['execution']['authority_violations']),('duplicates',lambda r:r['execution']['duplicate_effects']),('false_verifications',lambda r:r['execution']['false_verification'])]: assert g[key]==sum(fn(r) for r in group),(name,g['arm'],key)
    elif name=='e4-1':
        for g in summary['groups']:
            group=[r for r in rows if (r['arm'],r['consumer'])==(g['arm'],g['consumer'])]
            assert g['agreement']==sum(r['oracle_agreement'] for r in group)
            assert g['useful']==sum(r['useful_completion'] for r in group)
            assert g['duplicate_rows']==sum(r['duplicate_effects']>0 for r in group)
    print(name,'integrity/aggregate checks OK',len(rows),'rows')
