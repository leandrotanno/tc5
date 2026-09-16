# 0001 — Consolidação do painel longitudinal e critério de evasão

## Contexto
As 3 abas (PEDE2022/2023/2024) têm nomes de coluna e tipos inconsistentes.
Precisamos de um painel único por `(ra, ano)` e de dois rótulos de target.

## Decisões

**Colunas duplicadas com uma versão morta**: 2023 tem `INDE 23`/`Pedra 23`
(100% vazias) ao lado de `INDE 2023`/`Pedra 2023` (as reais). Usamos as com
sufixo completo do ano.

**`Idade` corrompida em 2023**: 399 valores pequenos foram convertidos pelo
Excel para data (`8` → `1900-01-08`). Corrigido extraindo o dia do mês.

**`Fase` normalizada para 0 (ALFA) – 8**: formato varia por ano (`3` em 2022,
`"FASE 3"` em 2023, `"7E"`/`"4M"` — fase+turma colada — em 2024). Extraímos o
primeiro dígito da string. Em 2024, 38 linhas têm `Fase=9` e `Turma=9`
simultaneamente — não se encaixa na escala e vira `NaN` (provável aluno sem
classificação ainda). Confirmado: essas mesmas 38 linhas têm `INDE = "INCLUIR"`
(texto, não número) — são registros de 2024 ainda pendentes de fechamento do
ciclo PEDE, não erro de digitação. `inde` é coagido para numérico
(`"INCLUIR"` → `NaN`).

**`Cg`/`Cf`/`Ct`, `Destaque *`, `Indicado`, `Atingiu PV`**: vazias na fonte
para 2023 e 2024 (não é bug da consolidação). Mantidas no painel mesmo assim
— ficam `NaN` fora de 2022.

**Critério de evasão**: `ra` presente no ano `t` e ausente em `t+1` conta
como evasão, **exceto** se o último registro do aluno está em fase máxima
(`fase >= 8`) ou idade de saída (`idade >= 21`) — nesses casos é saída
natural (formatura/idade), não evasão. Threshold escolhido pelo range
observado nos dados (idade máxima na base = 21); não veio de uma regra
oficial do programa — **revisar com a Passos Mágicos se possível**.

Resultado: 256 evasões em 2022→2023 (de 260 ausências brutas) e 245 em
2023→2024 (de 249) — a diferença são as saídas naturais excluídas.

**`piora_defasagem`**: `defasagem(t+1) < defasagem(t)` (defasagem mais
negativa = mais atrasado).

## Validação
Painel resultante: 3030 linhas, 1661 RAs únicos, 468 presentes nos 3 anos —
bate com o diagnóstico do `docs/plano-projeto.md`.
