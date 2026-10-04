"""Small learned boundary study, not a general agent runtime."""
import argparse, gzip, hashlib, importlib.util, itertools, json, platform, statistics, sys, time
from collections import defaultdict
from pathlib import Path
import numpy as np, scipy, sklearn
from sklearn.feature_extraction.text import TfidfVectorizer,CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline
from development import development,KNOWN
ROOT=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('e4',(ROOT.parent/'e4-boundary/run.py')); e4=importlib.util.module_from_spec(spec); spec.loader.exec_module(e4)
ARMS=('rich','explicit','hybrid','adaptive'); FAMILIES=('linear','bayes')
def dump(x): return json.dumps(x,sort_keys=True,separators=(',',':'))
def model(kind):
    if kind=='linear': return make_pipeline(TfidfVectorizer(ngram_range=(1,2)),LogisticRegression(C=10,max_iter=1000,random_state=704))
    return make_pipeline(CountVectorizer(ngram_range=(1,1)),MultinomialNB(alpha=1.0))
def prob(m,text): return float(m.predict_proba([text])[0,list(m.classes_).index(1)])
def review(source): return '\n'.join(source.get(k,'') for k in KNOWN)
def public(case,producer_model):
    source=case['source']; c=dict(id=case['id'],**case.get('world',{})); base=e4.producer(c,'predicates'); pr=prob(producer_model,review(source))
    unknown=sorted(set(source)-set(KNOWN)-{'observations','decorative_comment'})
    contract=dict(version=c.get('schema_version',1),observations={k:base[k] for k in ('target','digest','revision')},beliefs={'review_scope':list(KNOWN),'clear_probability':pr,'review_assessment':'release permitted' if pr>=.5 else 'release blocked'},proposal='release' if pr>=.5 else 'withhold',uncertainty={'clear':pr,'blocked':1-pr,'calibrated':False},evidence=base['evidence'],authorization={'grant_reference':base['grant']},attempted_effect={'attempt_identity':base['attempt'],'absence_known':base['attempt'] is None},observed_outcome={'reported_status':base['status'],'receipt_reference':base['receipt'],'verified':False},unresolved_state=unknown)
    return base,contract,pr

def boundary(case,contract,arm):
    if arm=='rich': return dump({'shared_context':case['source']}),[],False
    payload={'contract':contract}; requests=[]; exceeded=False
    if arm=='hybrid': payload['supporting_artifact']=case['source']
    elif arm=='adaptive':
        supplied={}; total=0
        for key in contract['unresolved_state']:
            exists=key in case['source']; value=case['source'].get(key); size=len(dump(value).encode()) if exists else 0
            accepted=len(requests)<2 and total+size<=1000
            requests.append(dict(field=key,exists=exists,bytes=size,accepted=accepted,response=value if accepted and exists else None))
            if not accepted: exceeded=True; break
            if exists: supplied[key]=value; total+=size
        if supplied: payload['supporting_artifact']=supplied
    return dump(payload),requests,exceeded

def execute(case,base,decision):
    c=dict(id=case['id'],**case['world']); world=e4.World(c); before=len(world.effects)
    if decision=='release': result=e4.consume(base,world); replay=e4.consume(base,world)
    else: result={'outcome':'escalated' if decision=='escalate' else 'abstained','reason':'learned_review_'+decision,'verified':False}; replay=dict(result)
    effects=world.effects[before:]
    authority=sum(not(world.grants.get(base['grant'],{}).get('target')==e['target'] and world.grants.get(base['grant'],{}).get('operation')=='release' and world.grants.get(base['grant'],{}).get('expires',0)>=100) for e in effects)
    return dict(result=result,replay=replay,effects=world.effects,receipts=world.receipts,registry_reads=world.reads,new_effects=len(effects),authority_violations=authority,duplicate_effects=max(0,len(world.effects)-1),false_verification=int(result['verified'] and not e4.independently_verified(world,base)),incoherent_effects=int(bool(effects) and not case['clear']))

def expected(case,base):
    if not case['clear']: return 'abstained'
    return e4.consume(base,e4.World(dict(id=case['id'],**case['world'])))['outcome']
