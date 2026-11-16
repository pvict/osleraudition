"""Exportação reproduzível, exclusivamente de leitura, de uma cópia SQLite."""
from pathlib import Path
from collections import Counter
import argparse,csv,hashlib,json,sqlite3

ROOT=Path(__file__).resolve().parents[1]

def quoted(name):return '"'+name.replace('"','""')+'"'

def latest(rows,key):
    selected={}
    for row in rows:
        if key not in row:continue
        previous=selected.get(row[key])
        if previous is None or (row.get('version',0),row.get('id',0))>(previous.get('version',0),previous.get('id',0)):
            selected[row[key]]=row
    return [r for r in selected.values() if r.get('action')=='save']

def decoded(row):
    return {**row,'payload':json.loads(row['payload'])} if 'payload' in row else row

def export(database,destination):
    database=database.resolve();destination=destination.resolve()
    original=hashlib.sha256(database.read_bytes()).hexdigest()
    destination.mkdir(parents=True,exist_ok=True)
    (destination/'tabelas_jsonl').mkdir(exist_ok=True)
    with sqlite3.connect(database.as_uri()+'?mode=ro',uri=True) as con:
        con.row_factory=sqlite3.Row
        con.execute('pragma query_only=on')
        integrity=[tuple(r) for r in con.execute('pragma integrity_check')]
        foreign=[tuple(r) for r in con.execute('pragma foreign_key_check')]
        if integrity!=[('ok',)] or foreign:raise ValueError('Falha de integridade')
        schema=[dict(r) for r in con.execute("select type,name,tbl_name,sql from sqlite_master where sql is not null order by type,name")]
        (destination/'schema.sql').write_text('\n\n'.join(r['sql']+';' for r in schema),encoding='utf-8')
        tables={};allrows={};invalid=[]
        for table, in con.execute("select name from sqlite_master where type='table' order by name"):
            rows=[dict(r) for r in con.execute('select * from '+quoted(table))]
            tables[table]={'rows':len(rows),'columns':[dict(r) for r in con.execute('pragma table_info('+quoted(table)+')')]}
            allrows[table]=rows
            with (destination/'tabelas_jsonl'/(table+'.jsonl')).open('w',encoding='utf-8',newline='\n') as out:
                for row in rows:
                    out.write(json.dumps(row,ensure_ascii=False)+'\n')
                    for key in ['payload','details','config','snapshot']:
                        if key in row and row[key] is not None:
                            try:json.loads(row[key])
                            except (json.JSONDecodeError,TypeError):invalid.append({'table':table,'id':row.get('id'),'field':key})
        events=latest(allrows.get('study_events',[]),'session_id')
        sessions=[decoded(r) for r in events]
        mocks=[decoded(r) for r in latest(allrows.get('mock_exams',[]),'exam_key')]
        plans=[decoded(r) for r in allrows.get('study_plan_runs',[])]
        kinds=Counter(r['payload'].get('kind','unknown') for r in plans)
        settings=[r for r in plans if r['payload'].get('kind')=='recovery.quantity.settings']
        profiles=allrows.get('study_profiles',[])
        profile=decoded(max(profiles,key=lambda r:r['id'])) if profiles else None
        blocks=[r for r in sessions if r['payload'].get('kind')=='bloco']
        q=sum(r['payload'].get('questions',0) or 0 for r in blocks)
        correct=sum(r['payload'].get('correct',0) or 0 for r in blocks)
        conf=[r for r in blocks if r['payload'].get('confident_correct') is not None]
        summary={'database_sha256':original,'integrity':integrity,'foreign_key_violations':foreign,'tables':tables,
            'invalid_json_fields':invalid,'study_event_rows':len(allrows.get('study_events',[])),
            'active_study_sessions':len(sessions),'active_question_blocks':len(blocks),
            'recorded_block_questions':q,'recorded_block_correct':correct,
            'descriptive_block_accuracy':correct/q if q else None,
            'accuracy_warning':'Descritivo dos blocos registrados; mistura seleção dirigida e possivelmente repetições. Não estima nota em prova nem aprovação.',
            'blocks_with_confidence_recorded':len(conf),'blocks_without_minutes':sum(r['payload'].get('minutes') is None for r in blocks),
            'last_recorded_block_day':max((r['payload']['day'] for r in blocks),default=None),
            'active_mock_exam_records':len(mocks),'mock_conditions':dict(Counter(str(r['payload'].get('conditions')) for r in mocks)),
            'latest_study_profile':profile,'latest_quantity_recovery_settings':max(settings,key=lambda r:r['id']) if settings else None,
            'plan_record_kinds':dict(kinds),'item_level_question_identity_available':False}
        (destination/'resumo_banco.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8')
        (destination/'sessoes_ativas.json').write_text(json.dumps(sessions,ensure_ascii=False,indent=2),encoding='utf-8')
        (destination/'simulados_ativos.json').write_text(json.dumps(mocks,ensure_ascii=False,indent=2),encoding='utf-8')
        fields=['session_id','day','kind','mode','path','questions','correct','confident_correct','minutes','cards_created','source']
        with (destination/'sessoes_ativas.csv').open('w',encoding='utf-8-sig',newline='') as out:
            writer=csv.DictWriter(out,fieldnames=fields);writer.writeheader()
            for r in sessions:
                item={**r['payload'],'session_id':r['session_id']}
                item['path']=' > '.join(item.get('path',[]))
                writer.writerow({k:item.get(k) for k in fields})
        with (destination/'banco_dump.sql').open('w',encoding='utf-8',newline='\n') as out:
            for line in con.iterdump():out.write(line+'\n')
    if hashlib.sha256(database.read_bytes()).hexdigest()!=original:raise RuntimeError('A cópia original foi modificada')
    return {k:summary[k] for k in ['active_study_sessions','active_question_blocks','recorded_block_questions','recorded_block_correct','blocks_without_minutes','last_recorded_block_day','active_mock_exam_records']}

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--db',type=Path,default=ROOT/'dados/snapshot_20261116/osler.sqlite3')
    parser.add_argument('--output',type=Path,default=ROOT/'dados/exportacao_legivel')
    args=parser.parse_args()
    print(json.dumps(export(args.db,args.output),ensure_ascii=False,indent=2))
