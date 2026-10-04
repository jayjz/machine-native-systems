"""E4.1 adapters; E4 consumer, simulator and measurements remain unchanged."""
import gzip, hashlib, importlib.util, itertools, json, platform, statistics, sys, time
from pathlib import Path
ROOT=Path(__file__).resolve().parent
BASE=ROOT.parent/'e4-boundary'
spec=importlib.util.spec_from_file_location('e4',BASE/'run.py'); e4=importlib.util.module_from_spec(spec); spec.loader.exec_module(e4)
OLD_ENCODE,OLD_DECODE=e4.encode,e4.decode
CONTEXT=e4.CONTEXT
UNKNOWN_ATTEMPT='__E41_UNKNOWN_ATTEMPT_NOT_AN_ID__'
def arms():
    return [('full',tuple(CONTEXT))]+[(mode,subset) for mode in ('optimistic','conservative') for n in range(5) for subset in itertools.combinations(CONTEXT,n)]
def label(mode,subset): return mode+':'+('+'.join(subset) or 'empty')
def encode(public,arm,style,case):
    if arm=='full': return OLD_ENCODE(public,'typed-full',style,case)
    subset=arm.split(':')[1].split('+')
    record=json.loads(OLD_ENCODE(public,'typed-full',style,case))
    for field in CONTEXT:
        if field not in subset: record['record'].pop(field)
    return json.dumps(record)
def decode(wire,arm,consumer):
    if arm=='full': return OLD_DECODE(wire,'typed-full',consumer)
    mode=arm.split(':')[0]; message=json.loads(wire); record=message['record']
    defaults=dict(alternatives=[],attempt=None,status='proposed',receipt=None) if mode=='optimistic' else dict(alternatives=None,attempt=UNKNOWN_ATTEMPT,status=None,receipt=None)
    for key,value in defaults.items(): record.setdefault(key,value)
    return OLD_DECODE(json.dumps(message),'typed-full',consumer)
def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    import argparse
    p=argparse.ArgumentParser(); p.add_argument('--output',type=Path,default=ROOT/'results/run-001'); a=p.parse_args(); a.output.mkdir(parents=True,exist_ok=False)
    cases=json.loads((BASE/'fixtures.json').read_text())['cases']
    e4.encode,e4.decode=encode,decode
    rows=[e4.run_case(c,'full' if m=='full' else label(m,s),pr,co,st) for c,(m,s),pr,co,st in itertools.product(cases,arms(),e4.PRODUCERS,e4.CONSUMERS,('ordered','reordered'))]
    for r in rows:
        r['abstention_cost']=r['expected'] in ('completed','confirmed') and not r['useful_completion']
        r['rejected']=r['decoded'] is None
        r['missing_wire_fields']=[k for k in CONTEXT if k not in json.loads(r['wire'])['record']]
    raw=''.join(json.dumps(r,sort_keys=True)+'\n' for r in rows).encode(); (a.output/'raw.jsonl.gz').write_bytes(gzip.compress(raw,mtime=0))
    summary=e4.summarize(rows)
    for s in summary:
        rr=[r for r in rows if r['arm']==s['arm'] and r['consumer']==s['consumer']]
        s.update(abstention_cost=sum(r['abstention_cost'] for r in rr), abstained=sum(r['result']['outcome']=='abstained' for r in rr), unresolved=sum(r['result']['outcome']=='unresolved' for r in rr), rejected=sum(r['rejected'] for r in rr), failures=sorted({r['case'] for r in rr if not r['oracle_agreement']}))
    sufficient=[]
    for s in summary:
        if s['agreement']==s['n'] and s['useful']==s['eligible'] and s['recovered']==s['recovery_n'] and not any(s[k] for k in ['duplicate_rows','authority_violations','false_verifications']): sufficient.append(s['arm']+'|'+s['consumer'])
    (a.output/'summary.json').write_text(json.dumps(dict(n=len(rows),groups=summary,sufficient=sufficient),indent=2)+'\n')
    cfg=dict(python=sys.version,platform=platform.platform(),command='python3 experiments/e4-1/run.py',source_hashes={str(p.relative_to(ROOT.parent.parent)):digest(p) for p in [ROOT/'run.py',ROOT/'PROTOCOL.md',BASE/'run.py',BASE/'fixtures.json']},model_calls=0,raw_bytes=len(raw),raw_sha256=hashlib.sha256(raw).hexdigest())
    (a.output/'configuration.json').write_text(json.dumps(cfg,indent=2)+'\n')
    (a.output/'SHA256SUMS').write_text(''.join(f'{digest(p)}  {p.name}\n' for p in sorted(a.output.iterdir()) if p.is_file())+f'{hashlib.sha256(raw).hexdigest()}  raw.jsonl (decompressed)\n')
    print(json.dumps(dict(rows=len(rows),sufficient=sufficient)))
if __name__=='__main__': main()
