# Mapa técnico para iniciar a revisão

## Execução e persistência

`app.py` é a entrada local; `cloud_app.py` habilita o modo online e chama `osler/cloud_ui.py`. O modo online usa `CloudWorkspace` (`cloud_store.py`) e `SupabasePostgres` (`cloud_postgres.py`). O banco relacional do estudo é SQLite; no Supabase, o projeto mantém objetos e manifests de snapshots em esquema privado, com funções RPC e controle de lease/revisão.

Portanto, o SQLite anexado é o banco de estudo efetivo exportado pelo app, e não um banco de demonstração. Ele não equivale a um dump administrativo de todo o PostgreSQL. Para o armazenamento, leia também `cloud/schema.sql`, `cloud/README.md`, `cloud_access.py`, `backups.py`, `database_check.py` e `storage.py`.

## Planejamento e mensuração

- `adaptive_service.py`: composição de catálogo, estados, overview, calendário e replanejamento; ponto principal de rastreamento.
- `adaptive_planning.py`, `topic_spacing.py`, `study_models.py`: dose, estados, espaçamento e perfil; conferir fórmulas e limites.
- `study_agenda.py`, `study_calendar.py`, `study_replanning.py`, `study_replanning_ui.py`: reservas, previsões, recuperação e apresentação dos atrasos.
- `recovery.py`, `recurring_questions.py`, `recovery_apply.py`, `recovery_ui.py`: retomada por quantidade, cotas externas, retornos relatados de sete dias e aplicação em estágio/validação.
- `study_dashboard.py`, `bento_day_ui.py`, `study_feedback.py`: contagem apresentada em Hoje; conferir correspondência com a carga efetiva e o que foi feito.
- `exam_goals.py`, módulos de simulados e `exam_practice.py`: provas-alvo, treinos e resultados; manter separação de denominadores e condições de aplicação.
- `error_cards.py`, `error_cards_service.py`, módulos `error_cards_*`: inventário e primeira passagem dos manuais; não tratar como estimativa de retenção FSRS.
- `incidence.py`, `models.py`, classificadores e importadores: fontes, normalização e relação entre bases.
- `evolution_performance.py`, `evolution_spacing.py`, `longitudinal.py`: evolução e cenários; conferir distinção entre medido e projetado.

## Banco

O snapshot contém 30 tabelas. Veja os números exatos e colunas em `dados/exportacao_legivel/resumo_banco.json`.

`reports/records` preservam importações; `study_profiles` é histórico de perfis; `study_events` e `mock_exams` têm versões/ações; `study_plan_runs` agrega vários tipos de eventos JSON. Não some indiscriminadamente todas as linhas de `study_plan_runs`: ali há configurações, cenários, reservas, snapshots e históricos, não apenas estudo executado.

O perfil-base mais recente tem `max_questions=120`, mas a retomada registra sua própria configuração. A carga efetiva precisa passar pelos overrides e reservas. Compare os campos derivados na inspeção dos serviços; não conclua que 120 é necessariamente a meta operacional atual.

## Branches

Os sete snapshots estão listados em `proveniencia/branches.json`. A pasta `app/` corresponde à branch hospedada informada pelo usuário; não se demonstrou nesta preparação o SHA do processo Streamlit efetivamente em execução.

O PR #3 (`https://github.com/pvict/study-optimizer/pull/3`) está aberto e adiciona exposição de datas e classificação de agendamentos vencidos. Sua branch está em `branches/codex__datas-reais-recuperacao-20261115/`. A CI dessa branch passou pelo critério “sem falhas novas”, mas a suíte inteira ainda contém seis falhas anteriores. Não confundir CI verde com suíte totalmente verde.

As outras branches são históricas ou alternativas; leia as diferenças antes de recomendar integrações. Todos os arquivos foram verificados usando os hashes Git de seus respectivos commits.
