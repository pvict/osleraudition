# Perguntas críticas e evidências iniciais

Este documento orienta a auditoria; não substitui a reprodução pelo Claude.

## 1. Viabilidade conjunta das metas

Cinco horas são 300 minutos totais. Uma conta de 550 prontos pode consumir 45,8 minutos se cada resposta levar 5 segundos; 91,7 minutos a 10 segundos; 137,5 a 15 segundos; 183,3 a 20 segundos. Esses ritmos são **cenários aritméticos**, não o ritmo observado do usuário. Ainda faltam manuais, resolução, correção e pausas.

No snapshot há 43 blocos ativos de questões e **41 não têm minutos registrados**. Não há dados suficientes nesses registros para certificar que a composição atual cabe no tempo. Estime duração apenas com observações disponíveis, explicite amostra/variabilidade e proponha a coleta mínima do que falta.

## 2. O que o desempenho disponível permite concluir

Há 754 respostas e 556 acertos nos blocos ativos registrados: cerca de 73,74% descritivos. Isso não representa a nota atual esperada numa prova. Os temas são escolhidos, há modos distintos e não há identificação individual de questões para comprovar independência ou primeira exposição. Verifique simulados separadamente, com condições, tamanho e exposição declarados.

O registro mais recente de bloco está em 11/11/2026; isso descreve o que foi registrado, não prova que o usuário não estudou depois. Tabelas vazias de erros/avaliações semanais não comprovam ausência de erros ou de revisão.

## 3. Acúmulo, reserva e data

Reproduza um dia perdido e dois dias perdidos. O saldo pode continuar existente, mas a meta executável seguinte não deve dobrar automaticamente. O app precisa mostrar simultaneamente capacidade, saldo e atraso residual, sem marcar recuperação como concluída.

Na versão publicada do pacote, o resumo antigo conta reservas com saldo sem filtrar data vencida. O PR #3 ajusta a apresentação. Investigue também se uma data salva efetivamente obtém vaga dentro da carga, pois data e encaixe no calendário são condições diferentes.

**Contraprova importante no snapshot atual:** a inspeção em cópia encontrou 36 temas atrasados, 47 reservas com saldo, **zero reservas com data passada** e um tema atrasado sem reserva para hoje ou depois. Portanto, a falha potencial do contador não demonstra que os 35 temas vistos antes estavam sem data. O resultado atual indica que 35 dos 36 têm alguma reserva atual/futura; falta verificar a exibição e o efetivo encaixe. Não repita conclusões anteriores da conversa sem confrontar os dados.

A mesma inspeção retorna perfil-base de 120 questões, meta operacional do app de 50 e 47 questões em blocos do dia, com reservas externas compondo a carga total. Confira a composição detalhada em `inspecao_servicos_app.json` antes de interpretar a diferença como defeito. O limite de cinco horas foi declarado depois das configurações presentes no perfil e precisa ser confrontado com as regras atuais de planejamento por quantidade.

## 4. Gargalo semanal

Um teto de 550 em seis dias oferece 3.300 revisões por semana, média de 471,4 por dia de calendário. Compare isso com entradas futuras, reaprendizado e falhas, e com o tempo reservado às questões. “Reequilibrar” não elimina o volume total nem a geração de novas obrigações.

Exija testes com dia de descanso, simulado, plantão, retorno após pausa e deck manual grande. Uma estratégia pode ser inviável na carga disponível; o app deve declarar a falta de vagas sem inventar capacidade.

## 5. Inferências e ciência

Uma meta de 90% deve ser acompanhada em questões inéditas e simulados representativos. Estudar prioritariamente pontos fracos pode diminuir a taxa bruta de acerto enquanto o aprendizado melhora. Revisões de questões conhecidas também podem inflar acertos. Compare conjuntos adequados e reporte limites.

Retenção desejada FSRS não é acerto em prova. A redução de um parâmetro pode espaçar revisões futuras sem alterar vencimentos já criados. A documentação do Anki serve para o Anki; confirme separadamente o comportamento da Osler, cuja tela informa efeito apenas futuro.

A literatura sustenta princípios de recuperação/espaçamento, mas não valida automaticamente as fórmulas específicas do app, a dose de cada tema, pesos de prioridade ou o teto de 550. Classifique parâmetros sem dados de validação como heurísticas.

## 6. Limitações de engenharia já conhecidas

A CI histórica que contém a recorrência de sete dias registra **1.169 testes aprovados, seis falhas e 11 ignorados**. A CI do PR #3 registra **1.173 aprovados, as mesmas seis falhas e 11 ignorados**. Fontes e trechos estão em `proveniencia/`.

Falhas explícitas:

- `tests.test_backups::test_transient_windows_folder_lock_does_not_lose_restoration`.
- `tests.test_balanced_ui::test_strategy_ui_requires_preview_and_can_show_saved_changes`.
- `tests.test_coverage_inclusion::test_small_positive_bank_receives_real_slot_without_inventing_questions`, quatro combinações: `[1-adaptive-balanced_v2]`, `[1-fixed-balanced_v2]`, `[9-adaptive-balanced_v2]`, `[9-fixed-balanced_v2]`.

A hipótese anterior de diferença Windows/Linux ou índice de UI desatualizado não substitui diagnóstico. Reproduza e classifique impacto. Há uma sétima falha de ambiente na base usada para comparação (`test_seed_refuses_existing_folder_and_destination_outside_system_temp`), ausente na execução do head; a preparação não a classifica como correção deliberada.

Uma verificação local atual do código de `app/` rodou 24 testes de retomada/recorrência: 23 passaram e um teste Streamlit foi ignorado por falta da dependência local. Isso não é uma execução nova da suíte completa do commit publicado.

## 7. Escopo da coleta

O pacote não contém: histórico individual completo dos flashcards prontos na Osler, tempos completos de revisão, todas as identidades das questões resolvidas, nem snapshot administrativo do PostgreSQL. Relatos/capturas foram separados dos dados do Optimizer. Recomendações de suspensão ou uma probabilidade de aprovação dependem de dados que podem estar faltando.
