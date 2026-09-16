default:
    @just --list

sync:
    uv sync --all-groups

panel:
    uv run python -m tc5.data

score:
    uv run python -m tc5.score

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
