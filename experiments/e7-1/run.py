"""E7.1 finite causal diagnostic. Reuses E7 components; no new runtime architecture."""
from __future__ import annotations
import argparse,copy,gzip,hashlib,importlib.util,itertools,json,platform,random,statistics,subprocess,sys,time
from collections import defaultdict
from pathlib import Path
ROOT=Path(__file__).resolve().parent
REPO=ROOT.parent.parent
sys.path.insert(0,str(ROOT.parent/'e7'))
spec=importlib.util.spec_from_file_location('e7_reference',ROOT.parent/'e7/run.py')
e7=importlib.util.module_from_spec(spec); spec.loader.exec_module(e7)
REGIMES=('reliable','decor9101','decor9102')
SEEDS={'decor9101':9101,'decor9102':9102}
ACCESS=('present','masked')
ORIENTATIONS=('actual','complement')
ASSESSMENT_PATHS=(('beliefs','review_assessment'),('beliefs','clear_probability'),('proposal',),('uncertainty','clear'),('uncertainty','blocked'))

def sha(data): return hashlib.sha256(data).hexdigest()
def transform(contract,complement=False,masked=False):
    result=copy.deepcopy(contract)
    if complement:
        p=1-result['beliefs']['clear_probability']
        result['beliefs']['clear_probability']=p
        result['beliefs']['review_assessment']='release permitted' if p>=.5 else 'release blocked'
        result['proposal']='release' if p>=.5 else 'withhold'
        result['uncertainty']['clear']=p; result['uncertainty']['blocked']=1-p
    if masked:
        for path in ASSESSMENT_PATHS:
            parent=result
            for key in path[:-1]: parent=parent[key]
            parent[path[-1]]=None
    return result

