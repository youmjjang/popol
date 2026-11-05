"""Offline assessment experiment. No real customer data or network services.
Usage: python gigang_portfolio_measure.py --repo PATH --out PATH
"""
import argparse, csv, json, subprocess, sys
from pathlib import Path
from datetime import datetime
from unittest.mock import patch
from contextlib import ExitStack
import importlib

parser=argparse.ArgumentParser()
parser.add_argument('--repo',required=True);parser.add_argument('--out',required=True)
args=parser.parse_args();repo=Path(args.repo).resolve();out=Path(args.out).resolve();out.mkdir(exist_ok=True,parents=True)
sys.path[:0]=[str(repo),str(repo/'tests')]
from test_outbound_scoring import engine,event,matched
from gigang.schemas.event import EventAction

rows=[]
def run_case(id,name,expected,action=EventAction.PASTE_ATTEMPT,target='chatgpt.com',extra=None,setup=None):
    e=engine()
    e.store.db_path = ':memory:'
    e.store.has_user_prior_watch_history = lambda user: False
    for name in ['user_sensitive_db_touch','user_visited_unapproved_ai','user_ai_accesses','pending_db_exports','user_db_counts','_db_touch_noted']:
        if not hasattr(e,name):setattr(e,name,{})
    e.store.get_incident = lambda id: None
    if setup: setup(e)
    ev=event(action,target=target,extra=extra,name='sample.csv' if action==EventAction.FILE_UPLOAD_ATTEMPT else None,size=100)
    with ExitStack() as stack:
        module=importlib.import_module('gigang.engine.correlation')
        stack.enter_context(patch.object(module,'on_risk_state_changed',create=True))
        stack.enter_context(patch.object(module,'notify_high',create=True))
        e.update_user_risk(ev)
    observed=e.store.risk['state']=='HIGH'
    inc=e.store.incidents[-1] if e.store.incidents else None
    rows.append({'id':id,'scenario':name,'expected_high':expected,'observed_high':observed,
                 'state':e.store.risk['state'],'event_score':inc.score if inc else 0,
                 'pass':observed==expected,'input':extra or {}})

# Ten explicit content-match input fixtures. Match generation is outside this experiment.
risks=[('주민번호 1건',{'rrn_high':1}),('주민번호 3건',{'rrn_high':3}),
       ('주민번호 10건',{'rrn_high':10}),('주민번호 30건',{'rrn_high':30}),
       ('이메일 1건',{'email':1}),('전화번호 3건',{'phone':3}),
       ('계좌번호 3건',{'account':3}),('카드번호 3건',{'card':3}),
       ('복합 항목',{'email':3,'phone':3}),('검사 건수 없음',{})]
for i,(name,hits) in enumerate(risks,1):
    action=EventAction.FILE_UPLOAD_ATTEMPT if i%2==0 else EventAction.PASTE_ATTEMPT
    run_case('R%02d'%i,'미승인 외부 '+('첨부' if i%2==0 else '입력')+' · 내용 일치 · '+name,True,action,extra=matched(hits))

run_case('C01','일반 외부 붙여넣기 · 연결 근거 없음',False)
run_case('C02','일반 외부 첨부 · 연결 근거 없음',False,EventAction.FILE_UPLOAD_ATTEMPT)
run_case('C03','사내 사이트 입력',False,target='intranet.example')
run_case('C04','사내 사이트 첨부',False,EventAction.FILE_UPLOAD_ATTEMPT,target='intranet.example')
run_case('C05','승인 목적지 · 내용 일치',False,extra=matched({'rrn_high':3}),setup=lambda e:e.policy.update(approved_outbound_domains=['chatgpt.com']))
run_case('C06','승인 하위 도메인 · 내용 일치',False,target='sub.chatgpt.com',extra=matched({'rrn_high':3}),setup=lambda e:e.policy.update(approved_outbound_domains=['chatgpt.com']))
run_case('C07','복사 글자 수만 동일',False,extra={'text_length':200},setup=lambda e:e.user_db_copies.update(audit=[{'time':datetime.utcnow(),'length':200,'source':'desktop-oli.tail2bbbea.ts.net'}]))
run_case('C08','첨부 이름·크기만 동일',False,EventAction.FILE_UPLOAD_ATTEMPT,setup=lambda e:e.user_db_downloads.update(audit=[{'name':'sample.csv','size':100,'source':'desktop-oli.tail2bbbea.ts.net','time':datetime.utcnow()}]))
run_case('C09','내용 일치 신호의 출처가 회사 원본과 다름',False,extra={'match_status':'matched','match':{'source_domain':'other.example'},'pattern_hits':{'rrn_high':3}})
run_case('C10','민감도 건수만 존재 · 자료 연결 없음',False,extra={'pattern_hits':{'rrn_high':30}})

tp=sum(r['expected_high'] and r['observed_high'] for r in rows)
fn=sum(r['expected_high'] and not r['observed_high'] for r in rows)
fp=sum(not r['expected_high'] and r['observed_high'] for r in rows)
tn=sum(not r['expected_high'] and not r['observed_high'] for r in rows)
report={'commit':(repo/'SOURCE_COMMIT.txt').read_text().strip() if (repo/'SOURCE_COMMIT.txt').exists() else subprocess.check_output(['git','rev-parse','HEAD'],cwd=repo,text=True).strip(),
        'scope':'Offline risk-classification fixtures; content matching supplied as input; memory store; notification mocked. No browser, API, DB, OCR or enforcement measurement.',
        'cases':len(rows),'passed':sum(r['pass'] for r in rows),'tp':tp,'fn':fn,'fp':fp,'tn':tn,'rows':rows}
(out/'scenario_results.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
with (out/'scenario_results.csv').open('w',encoding='utf-8-sig',newline='') as f:
    writer=csv.DictWriter(f,fieldnames=[k for k in rows[0] if k!='input']);writer.writeheader()
    writer.writerows({k:v for k,v in row.items() if k!='input'} for row in rows)
print(json.dumps({k:v for k,v in report.items() if k!='rows'},ensure_ascii=False))
