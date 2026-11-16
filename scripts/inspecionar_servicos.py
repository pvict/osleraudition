"""Reproduz a inspeção em cópia temporária, sem acessar Supabase ou produção."""
from pathlib import Path
from datetime import timezone,timedelta
from contextlib import nullcontext
from unittest.mock import patch
from zoneinfo import ZoneInfo,ZoneInfoNotFoundError
import argparse,hashlib,json,shutil,sys,tempfile

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'app'))
from osler.storage import Repository
from osler.adaptive_service import AdaptiveService

def inspect(database,as_of):
    original=hashlib.sha256(database.read_bytes()).hexdigest()
    try:ZoneInfo('America/Sao_Paulo');fallback=False
    except ZoneInfoNotFoundError:fallback=True
    with tempfile.TemporaryDirectory(prefix='osler-audit-') as temp:
        stage=Path(temp);shutil.copy2(database,stage/'osler.sqlite3')
        context=patch('osler.planner_service.ZoneInfo',return_value=timezone(timedelta(hours=-3))) if fallback else nullcontext()
        with context:
            service=AdaptiveService(Repository(stage))
            view=service.overview(as_of)
            replanning=service.replanning(as_of,view=view)
            bookings=replanning['rows'];backlog=replanning['backlog'];plan=view['plan']
            report={'as_of':as_of,'timezone_workaround':'UTC-03 somente na inspeção por falta de tzdata' if fallback else None,
                'execution':'Cópia temporária; não registra estudo nem acessa Supabase.',
                'profile_max_questions':view['profile'].get('max_questions'),'plan_target_questions':plan.get('target_questions'),
                'plan_questions':plan.get('questions'),'plan_done_questions':plan.get('done_questions'),
                'planning_states':len(view['planning_states']),'pending_recovery_topics':len(backlog),
                'unfinished_saved_bookings':len(bookings),'bookings_with_past_date':sum(r['date']<as_of for r in bookings),
                'backlog_without_booking_on_or_after_as_of':sum(not any(b['topic_id']==r['topic_id'] and b['date']>=as_of for b in bookings) for r in backlog),
                'quantity_recovery':view['agenda'].get('quantity_recovery'),
                'topic_bookings':[{'topic_id':r['topic_id'],'path':r['path'],'questions':r['questions'],
                    'original_due':r['original_due'],'saved_recovery_dates':[b['date'] for b in bookings if b['topic_id']==r['topic_id']]} for r in backlog]}
    if hashlib.sha256(database.read_bytes()).hexdigest()!=original:raise RuntimeError('Banco original foi alterado')
    return report

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--db',type=Path,default=ROOT/'dados/snapshot_20261116/osler.sqlite3')
    p.add_argument('--as-of',default='2026-11-16')
    p.add_argument('--output',type=Path,default=ROOT/'dados/exportacao_legivel/inspecao_servicos_app.json')
    args=p.parse_args();report=inspect(args.db,args.as_of)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(report,ensure_ascii=False,indent=2,default=str),encoding='utf-8')
    print(json.dumps({k:v for k,v in report.items() if k not in {'quantity_recovery','topic_bookings'}},ensure_ascii=False,indent=2))
