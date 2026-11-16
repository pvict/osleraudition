"""Confere hashes de arquivos, branches, backup e banco sem conexão externa."""
from pathlib import Path,PurePosixPath
import hashlib,json,sqlite3,sys,zipfile

ROOT=Path(__file__).resolve().parents[1]
def sha(b):return hashlib.sha256(b).hexdigest()
def gitsha(b):return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()

def verify():
    manifest=json.loads((ROOT/'proveniencia/package_manifest.json').read_text(encoding='utf-8'))
    checked=0
    for row in manifest['files']:
        p=ROOT/row['path']
        if not p.is_file() or sha(p.read_bytes())!=row['sha256']:raise ValueError('Arquivo ausente ou divergente: '+row['path'])
        checked+=1
    branches=json.loads((ROOT/'proveniencia/branches.json').read_text(encoding='utf-8'))
    trees=json.loads((ROOT/'proveniencia/all_branch_trees.json').read_text(encoding='utf-8'))
    branch_checks=[]
    for b in branches:
        tree=next(t for t in trees if t['branch']==b['branch'])
        count=0
        for r in tree['tree']['tree']:
            if r['type']!='blob':continue
            p=ROOT/b['folder']/r['path']
            if gitsha(p.read_bytes())!=r['sha']:raise ValueError('Blob Git divergente: '+b['branch']+'/'+r['path'])
            count+=1
        branch_checks.append({'branch':b['branch'],'files':count,'ok':True})
    provenance=json.loads((ROOT/'proveniencia/database_snapshot.json').read_text(encoding='utf-8'))
    backup=ROOT/'dados'/provenance['backup_file']
    if sha(backup.read_bytes())!=provenance['backup_sha256']:raise ValueError('Backup original divergente')
    with zipfile.ZipFile(backup) as z:
        m=json.loads(z.read('manifest.json'))
        for name,row in m['files'].items():
            rel=PurePosixPath(name)
            if rel.is_absolute() or '..' in rel.parts or '\\' in name:raise ValueError('Caminho inválido')
            data=z.read(name)
            if sha(data)!=row['sha256'] or len(data)!=row['size']:raise ValueError('Backup inválido: '+name)
            if sha((ROOT/'dados/snapshot_20261116'/name).read_bytes())!=row['sha256']:raise ValueError('Extração divergente: '+name)
    db=ROOT/'dados/snapshot_20261116/osler.sqlite3'
    with sqlite3.connect(db.resolve().as_uri()+'?mode=ro',uri=True) as c:
        integrity=c.execute('pragma integrity_check').fetchall()
        foreign=c.execute('pragma foreign_key_check').fetchall()
        if integrity!=[('ok',)] or foreign:raise ValueError('Integridade SQLite inválida')
    return {'package_files_verified':checked,'branches':branch_checks,'backup_files_verified':len(m['files']),'database_integrity':'ok','foreign_key_violations':0}

if __name__=='__main__':
    try:print(json.dumps(verify(),ensure_ascii=False,indent=2))
    except Exception as e:
        print('FALHA: '+str(e),file=sys.stderr);raise SystemExit(1)