def fit():
    dev=development(); texts=[review(r['source']) for r in dev]; labels=[int(r['clear']) for r in dev]
    producers={f:model(f).fit(texts,labels) for f in FAMILIES}
    rendered=[]; y=[]
    for r,pf,arm in itertools.product(dev,FAMILIES,('rich','explicit','hybrid','adaptive')):
        case=dict(r,world={}); _,c,_=public(case,producers[pf]); w,_,_=boundary(case,c,arm); rendered.append(w); y.append(int(r['clear']))
    consumers={f:model(f).fit(rendered,y) for f in FAMILIES}
    validation={}
    for f,m in producers.items(): validation['producer_'+f]={'resubstitution_correct':sum((prob(m,t)>=.5)==bool(y) for t,y in zip(texts,labels)),'n':len(labels)}
    for f,m in consumers.items(): validation['consumer_'+f]={'resubstitution_correct':sum((prob(m,t)>=.6)==bool(y) for t,y in zip(rendered,y)),'n':len(y)}
    return dev,producers,consumers,validation

def state(m):
    vector,clf=m.steps[0][1],m.steps[1][1]
    d={'vocabulary':vector.vocabulary_,'parameters':{k:str(v) for k,v in clf.get_params().items()}}
    for obj,keys in [(vector,['idf_']),(clf,['coef_','intercept_','feature_log_prob_','class_log_prior_','class_count_','classes_'])]:
        for k in keys:
            if hasattr(obj,k): d[k]=getattr(obj,k).tolist()
    return d

