# Datathon Fase 5 — Case Passos Mágicos — Plano de Projeto

## Contexto
Tech Challenge Fase 5 (última fase) do MBA POSTECH FIAP. Trabalho em dupla, mesmo
esquema do TC4 (obesidade). Prazo: **14 dias** a partir de 15/09/2026. Ambiente:
PC próprio, Ubuntu via WSL. Mesma stack do TC4: uv (dependency groups), mise, just,
scikit-learn/XGBoost/Optuna/SHAP, Streamlit Community Cloud para deploy.

## Por que não "mais do mesmo"
Esse datathon é extremamente repetido — dezenas de repositórios públicos no GitHub
resolvem exatamente o enunciado da mesma forma: notebook de EDA, modelo de
classificação (RF/XGBoost) prevendo "risco de defasagem", app Streamlit de
**consulta individual** (digita a matrícula, vê o score), PPT de storytelling
genérico. Um dos mais completos encontrados foi `naruto112/data_analytics_fase5`
(modelo servido por API externa, documentação técnica robusta) — mostra que só
"cumprir o rubric" já tem régua alta.

O ângulo de "app de consulta individual" é passivo: só ajuda se alguém já
suspeitar do aluno e for lá procurar. Numa ONG com equipe pedagógica/psicológica
pequena, isso não muda a rotina de ninguém.

**Diferencial escolhido — dois eixos:**
1. **Modelo de risco de evasão**, além do modelo de defasagem exigido pela Q9.
   Não é pedido no enunciado, mas é exatamente o espaço da Q11 (insights e
   criatividade) — e para a sustentabilidade da ONG, perder um aluno do programa
   é mais grave que uma queda temporária de nota.
2. **Dashboard de triagem operacional**, em vez de app de lookup solitário: lista
   de alunos ativos já ranqueada por risco, com o driver dominante explicado —
   um "quem eu priorizo essa semana" para a equipe, não um brinquedo de consulta.

## Dados disponíveis (diagnóstico já feito)

Arquivo principal: `BASE DE DADOS PEDE 2024 - DATATHON.xlsx`, 3 abas em formato
long (uma linha por aluno-ano):

| Aba | Linhas | Observação |
|---|---|---|
| PEDE2022 | 860 | não tem IPP |
| PEDE2023 | 1.014 | schema mais completo, tem IPP |
| PEDE2024 | 1.156 | schema mais completo ainda, tem campo `Ativo/Inativo` |

As colunas **não são idênticas entre os anos** — precisa homogeneizar antes de
empilhar num painel longitudinal (chave: `RA`).

Pasta `Bases antigas/` (dataset padrão FIAP, formato wide, 2020-2022) é de uma
edição anterior do datathon — **não é a base oficial deste ciclo** (o enunciado
pede 2022-2024), usar só como referência se necessário, não como fonte principal.

Documentação de apoio já lida:
- `Dicionário Dados Datathon.pdf` — dicionário de campos
- `PEDE_ Pontos importantes.docx` — fórmulas oficiais dos indicadores:
  - Defasagem = Fase Efetiva − Fase Ideal
  - IDA = média (nota Matemática, Português, Inglês)
  - IEG = pontuação de tarefas / nº de tarefas
  - IAA = pontuação de autoavaliação / nº de perguntas
  - IPS = pontuação dos avaliadores / nº de avaliadores (psicólogos)
  - IPP = avaliações pedagógicas / nº de avaliações
  - IPV = análise longitudinal (qualitativo, sem fórmula fechada)
- Relatórios anuais de atividades da Passos Mágicos (2020-2023) — bons para
  amarrar o storytelling com a narrativa institucional/de doador

## Achados-chave do diagnóstico de overlap entre anos

```
RAs 2022: 860   2023: 1.014   2024: 1.156
2022 → ausentes em 2023: 260  (candidatos a evasão)
2023 → ausentes em 2024: 249  (candidatos a evasão)
novos em 2023: 414   novos em 2024: 391
presentes nos 3 anos: 468
```

O campo `Ativo/Inativo` da aba 2024 **não serve para nada aqui** — é um snapshot
atual, 100% "Cursando". O sinal de evasão real só existe comparando presença de
RA entre as abas ano a ano.

**Cuidado crítico:** nem toda ausência no ano seguinte é evasão "ruim". Parte
pode ser **saída natural por formatura/idade** (o programa atende até certa
idade/fase). É preciso separar isso olhando idade e fase no último ano em que o
aluno aparece antes de rotular como evasão — senão o modelo vira ruído e a
narrativa perde credibilidade.

## Plano técnico

### 1. Engenharia de dados
- Consolidar PEDE2022/2023/2024 num painel longitudinal por RA
- Homogeneizar schema entre anos (ex.: IPP ausente em 2022)
- Construir os dois rótulos de target:
  - `piora_defasagem`: defasagem aumenta de t para t+1
  - `evasao`: ausência do RA em t+1, **excluindo saída natural por idade/fase**
- Gerar features longitudinais (deltas ano a ano dos indicadores, não só o
  snapshot do ano corrente)

### 2. Dois modelos preditivos
- **Risco de defasagem** (exigido pela Q9 do enunciado)
- **Risco de evasão** (o diferencial, ligado à Q11)
- Ambos com explicabilidade via SHAP, apontando o driver dominante por aluno
  (acadêmico / engajamento / psicossocial / psicopedagógico)
- Notebook único demonstrando: feature engineering → split treino/teste →
  modelagem → avaliação (exigência explícita do enunciado)

### 3. App Streamlit — dashboard de triagem
- Lista de alunos ativos ranqueada por risco combinado (defasagem + evasão)
- Filtro por fase/turma
- Driver dominante exibido por aluno
- Exportação CSV para virar lista de trabalho real da equipe
- Deploy no Streamlit Community Cloud

### 4. Storytelling (perguntas Q1-Q10 do enunciado)
Responder cada pergunta (perfil de IAN, evolução de IDA, relação IEG↔IDA/IPV,
coerência IAA↔desempenho real, padrões IPS antecedendo quedas, IPP vs IAN,
comportamentos que influenciam IPV, combinações de indicadores que elevam INDE,
efetividade do programa por fase Quartzo/Ágata/Ametista/Topázio) amarrando com
os relatórios anuais da associação para dar peso de impacto real, não só
gráfico solto.

## Entregáveis (rubric do enunciado)
- Link do GitHub com os códigos de limpeza e análise
- Apresentação de storytelling em formato gerencial (PPT ou PDF)
- Notebook Python com o modelo preditivo (feature engineering, split,
  modelagem, avaliação)
- App Streamlit deployado no Community Cloud
- Vídeo de até 5 minutos apresentando resultados e storytelling
