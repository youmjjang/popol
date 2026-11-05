"""Recalculate a shared-rule versus per-group-rule comparison from 48 result rows.
Usage: python http_compare.py --input original_48.csv --out results
This does not generate logs or rerun a detector.
"""
import argparse,csv,json,hashlib
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--input',required=True);p.add_argument('--out',required=True)
a=p.parse_args();src=Path(a.input);out=Path(a.out);out.mkdir(parents=True,exist_ok=True)
rows=list(csv.DictReader(src.open(encoding='utf-8-sig')))
for r in rows:
    for k in ['시간구간(초)','임계값(회)','TP','FP','FN','TN']:r[k]=int(r[k])
    assert r['TP']+r['FN']==200 and r['FP']+r['TN']==200
assert len(rows)==48
def metrics(rs):
    d={k:sum(r[k] for r in rs) for k in ['TP','FP','FN','TN']}
    d.update(precision=d['TP']/(d['TP']+d['FP']) if d['TP']+d['FP'] else 0,
             recall=d['TP']/(d['TP']+d['FN']),fpr=d['FP']/(d['FP']+d['TN']),
             f1=2*d['TP']/(2*d['TP']+d['FP']+d['FN']))
    return d
shared=[]
for w in [30,60,120]:
    for t in [3,5,8,12]:
        rs=[r for r in rows if r['시간구간(초)']==w and r['임계값(회)']==t]
        assert len(rs)==4
        shared.append(dict(window=w,threshold=t,**metrics(rs)))
common=max(shared,key=lambda r:(r['f1'],-r['FP'],-r['window']))
selected=[]
for group in dict.fromkeys(r['유형'] for r in rows):
    candidates=[r for r in rows if r['유형']==group]
    selected.append(max(candidates,key=lambda r:(metrics([r])['f1'],-r['FP'],-r['시간구간(초)'])))
typed=metrics(selected)
report={'source_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),
        'method':'Reaggregation of historical synthetic experiment; best pooled-F1 common rule vs per-group F1 selections on the same data. No holdout set.',
        'shared_candidates':shared,'shared':common,'per_group':typed,'selected':selected,
        'fp_reduction_pct':100*(common['FP']-typed['FP'])/common['FP']}
(out/'comparison.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
with (out/'comparison.csv').open('w',encoding='utf-8-sig',newline='') as f:
    rs=[dict(method='shared',**{k:common[k] for k in typed}),dict(method='per_group',**typed)]
    w=csv.DictWriter(f,fieldnames=list(rs[0]));w.writeheader();w.writerows(rs)
print(json.dumps({'shared':common,'per_group':typed,'fp_reduction_pct':report['fp_reduction_pct']}))