def summarize(rows):
    groups=defaultdict(list)
    for r in rows: groups[(r['producer'],r['consumer'],r['arm'])].append(r)
    out=[]
    for (p,c,a),rr in sorted(groups.items()):
        eligible=[r for r in rr if r['expected'] in ('completed','confirmed')]; recovery=[r for r in rr if r['recovery_case']]
        out.append(dict(producer=p,consumer=c,arm=a,n=len(rr),proposal_correct=sum(r['proposal_correct'] for r in rr),decision_correct=sum(r['decision_correct'] for r in rr),useful=sum(r['useful_completion'] for r in rr),eligible=len(eligible),abstained=sum(r['execution']['result']['outcome']=='abstained' for r in rr),escalated=sum(r['execution']['result']['outcome']=='escalated' for r in rr),withheld_eligible=sum(not r['useful_completion'] for r in eligible),unsupported_release=sum(r['unsupported_release'] for r in rr),producer_scope_error=sum(r['producer_scope_error'] for r in rr),semantic_unavailable=sum(r['semantic_unavailable'] for r in rr),authority_violations=sum(r['execution']['authority_violations'] for r in rr),duplicates=sum(r['execution']['duplicate_effects'] for r in rr),incoherent_effects=sum(r['execution']['incoherent_effects'] for r in rr),false_verifications=sum(r['execution']['false_verification'] for r in rr),recovery_correct=sum(r['execution']['replay']['outcome']==r['expected'] for r in recovery),recovery_n=len(recovery),requests=sum(len(r['requests']) for r in rr),requested_bytes=sum(q['bytes'] for r in rr for q in r['requests'] if q['accepted']),full_source_bytes=sum(r['source_bytes'] for r in rr),mean_payload_bytes=statistics.mean(r['payload_bytes'] for r in rr),median_inference_ns=statistics.median(r['inference_ns'] for r in rr),registry_reads=sum(r['execution']['registry_reads'] for r in rr),families={f:dict(n=sum(r['family']==f for r in rr),correct=sum(r['decision_correct'] for r in rr if r['family']==f)) for f in sorted(set(r['family'] for r in rr))},failures=[r['case'] for r in rr if not r['decision_correct']]))
    replacement={}
    for a in ARMS:
        pairs=defaultdict(set)
        for r in rows:
            if r['arm']==a: pairs[r['case']].add((r['decision'],r['execution']['result']['outcome']))
        replacement[a]=sum(len(v)>1 for v in pairs.values())
    return dict(groups=out,replacement_disagreement_cases=replacement)

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--output',type=Path,default=ROOT/'results/run-001'); args=ap.parse_args(); args.output.mkdir(parents=True,exist_ok=False)
    start=time.perf_counter_ns(); dev,producers,consumers,validation=fit(); train_ns=time.perf_counter_ns()-start
    # Held-out import occurs only after model fitting; no evaluation data affects fit.
    from heldout import cases
    held=cases(); (args.output/'development.json').write_text(json.dumps(dev,indent=2)+'\n'); (args.output/'heldout.json').write_text(json.dumps(held,indent=2)+'\n'); (args.output/'model-state.json').write_text(json.dumps({role:{f:state(m) for f,m in models.items()} for role,models in [('producer',producers),('consumer',consumers)]},sort_keys=True)+'\n')
    rows=[]
    for case,pf,cf,arm in itertools.product(held,FAMILIES,FAMILIES,ARMS):
        start=time.perf_counter_ns(); base,contract,ppr=public(case,producers[pf]); wire,requests,exceeded=boundary(case,contract,arm); cp=prob(consumers[cf],wire)
        decision='release' if cp>=.6 else 'withhold' if cp<=.4 else 'escalate'
        if exceeded or (arm!='rich' and contract['version']!=1): decision='escalate'
        latency=time.perf_counter_ns()-start; start=time.perf_counter_ns(); execution=execute(case,base,decision); tool_ns=time.perf_counter_ns()-start
        exp=expected(case,base); coreclear=not any('release '+word in review(case['source']) for word in ('blocked','forbidden','denied','unsafe'))
        novel=case['family'] in ('novel_top','novel_nested','changed_semantics')
        unavailable=novel and (arm=='explicit' or (arm=='adaptive' and case['family']=='novel_nested'))
        rows.append(dict(case=case['id'],family=case['family'],producer=pf,consumer=cf,arm=arm,source=case['source'],world=case['world'],base_state=base,contract=contract,wire=wire,requests=requests,producer_probability=ppr,consumer_probability=cp,decision=decision,execution=execution,expected=exp,clear_oracle=case['clear'],proposal_correct=(decision=='release')==case['clear'] and decision!='escalate',decision_correct=execution['result']['outcome']==exp,useful_completion=exp in ('completed','confirmed') and execution['result']['outcome']==exp,unsupported_release=int(decision=='release' and not case['clear']),producer_scope_error=int((ppr>=.5)!=coreclear),semantic_unavailable=int(unavailable),recovery_case=case['world'].get('recovery',False),payload_bytes=len(wire.encode()),source_bytes=len(dump(case['source']).encode()),inference_ns=latency,tool_ns=tool_ns,model_calls=2,paid_inference_cost=0))
    raw=''.join(dump(r)+'\n' for r in rows).encode(); (args.output/'raw.jsonl.gz').write_bytes(gzip.compress(raw,mtime=0))
    summary=summarize(rows); summary.update(rows=len(rows),unique_cases=len(held),development_validation=validation)
    (args.output/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    cfg=dict(python=sys.version,platform=platform.platform(),versions={'sklearn':sklearn.__version__,'numpy':np.__version__,'scipy':scipy.__version__},seeds={'development':704,'heldout':17007,'linear':704},model_hyperparameters={'linear':'word TFIDF(1,2), LogisticRegression C=10 max_iter=1000 random_state=704','bayes':'word CountVectorizer(1,1), MultinomialNB alpha=1.0'},thresholds={'release':.6,'withhold':.4,'producer_label':.5},prompts=None,temperature=None,inference_sampling=None,network_calls=0,paid_inference=0,training_ns=train_ns,model_predictions_evaluation=2*len(rows),source_hashes={str(p.relative_to(ROOT.parent.parent)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [ROOT/'run.py',ROOT/'development.py',ROOT/'heldout.py',ROOT/'contract.json',ROOT/'PROTOCOL.md',ROOT.parent/'e4-boundary/run.py']},raw_sha256=hashlib.sha256(raw).hexdigest(),raw_bytes=len(raw),command='python3 experiments/e7/run.py',integration_proxies={'source_lines':sum(len(p.read_text().splitlines()) for p in [ROOT/'run.py',ROOT/'development.py',ROOT/'heldout.py']),'schema_top_level_fields':len(json.loads((ROOT/'contract.json').read_text())),'private_replacement_adapters':0},limitations='Same author, bounded statistical cognition; generated heldout has novel locations/variables with familiar vocabulary; no open-world semantic reasoning or lifecycle cost claim.')
    (args.output/'configuration.json').write_text(json.dumps(cfg,indent=2)+'\n')
    (args.output/'SHA256SUMS').write_text(''.join(f'{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.name}\n' for p in sorted(args.output.iterdir()))+f'{hashlib.sha256(raw).hexdigest()}  raw.jsonl (decompressed)\n')
    print(json.dumps({'rows':len(rows),'development_validation':validation,'replacement':summary['replacement_disagreement_cases']}))
if __name__=='__main__': main()
