-- Opcional. Apenas leitura. Executar somente no projeto correto e em sessão autorizada.
-- Não retorna senhas nem conteúdo dos objetos privados do estudo.
begin read only;
select current_database(),current_user,now() as collected_at;
select schemaname,tablename,tableowner,rowsecurity
from pg_tables where schemaname='osler_private' order by tablename;
select schemaname,tablename,policyname,roles,cmd,qual,with_check
from pg_policies where schemaname='osler_private';
select rolname,rolcanlogin,rolsuper,rolbypassrls
from pg_roles where rolname in ('osler_cloud','anon','authenticated');
select n.nspname,p.proname,p.prosecdef,p.proconfig,p.proacl
from pg_proc p join pg_namespace n on n.oid=p.pronamespace
where n.nspname='public' and p.proname in ('osler_acquire','osler_release','osler_put','osler_get','osler_commit')
order by p.proname;
select id,revision,updated_at,lease_until,
       (select count(*) from jsonb_object_keys(w.manifest)) as current_manifest_files,
       (select count(*) from jsonb_object_keys(w.previous_manifest)) as previous_manifest_files
from osler_private.workspace w;
select count(*) as objects_count,sum(length(content)) as encoded_content_chars
from osler_private.objects;
rollback;