def allocations(dev,seed):
    rng=random.Random(seed); chosen=set()
    for label in (False,True):
        ids=sorted(row['id'] for row in dev if row['clear']==label)
        assert len(ids)%2==0
        chosen.update(rng.sample(ids,len(ids)//2))
    return chosen

def fit():
    dev,producers,reliable,validation=e7.fit()
    reference=json.loads((ROOT.parent/'e7/results/run-001/model-state.json').read_text())
    states={role:{f:e7.state(m) for f,m in models.items()} for role,models in [('producer',producers),('consumer',reliable)]}
    assert states==reference,'Stop: reliable reference no longer matches E7 fitted parameters'
    consumers={'reliable':reliable}; training=[]; checks={}
    for regime in REGIMES:
        flipped=set() if regime=='reliable' else allocations(dev,SEEDS[regime])
        texts=[]; labels=[]; counts=defaultdict(int)
        for row,pf,arm in itertools.product(dev,e7.FAMILIES,e7.ARMS):
            case=dict(row,world={}); _,original,_=e7.public(case,producers[pf])
            contract=transform(original,complement=row['id'] in flipped)
            wire,requests,exceeded=e7.boundary(case,contract,arm)
            assert not requests and not exceeded
            texts.append(wire); labels.append(int(row['clear']))
            if arm=='explicit': counts[(bool(row['clear']),contract['proposal']=='release')]+=1
            training.append(dict(regime=regime,case=row['id'],producer=pf,arm=arm,flipped=row['id'] in flipped,clear=row['clear'],source=row['source'],contract=contract,wire=wire))
        if regime!='reliable': consumers[regime]={f:e7.model(f).fit(texts,labels) for f in e7.FAMILIES}
        checks[regime]=dict(flipped_records=len(flipped),flipped_ids=sorted(flipped),labels_per_source_class={str(label):sum(r['clear']==label for r in dev) for label in (False,True)},binary_assessment_contingency={f'truth_{truth}_assessment_{assess}':n for (truth,assess),n in counts.items()},development_resubstitution={f:dict(correct=sum((e7.prob(m,t)>=.6)==bool(y) for t,y in zip(texts,labels)),n=len(labels)) for f,m in consumers[regime].items()})
    return dev,producers,consumers,training,checks

def decision(probability,arm,contract,exceeded):
    result='release' if probability>=.6 else 'withhold' if probability<=.4 else 'escalate'
    if exceeded or (arm!='rich' and contract['version']!=1): result='escalate'
    return result

def evaluate_case(case,regime,pf,cf,arm,access,orientation,producers,consumers):
    start=time.perf_counter_ns()
    base,original,ppr=e7.public(case,producers[pf])
    contract=transform(original,complement=orientation=='complement',masked=access=='masked')
    wire,requests,exceeded=e7.boundary(case,contract,arm)
    cp=e7.prob(consumers[regime][cf],wire)
    action=decision(cp,arm,contract,exceeded)
    infer_ns=time.perf_counter_ns()-start
    start=time.perf_counter_ns(); execution=e7.execute(case,base,action); tool_ns=time.perf_counter_ns()-start
    expected=e7.expected(case,base)
    parsed=json.loads(wire); support=parsed.get('supporting_artifact')
    full_source=parsed.get('shared_context') if arm=='rich' else support
    available=arm in ('rich','hybrid') or (arm=='adaptive' and case['family']=='novel_top')
    return dict(case=case['id'],pair=case['pair'],family=case['family'],regime=regime,producer=pf,consumer=cf,arm=arm,access=access,orientation=orientation,source=case['source'],world=case['world'],clear_oracle=case['clear'],expected=expected,base_state=base,original_contract=original,consumer_contract=contract,wire=wire,wire_sha256=sha(wire.encode()),support_sha256=sha(e7.dump(full_source).encode()),source_sha256=sha(e7.dump(case['source']).encode()),requests=requests,exceeded=exceeded,producer_probability=ppr,consumer_probability=cp,decision=action,execution=execution,proposal_correct=(action=='release')==case['clear'] and action!='escalate',decision_correct=execution['result']['outcome']==expected,useful_completion=expected in ('completed','confirmed') and execution['result']['outcome']==expected,unsupported_release=int(action=='release' and not case['clear']),semantic_unavailable=int(case['family'].startswith('novel') and not available),recovery_case=case['world'].get('recovery',False),payload_bytes=len(wire.encode()),source_bytes=len(e7.dump(case['source']).encode()),inference_ns=infer_ns,tool_ns=tool_ns,model_calls=2,paid_inference_cost=0)

def manipulation_checks(rows):
    groups=defaultdict(list)
    for r in rows: groups[(r['case'],r['producer'],r['arm'])].append(r)
    support_mismatches=sum(len({r['support_sha256'] for r in group})!=1 for group in groups.values())
    request_mismatches=sum(len({e7.dump(r['requests']) for r in group})!=1 for group in groups.values())
    base_mismatches=sum(len({e7.dump(r['base_state']) for r in group})!=1 for group in groups.values())
    masked_groups=defaultdict(list)
    for r in rows:
        if r['access']=='masked': masked_groups[(r['case'],r['regime'],r['producer'],r['consumer'],r['arm'])].append(r)
    leak_rows=sum(len({r['wire_sha256'] for r in group})!=1 for group in masked_groups.values())
    assert not any([support_mismatches,request_mismatches,base_mismatches,leak_rows]),'Stop: uncontrolled context/state or remaining assessment leakage'
    return dict(support_mismatches=support_mismatches,request_mismatches=request_mismatches,base_mismatches=base_mismatches,masked_orientation_wire_mismatches=leak_rows)

def aggregate(rows):
    groups=defaultdict(list)
    for r in rows: groups[(r['regime'],r['producer'],r['consumer'],r['arm'],r['access'],r['orientation'])].append(r)
    summary=[]
    for keys,rr in sorted(groups.items()):
        eligible=[r for r in rr if r['expected'] in ('completed','confirmed')]
        recover=[r for r in rr if r['recovery_case']]
        summary.append(dict(zip(('regime','producer','consumer','arm','access','orientation'),keys))|dict(n=len(rr),proposal_correct=sum(r['proposal_correct'] for r in rr),decision_correct=sum(r['decision_correct'] for r in rr),useful=sum(r['useful_completion'] for r in rr),eligible=len(eligible),abstained=sum(r['execution']['result']['outcome']=='abstained' for r in rr),escalated=sum(r['execution']['result']['outcome']=='escalated' for r in rr),withheld_eligible=sum(not r['useful_completion'] for r in eligible),unsupported_release=sum(r['unsupported_release'] for r in rr),semantic_unavailable=sum(r['semantic_unavailable'] for r in rr),authority_violations=sum(r['execution']['authority_violations'] for r in rr),duplicates=sum(r['execution']['duplicate_effects'] for r in rr),incoherent_effects=sum(r['execution']['incoherent_effects'] for r in rr),false_verifications=sum(r['execution']['false_verification'] for r in rr),recovery_correct=sum(r['execution']['replay']['outcome']==r['expected'] for r in recover),recovery_n=len(recover),requests=sum(len(r['requests']) for r in rr),requested_bytes=sum(q['bytes'] for r in rr for q in r['requests'] if q['accepted']),mean_payload_bytes=statistics.mean(r['payload_bytes'] for r in rr),median_inference_ns=statistics.median(r['inference_ns'] for r in rr),median_tool_ns=statistics.median(r['tool_ns'] for r in rr),registry_reads=sum(r['execution']['registry_reads'] for r in rr),families={f:dict(n=sum(r['family']==f for r in rr),correct=sum(r['decision_correct'] for r in rr if r['family']==f)) for f in sorted({r['family'] for r in rr})},failures=[r['case'] for r in rr if not r['decision_correct']]))
    return summary

def causal_analysis(rows):
    novelty=[r for r in rows if r['family'].startswith('novel')]
    idx={(r['case'],r['regime'],r['producer'],r['consumer'],r['arm'],r['access'],r['orientation']):r for r in novelty}
    analyses=[]
    for pf,cf in itertools.product(e7.FAMILIES,e7.FAMILIES):
        def subset(regime,access,arm='hybrid',orientation='actual'):
            return [r for r in novelty if (r['regime'],r['producer'],r['consumer'],r['arm'],r['access'],r['orientation'])==(regime,pf,cf,arm,access,orientation)]
        base=subset('reliable','present'); n=len(base)
        orientation= [idx[(r['case'],'reliable',pf,cf,'hybrid','present','complement')] for r in base]
        orientation_flips=sum(a['decision']!=b['decision'] for a,b in zip(base,orientation))
        shift=statistics.mean(abs(a['consumer_probability']-b['consumer_probability']) for a,b in zip(base,orientation))
        interventions=[]
        for regime,access in [('reliable','masked'),('decor9101','present'),('decor9102','present'),('decor9101','masked'),('decor9102','masked')]:
            alternate={r['case']:r for r in subset(regime,access)}
            fixed=sum(not r['decision_correct'] and alternate[r['case']]['decision_correct'] for r in base if not r['clear_oracle'])
            new_safe=sum(r['decision_correct'] and not alternate[r['case']]['decision_correct'] for r in base if r['clear_oracle'])
            other=subset(regime,access)
            interventions.append(dict(regime=regime,access=access,fixed_blocked=fixed,new_safe_errors=new_safe,decision_correct=sum(r['decision_correct'] for r in other),safe_useful=sum(r['useful_completion'] for r in other),errors=n-sum(r['decision_correct'] for r in other)))
        base_blocked=sum(not r['decision_correct'] for r in base if not r['clear_oracle'])
        mask_ok=interventions[0]['fixed_blocked']>=6 and interventions[0]['new_safe_errors']<=2
        decor_ok=all(t['fixed_blocked']>=6 and t['new_safe_errors']<=2 for t in interventions[1:3])
        S=base_blocked>=6 and (orientation_flips>=6 or shift>=.20) and (mask_ok or decor_ok)
        I=all(t['errors']>=3 for t in interventions) and all(sum(not r['decision_correct'] for r in subset(reg,'present','rich'))<=1 for reg in REGIMES)
        sensitivity=[]; support_pairs=[]; interactions=[]
        for reg,access in itertools.product(REGIMES,ACCESS):
            actual=subset(reg,access); complement={r['case']:r for r in subset(reg,access,orientation='complement')}
            sensitivity.append(dict(regime=reg,access=access,decision_flips=sum(r['decision']!=complement[r['case']]['decision'] for r in actual),mean_abs_probability_shift=statistics.mean(abs(r['consumer_probability']-complement[r['case']]['consumer_probability']) for r in actual)))
            bypair=defaultdict(dict)
            for r in actual: bypair[r['pair']][r['clear_oracle']]=r
            support_pairs.append(dict(regime=reg,access=access,n_pairs=len(bypair),correct_both=sum(p[True]['decision_correct'] and p[False]['decision_correct'] for p in bypair.values()),decision_different=sum(p[True]['decision']!=p[False]['decision'] for p in bypair.values()),mean_probability_clear_minus_blocked=statistics.mean(p[True]['consumer_probability']-p[False]['consumer_probability'] for p in bypair.values())))
        count=lambda reg,access:sum(r['decision_correct'] for r in subset(reg,access))
        for reg in SEEDS:
            interactions.append(dict(regime=reg,correct_count_difference_in_differences=(count(reg,'present')-count('reliable','present'))-(count(reg,'masked')-count('reliable','masked'))))
        analyses.append(dict(producer=pf,consumer=cf,n=n,baseline_correct=sum(r['decision_correct'] for r in base),baseline_blocked_errors=base_blocked,assessment_orientation_flips=orientation_flips,assessment_mean_abs_shift=shift,interventions=interventions,sensitivity=sensitivity,support_pairs=support_pairs,interactions=interactions,S_supported=S,I_supported=I,classification='C' if S and I else 'A' if S else 'B' if I else 'D'))
    S=all(a['S_supported'] for a in analyses); I=all(a['I_supported'] for a in analyses)
    classification='C' if S and I else 'A' if S else 'B' if I else 'D'
    if len({a['classification'] for a in analyses})!=1: classification='D'
    return dict(configurations=analyses,pooled_classification=classification,S_supported_all=S,I_supported_all=I,warning='Finite same-author paired cases; criterion letter never replaces per-configuration evidence.')

def archive(output):
    manifest=''.join(f'{sha(p.read_bytes())}  {p.name}\n' for p in sorted(output.iterdir()) if p.name!='SHA256SUMS')
    for name in ['raw.jsonl','training.jsonl','model-state.json']:
        manifest+=f'{sha(gzip.decompress((output/(name+".gz")).read_bytes()))}  {name} (decompressed)\n'
    (output/'SHA256SUMS').write_text(manifest)

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--output',type=Path,default=ROOT/'results/run-001'); args=ap.parse_args(); args.output.mkdir(parents=True,exist_ok=False)
    start=time.perf_counter_ns(); dev,producers,consumers,training,fit_checks=fit(); train_ns=time.perf_counter_ns()-start
    # Import new untouched evaluation AFTER fitting: no cases or labels enter fit.
    from evaluation import cases
    held=cases(); assert len(held)==40
    datasets={'development.json':dev,'evaluation.json':held}
    for name,data in datasets.items(): (args.output/name).write_text(json.dumps(data,indent=2)+'\n')
    states={'producer':{f:e7.state(m) for f,m in producers.items()},'consumer':{reg:{f:e7.state(m) for f,m in models.items()} for reg,models in consumers.items()}}
    (args.output/'model-state.json.gz').write_bytes(gzip.compress(e7.dump(states).encode(),mtime=0))
    (args.output/'training.jsonl.gz').write_bytes(gzip.compress(''.join(e7.dump(t)+'\n' for t in training).encode(),mtime=0))
    pre_hashes={str(p.relative_to(REPO)):sha(p.read_bytes()) for p in [ROOT/'run.py',ROOT/'evaluation.py',ROOT/'PROTOCOL.md',ROOT.parent/'e7/run.py',ROOT.parent/'e7/development.py',ROOT.parent/'e7/contract.json',ROOT.parent/'e4-boundary/run.py']}
    rows=[evaluate_case(case,reg,pf,cf,arm,access,orientation,producers,consumers) for case,reg,pf,cf,arm,access,orientation in itertools.product(held,REGIMES,e7.FAMILIES,e7.FAMILIES,e7.ARMS,ACCESS,ORIENTATIONS)]
    assert all(sha((REPO/p).read_bytes())==h for p,h in pre_hashes.items()),'Source changed during evaluation'
    (args.output/'raw.jsonl.gz').write_bytes(gzip.compress(''.join(e7.dump(r)+'\n' for r in rows).encode(),mtime=0))
    summary={'rows':len(rows),'unique_cases':len(held),'groups':aggregate(rows),'manipulation_checks':manipulation_checks(rows),'training_checks':fit_checks,'analysis':causal_analysis(rows)}
    (args.output/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    import joblib,threadpoolctl
    cfg=dict(baseline='bf1003f3fdde28c3d518f661ce45aa8a42c08cdd',preregistration='89970c2c8dc9e2374b056d33d7b47a394af5e7c8',evaluated_commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=REPO,text=True).strip(),evaluation_source_before_after=pre_hashes['experiments/e7-1/evaluation.py'],source_hashes=pre_hashes,python=sys.version,platform=platform.platform(),versions={'sklearn':e7.sklearn.__version__,'numpy':e7.np.__version__,'scipy':e7.scipy.__version__,'joblib':joblib.__version__,'threadpoolctl':threadpoolctl.__version__},threadpools=threadpoolctl.threadpool_info(),seeds={'development':704,'linear_model':704,'decorrelation':[9101,9102],'evaluation':71004},model_families='E7 unchanged: word TFIDF(1,2)/logreg C10 max_iter1000; count(1,1)/NB alpha1',thresholds={'release':.6,'withhold':.4,'producer_label':.5},prompts=None,temperature=None,sampling=None,training_ns=train_ns,model_predictions_evaluation=2*len(rows),network_calls=0,paid_inference=0,training_rows=len(training),masked_paths=[list(p) for p in ASSESSMENT_PATHS],command='python3 experiments/e7-1/run.py',deviations=[],limits='Same-author familiar-cue novelty; null masking OOD; mixed-format consumer training; controlled flips not calibrated uncertainty; exact trusted simulator.')
    (args.output/'configuration.json').write_text(json.dumps(cfg,indent=2)+'\n'); archive(args.output)
    print(json.dumps({'rows':len(rows),'classification':summary['analysis']['pooled_classification'],'checks':summary['manipulation_checks']}))
if __name__=='__main__': main()
