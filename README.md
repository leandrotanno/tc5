# TC5 — Datathon Passos Mágicos

Tech Challenge Fase 5 (POSTECH FIAP MBA) — case Passos Mágicos. Plano completo em
[docs/plano-projeto.md](docs/plano-projeto.md).

## Setup

```
mise install
just sync
just lab
```

## Estrutura

- `data/raw/` — planilha original (`base_pede_2022_2024.xlsx`, abas 2022/2023/2024)
- `data/processed/` — painel longitudinal consolidado (gerado, não versionado)
- `notebooks/` — EDA, engenharia de dados, modelagem
- `src/tc5/` — código reutilizável (carregamento, features, modelos)
- `app/` — dashboard Streamlit de triagem
- `docs/fontes/` — dicionário de dados e documento de fórmulas oficiais
- `docs/decisions/` — decisões de modelagem (ex.: critério de evasão vs. saída natural)
