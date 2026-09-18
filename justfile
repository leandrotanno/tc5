default:
    @just --list

sync:
    uv sync --all-groups

panel:
    uv run python -m tc5.data

features:
    uv run python -m tc5.features

train:
    uv run --group dev jupyter nbconvert --to notebook --execute --inplace notebooks/01_modelagem.ipynb

score:
    uv run python -m tc5.score

rebuild: panel features train score
    @echo "painel, features, modelos e score regenerados em data/processed/"

lab:
    uv run --group dev jupyter lab

app:
    uv run streamlit run app/dashboard.py

lint:
    uv run --group dev ruff check .

fmt:
    uv run --group dev ruff format .

test:
    uv run --group dev pytest
