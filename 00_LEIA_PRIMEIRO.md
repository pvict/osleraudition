# Osler Study Optimizer — pacote de auditoria para Claude

Preparado em 16/11/2026. Objetivo: examinar se o aplicativo pode ser a ferramenta principal de planejamento e acompanhamento de Paulo Victor rumo à meta de **90% de acertos em provas de residência**, dentro de uma rotina sustentável. Meta de nota, retenção de flashcards e probabilidade de aprovação são conceitos diferentes.

## O que foi reunido

- `app/`: os 454 arquivos da branch usada pelo Streamlit, `codex/cloud-mobile-20261109`, no commit `3881882696119b32532f7232801c7832e25cbbb7`. Cada arquivo foi conferido pelo hash Git do servidor.
- `branches/`: cópias completas das outras seis branches encontradas no GitHub, também conferidas por hash. As versões são alternativas/históricas, não módulos adicionais do app.
- `dados/snapshot_20261116/`: banco SQLite, originais e exportações extraídos do backup atual, com os 62 arquivos verificados contra o manifesto.
- `dados/osler_20261116T155835Z_4372b8322e37efc6.zip`: backup original, preservado byte a byte.
- `dados/exportacao_legivel/`: esquema SQL, dump, todas as tabelas em JSONL, sessões e simulados ativos, resumo e inspeção dos serviços do app.
- `proveniencia/`: commits, manifests, status do PR e evidências de testes.
- `contexto/`: decisões do usuário, limitações e inventário dos decks manuais.
- `scripts/`: ferramentas de leitura/verificação, sem conexão com a produção.

O banco foi exportado do app online em **16/11/2026, 12h58min34s de Brasília** (15h58 UTC). É uma fotografia desse momento. Não é uma conexão viva com o Supabase e não contém automaticamente o estado interno da plataforma Osler.

## Como entregar ao Claude

1. Descompacte o ZIP em uma pasta nova.
2. Se estiver usando Claude com acesso a arquivos locais/Claude Code, abra essa pasta como projeto e use `01_PROMPT_PARA_CLAUDE.md` como primeira mensagem.
3. Peça que comece por este documento, pelo contexto e pelos resumos do banco; depois leia os módulos apontados no mapa técnico. Não precisa consumir todas as branches de uma vez.
4. Se estiver usando apenas uma conversa web sem ferramentas de arquivos, envie primeiro o prompt e os documentos `00` a `06`, os resumos JSON e `sessoes_ativas.csv`. O código completo e o SQLite exigem capacidade de abrir arquivos ou uma análise em lotes; um resumo sozinho não permite afirmar que o aplicativo inteiro foi auditado.

## Escopo e limites da preparação

Não foram alterados resultados de estudo, datas do banco de produção, credenciais, deploy ou branches remotas. O pacote contém dados pessoais de estudo: use-o privadamente e não publique a pasta `dados/` em repositório público.

Não foram coletadas senhas do Streamlit/Supabase nem feita automação da plataforma Osler. A estrutura PostgreSQL esperada está em `app/cloud/schema.sql`; papéis, políticas e funções efetivamente instalados no Supabase precisam de verificação separada. Há um roteiro SQL somente de leitura em `scripts/auditoria_supabase_somente_leitura.sql`.

Há uma correção no **PR #3 ainda aberto**, presente somente na branch `codex/datas-reais-recuperacao-20261115`: mostra datas reais de recuperação e deixa de considerar uma reserva vencida como uma nova data válida. Avalie-a separadamente; não a trate como publicada.

## Ordem sugerida de leitura

1. `01_PROMPT_PARA_CLAUDE.md` e `contexto/02_CONTEXTO_USUARIO.md`.
2. `dados/exportacao_legivel/resumo_banco.json` e `inspecao_servicos_app.json`.
3. `03_MAPA_TECNICO.md`, `04_PONTOS_CRITICOS.md`, `05_REFERENCIAS_VERIFICADAS.md`.
4. Código e testes da branch principal do pacote; então diferenças relevantes das outras branches.
5. `06_EXECUCAO_E_ACEITACAO.md` e testes de reprodução dos achados.

Os resumos desta preparação ajudam a localizar problemas; não são um laudo independente de eficácia ou aprovação.
