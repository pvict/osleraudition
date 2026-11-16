# Contexto confirmado e propostas ainda não validadas

## Usuário e objetivo

Paulo Victor está concluindo Medicina e pretende dedicar mais um ano à preparação para residência. Objetivo declarado: alcançar 90% de acertos e usar o app como principal organizador/monitor. A data-base do perfil é 30/11/2027; datas e cortes de instituições no banco são registros do usuário, não editais futuros verificados nesta preparação.

O limite atual confirmado é **cinco horas diárias no total**, incluindo resolução, correção, revisões e pausas. O usuário relatou exaustão, frustração com acúmulo e receio de piorar desempenho. Isso é contexto de planejamento, não diagnóstico clínico.

## Quantidades e diferenças de modalidade

- Questões: referência desejada de pelo menos 80/dia. A contagem inclui revisões externas de questões, blocos do app e treinos por área; dias de simulado devem ser tratados como atividade própria.
- Prontos da Osler: capacidade declarada de 550/dia, exclusivamente os prontos. Não confundir com manuais.
- Manuais: inventário enviado de 8.525 cards em 319 decks; referência de 50/dia e preferência por decks inteiros. Não é declaração de 8.525 atrasados. O app não controla o FSRS da plataforma.
- Questões externas: uma captura inicial mostrou 294 pendentes, 184 atrasadas. É uma observação datada anterior ao snapshot atual, não uma consulta atual à plataforma.
- Regra externa de questões relatada: erros e acertos sem convicção retornam em sete dias após resposta. Isso não é a regra FSRS dos flashcards.

## O que foi observado na plataforma Osler em 16/11

As capturas enviadas pelo usuário mostraram 17.835 revisões em 30 dias e 19.167 em 33 dias. Com teto desejado de 550, o equilíbrio em 45 e 60 dias apresentou o mesmo resultado: 874 cards remanejáveis e 1.169 preservados nas datas por limite do algoritmo; os picos continuavam acima de 550. A igualdade dessas duas prévias não demonstra impossibilidade global de qualquer outra configuração.

Na redistribuição de 148 pendentes, a interface declara que o campo “por dia” **se soma ao que já está agendado**. Não é um teto global. Foram discutidos 10/dia para essa parcela; não há confirmação suficiente de aplicação de todas as recomendações feitas na conversa.

As configurações mostradas eram: prontos normais 85%, HY 90%, máximo 182 dias; manuais normais 90%, HY 94%, máximo 182 dias. A interface diz que ajustes só afetam as próximas revisões. Foi sugerido reduzir HY pronto para 85%, mas a gravação dessa sugestão não foi confirmada. Use os valores como última observação enviada, não estado consultado ao vivo.

O filtro HY/não-HY não resolve sozinho a seleção pelo desempenho. O usuário se opôs a suspender sem dados; não presumir que ele aplicou suspensões por esses filtros.

## Propostas versus decisões

A conversa propôs priorizar questões, manuais de erros e reduzir os prontos dirigindo-os a dificuldades reais. Um quadro de cinco horas foi sugerido: 2h resolução, 1h correção, 30min manuais, 30min prontos, 1h pausas/margem. **Esse quadro não foi validado por tempo observado nem consolidado como configuração aceita.** O usuário manifestou medo de queda de desempenho. O pedido atual é justamente auditoria independente antes de confiar no app como ferramenta principal.

As propostas anteriores de teto de 100 prontos e suspensão ampla foram inadequadas à capacidade depois declarada pelo usuário e foram revistas. Não as use como requisitos.

## Separação dos sistemas

O Study Optimizer é código do usuário, hospedado em Streamlit com persistência Supabase. A plataforma comercial Osler é um sistema externo. Um ajuste no banco do Optimizer não modifica o algoritmo ou as datas internas dos flashcards da Osler. O pacote não contém o código nem o histórico individual completo do FSRS da plataforma comercial.
