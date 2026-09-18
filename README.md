# TC5 — Datathon Passos Mágicos

Tech Challenge Fase 5 (POSTECH FIAP MBA) — case Passos Mágicos. Contexto e
decisões em [docs/plano-projeto.md](docs/plano-projeto.md) e
[docs/decisions/](docs/decisions/). Enunciado literal em
[docs/fontes/enunciado-datathon.md](docs/fontes/enunciado-datathon.md).

## Rodando do zero

```
mise install       # python 3.12 + just
just sync          # cria .venv e instala as dependências
just rebuild        # painel -> features -> treina os 2 modelos -> score da safra atual
just app            # dashboard Streamlit, local
```

`just rebuild` roda em sequência (também disponíveis soltos, ver `justfile`):

1. `just panel` — consolida `data/raw/base_pede_2022_2024.xlsx` (3 abas,
   2022-2024) num painel longitudinal único (`src/tc5/data.py`)
2. `just features` — snapshot + deltas ano a ano (`src/tc5/features.py`)
3. `just train` — executa `notebooks/01_modelagem.ipynb` (split temporal,
   XGBoost, SHAP), salva os `.joblib` em `data/processed/`
4. `just score` — aplica os modelos treinados na safra ativa mais recente
   (`src/tc5/score.py`), gera `data/processed/risco_atual.csv`

Todos os arquivos gerados por esses passos ficam em `data/processed/` e são
regeneráveis — não versionados, exceto `risco_atual.csv` (o dashboard
depende dele direto; ver abaixo).

## Estrutura

- `data/raw/` — planilha original (`base_pede_2022_2024.xlsx`, abas 2022/2023/2024)
- `data/processed/` — gerado por `just rebuild`. Só `risco_atual.csv` fica
  versionado, porque é o que o dashboard lê em produção — sem ele, o app
  não sobe com dado nenhum antes de alguém rodar o pipeline
- `notebooks/01_modelagem.ipynb` — modelagem: feature engineering, split
  treino/teste, XGBoost, avaliação, SHAP (pergunta 9 do enunciado)
- `notebooks/02_eda_desempenho.ipynb`, `03_eda_psicossocial.ipynb` — EDA e
  storytelling das demais perguntas (1-8, 10)
- `src/tc5/` — código reutilizável: consolidação (`data.py`), features
  (`features.py`), explicabilidade SHAP (`explain.py`), score da safra
  atual (`score.py`)
- `app/dashboard.py` — dashboard Streamlit de triagem
- `docs/fontes/` — dicionário de dados e enunciado oficial
- `docs/decisions/` — decisões de modelagem (critério de evasão, achado do
  IPS sem sinal preditivo, etc.)
