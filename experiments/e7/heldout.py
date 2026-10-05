"""Authored only after freeze 9912049. Fixed held-out cases; no schema tuning."""
import random
from development import SAFE,BLOCK
def cases():
    rng=random.Random(17007); out=[]
    def add(family,clear=True,extras=None,nested=None,**world):
        source={'reviewer_note':'signed assessment: release permitted','supporting_note':'','observations':{'target':'artifact-A','digest':'sha256:A','revision':7},'decorative_comment':'routine record'}
        source.update(extras or {}); source['observations'].update(nested or {})
        out.append(dict(id=f'{family}-{len(out):02}',family=family,source=source,clear=clear,world=world))
    for i in range(8):
        clear=i%2==0; add('control',clear,extras={'reviewer_note':'independent assessment: '+rng.choice(SAFE if clear else BLOCK)})
    for i in range(4):
        key=rng.choice(['regional_directive','containment_rule','withdrawn_consent','inspection_window'])+'_'+str(i)
        for clear in (True,False): add('novel_top',clear,extras={key:'new condition: '+rng.choice(SAFE if clear else BLOCK)})
    for i in range(4):
        key=rng.choice(['transport_constraint','owner_instruction','storage_restriction','scope_change'])+'_'+str(i)
        for clear in (True,False): add('novel_nested',clear,nested={key:'new condition: '+rng.choice(SAFE if clear else BLOCK)})
    for i in range(4): add('conflicting_notes',False,extras={'supporting_note':'counter-observation: '+BLOCK[i]})
    for i in range(4):
        clear=i%2==0; add('changed_semantics',clear,extras={'task_meaning_'+str(i):'release means onward redistribution: '+(SAFE[i] if clear else BLOCK[i])})
    faults=[dict(revision=6),dict(evidence=[]),dict(evidence=['e-good','e-conflict']),dict(grant='g-forged'),dict(attempt='old-attempt',status='unknown',initial_effect=True,initial_receipt=True,recovery=True),dict(attempt='old-attempt',status='unknown',initial_effect=True,recovery=True),dict(attempt='__unknown_prior_effect__',status='unknown',initial_effect=True,recovery=True),dict(schema_version=2)]
    for f in faults: add('state_fault',**f)
    return out
