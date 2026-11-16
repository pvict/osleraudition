# Execução e critérios verificáveis

## Inspeção sem instalação

O pacote já inclui SQLite, esquema SQL, dump e tabelas JSONL. Comece por `dados/exportacao_legivel/resumo_banco.json`, `sessoes_ativas.csv`, `simulados_ativos.json` e `inspecao_servicos_app.json`.

Para abrir o banco com Python:

```python
import sqlite3
from pathlib import Path
db = Path('dados/snapshot_20261116/osler.sqlite3').resolve()
con = sqlite3.connect(db.as_uri() + '?mode=ro', uri=True)
con.execute('PRAGMA query_only=ON')
```

Não importe `cloud_app.py` para auditar os dados locais. Isso solicita configuração online e pode envolver a produção. Não preencha credenciais reais em cópias compartilhadas.

## Reproduzir exportação e integridade

Na raiz extraída:

```text
python scripts/exportar_banco.py
python scripts/verificar_pacote.py
```

O primeiro script só lê o SQLite e gera saídas derivadas; a verificação confere que o original não mudou. O segundo verifica hashes do pacote e os blobs Git de todas as branches. Para gerar uma nova exportação a partir de outro snapshot, use `--db CAMINHO --output PASTA_NOVA`.

## Executar o aplicativo em cópia

Utilize Python 3.13, compatível com a CI capturada. Crie um ambiente virtual, instale `app/requirements.txt` e `pytest`, e use uma pasta de trabalho separada. Copie nela apenas o conteúdo de `dados/snapshot_20261116/` necessário à execução. Configure `OSLER_DATA_DIR` para essa cópia, remova `OSLER_CLOUD` do ambiente e execute `python -m streamlit run app/app.py` a partir da raiz extraída.

Essa é uma execução local de auditoria. Não é restauração do histórico online. Não execute `cloud/schema.sql` ou scripts de criação/alteração de roles durante a leitura do pacote.

Na pasta `app/`, execute `python -m pytest -q`. Para checagens focadas: `python -m unittest tests.test_recovery_quantities tests.test_recurring_questions`. A branch do PR #3 também contém `tests/test_recovery_schedule_dates.py`.

Resultados locais desta preparação estão em `proveniencia/validacao_local.json`. A inspeção dos serviços usa uma cópia descartável e documenta o fallback de fuso local. O fuso de produção não foi alterado.

## Critérios de aceitação a avaliar

- Banco, backup e restauração íntegros; concorrência não perde nem duplica resultados.
- Datas passadas/atuais/futuras e vagas previstas são distinguíveis; datas vencidas não são anunciadas como reagendamento atual.
- Meta diária total não soma revisões externas, áreas e blocos duas vezes.
- Um ou mais dias perdidos mantêm saldo auditável sem dobrar automaticamente a tarefa executável seguinte.
- Descansos e simulados continuam reservados; inviabilidade de cobertura/prazo é exposta.
- Questões novas, conhecidas, revisões, acertos sem convicção e dados importados têm semânticas separadas.
- Doses e prioridades respeitam bancos pequenos e demonstram o efeito dos seus parâmetros.
- Tempo total é estimado com base identificada, variabilidade e coleta dos dados que faltam; cabe no teto de cinco horas.
- Indicadores de evolução distinguem treino dirigido de desempenho em provas inéditas comparáveis.
- A meta de 90% aparece como objetivo e é acompanhada com incerteza; não se converte em probabilidade de aprovação sem modelo validado.
- Seleções de suspensão/manutenção usam desempenho e incidência com fonte; não produzem urgência ou dívida fictícia.
- Uma rotina piloto tem medidas prospectivas de resultado e tolerabilidade, com regras de ajuste; duas semanas não são tratadas como validação de longo prazo.

Só o auditor pode emitir o parecer de prontidão após reproduzir os itens. A existência deste pacote não declara todos os critérios atendidos.
