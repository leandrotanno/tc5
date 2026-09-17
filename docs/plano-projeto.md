# Datathon Fase 5 — Case Passos Mágicos

Tech Challenge Fase 5 do MBA POSTECH FIAP, em dupla. Case: dados do PEDE
(Pesquisa Extensiva do Desenvolvimento Educacional) da Passos Mágicos, 2022 a 2024.

## O ângulo

Esse datathon é repetido — tem dezenas de repositórios no GitHub resolvendo o
enunciado do mesmo jeito: EDA, um modelo de defasagem, um app Streamlit de
consulta individual (digita a matrícula, vê o score), PPT genérico. Um dos
mais completos que achei foi o `naruto112/data_analytics_fase5` (modelo
servido por API, documentação técnica boa) — mostra que só cumprir o rubric
já é régua alta, não dá pra competir nisso.

O problema do app de consulta é que ele é passivo: só ajuda se alguém já
suspeitar do aluno e for lá conferir. Numa ONG com equipe pedagógica pequena,
isso não muda a rotina de ninguém.

Por isso o projeto vai em duas frentes que o enunciado não pede diretamente:

- Modelo de risco de **evasão**, além do modelo de defasagem da Q9. Entra no
  espaço da Q11 (insights e criatividade), e pra sustentabilidade da ONG
  perder um aluno do programa pesa mais que uma queda pontual de nota.
- Um **dashboard de triagem**, não um app de lookup: lista de alunos ativos
  já ranqueada por risco, com o driver dominante explicado — o "quem eu
  priorizo essa semana" da equipe, em vez de um brinquedo de consulta.

## Os dados

`BASE DE DADOS PEDE 2024 - DATATHON.xlsx`, 3 abas em formato long (uma linha
por aluno-ano):

| Aba | Linhas | Observação |
|---|---|---|
| PEDE2022 | 860 | sem IPP |
| PEDE2023 | 1.014 | schema mais completo, com IPP |
| PEDE2024 | 1.156 | schema mais completo ainda, tem `Ativo/Inativo` |

As colunas não são idênticas entre os anos — precisa homogeneizar antes de
empilhar num painel longitudinal (chave: `RA`).

A pasta `Bases antigas/` (dataset padrão FIAP, formato wide, 2020-2022) é de
uma edição anterior do datathon, não é a base oficial deste ciclo (o
enunciado pede 2022-2024) — usar só como referência se precisar, não como
fonte principal.

Documentação de apoio: o dicionário de dados, e o documento com as fórmulas
oficiais dos indicadores —

- Defasagem = Fase Efetiva − Fase Ideal
- IDA = média (nota Matemática, Português, Inglês)
- IEG = pontuação de tarefas / nº de tarefas
- IAA = pontuação de autoavaliação / nº de perguntas
- IPS = pontuação dos avaliadores / nº de avaliadores (psicólogos)
- IPP = avaliações pedagógicas / nº de avaliações
- IPV = análise longitudinal, qualitativo, sem fórmula fechada

Os relatórios anuais da Passos Mágicos (2020-2023) ajudam a amarrar o
storytelling com a narrativa institucional/de doador.

### Overlap entre anos

```
RAs 2022: 860   2023: 1.014   2024: 1.156
2022 → ausentes em 2023: 260  (candidatos a evasão)
2023 → ausentes em 2024: 249  (candidatos a evasão)
novos em 2023: 414   novos em 2024: 391
presentes nos 3 anos: 468
```

O campo `Ativo/Inativo` de 2024 não serve pra nada aqui — é um snapshot
atual, 100% "Cursando". O sinal de evasão só existe comparando presença de
RA entre as abas, ano a ano.

Cuidado: nem toda ausência no ano seguinte é evasão. Parte pode ser saída
natural por formatura ou idade (o programa atende até certa idade/fase).
Precisa olhar idade e fase no último ano em que o aluno aparece antes de
rotular como evasão, senão o modelo vira ruído e a narrativa perde
credibilidade.

## Plano técnico

**Engenharia de dados.** Consolidar as 3 abas num painel longitudinal por
RA, homogeneizando schema entre anos. Dois rótulos de target: `piora_defasagem`
(defasagem piora de t pra t+1) e `evasao` (ausência do RA em t+1, excluindo
saída natural por idade/fase). Features longitudinais — deltas ano a ano dos
indicadores, não só o snapshot do ano corrente.

**Dois modelos preditivos**, defasagem (Q9) e evasão (o diferencial, Q11),
ambos com explicabilidade via SHAP apontando o driver dominante por aluno
(acadêmico / engajamento / psicossocial / psicopedagógico). Notebook único
demonstrando feature engineering, split treino/teste, modelagem e avaliação
— exigência explícita do enunciado.

**Dashboard Streamlit de triagem**: lista de alunos ativos ranqueada por
risco combinado (defasagem + evasão), filtro por fase/turma, driver
dominante por aluno, exportação CSV pra virar lista de trabalho real da
equipe. Deploy no Streamlit Community Cloud.

**Storytelling**, respondendo as perguntas 1-10 do enunciado (texto literal
em `docs/fontes/enunciado-datathon.md`) e usando a 11 (insights e
criatividade) pra apresentar o modelo de evasão e o dashboard de triagem.
Amarrar com os relatórios anuais da associação pra dar peso de impacto
real, não só gráfico solto.

## Entregáveis

- Link do GitHub com os códigos de limpeza e análise
- Apresentação de storytelling em formato gerencial (PPT ou PDF)
- Notebook Python com o modelo preditivo (feature engineering, split,
  modelagem, avaliação)
- App Streamlit deployado no Community Cloud
- Vídeo de até 5 minutos apresentando resultados e storytelling
