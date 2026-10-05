"""New cases authored after canonical E7.1 protocol 89970c2; never used in fit."""
import random
from pathlib import Path
import importlib.util
spec=importlib.util.spec_from_file_location('dev_cues',Path(__file__).resolve().parent.parent/'e7/development.py')
dev=importlib.util.module_from_spec(spec); spec.loader.exec_module(dev)
def cases():
    rng=random.Random(71004); out=[]
    def add(family,clear,source_extra=None,nested=None,world=None,pair=None):
        source={'reviewer_note':'intake review: release permitted','supporting_note':'','observations':{'target':'artifact-A','digest':'sha256:A','revision':7},'decorative_comment':'independent intake record'}
        source.update(source_extra or {}); source['observations'].update(nested or {})
        out.append(dict(id=f'e71-{family}-{len(out):02}',family=family,clear=clear,source=source,world=world or {},pair=pair))
    for family in ['novel_top','novel_nested']:
        for index in range(6):
            name=rng.choice(['recipient_constraint','distribution_scope','owner_condition','retention_directive','destination_policy'])+'_'+format(rng.getrandbits(24),'06x')
            # Both paired cases retain the same core/source metadata and key.
            for clear in [True,False]:
                clause='secondary directive: '+rng.choice(dev.SAFE if clear else dev.BLOCK)
                add(family,clear,source_extra={name:clause} if family=='novel_top' else None,nested={name:clause} if family=='novel_nested' else None,pair=f'{family}-{index}')
    for index in range(8):
        primary=dev.SAFE[index%4] if index%2==0 else dev.BLOCK[index%4]
        secondary='' if index<4 else dev.BLOCK[(index+1)%4]
        clear=primary in dev.SAFE and not secondary
        add('known_control',clear,source_extra={'reviewer_note':'intake review: '+primary,'supporting_note':secondary})
    faults=[{'revision':6},{'evidence':[]},{'evidence':['e-good','e-conflict']},{'grant':'g-forged'}, {'attempt':'old-attempt','status':'unknown','initial_effect':True,'initial_receipt':True,'recovery':True}, {'attempt':'old-attempt','status':'unknown','initial_effect':True,'recovery':True}, {'attempt':'__unknown_prior_effect__','status':'unknown','initial_effect':True,'recovery':True}, {'schema_version':2}]
    for fault in faults: add('state_fault',True,world=fault)
    return out
