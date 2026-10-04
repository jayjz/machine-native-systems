"""Development-only data/specification. No held-out cases are imported here."""
import itertools, random
SAFE=('release permitted','release allowed','release approved','release clear')
BLOCK=('release blocked','release forbidden','release denied','release unsafe')
KNOWN=('reviewer_note','supporting_note')
def development():
    rng=random.Random(704); rows=[]
    for i,(primary,secondary) in enumerate(itertools.product(SAFE+BLOCK,('',)+SAFE+BLOCK)):
        for prefix in ('review: ','review record: ','assessment: '):
            source={'reviewer_note':prefix+primary,'supporting_note':secondary,'observations':{'target':'artifact-A','digest':'sha256:A','revision':7},'decorative_comment':rng.choice(['artifact review','release meeting','routine record'])}
            rows.append({'id':f'dev-{len(rows)}','source':source,'clear':primary in SAFE and (not secondary or secondary in SAFE)})
    return rows
