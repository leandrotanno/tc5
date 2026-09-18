"""Dashboard de triagem — lista de alunos ativos ranqueada por risco combinado."""

from pathlib import Path

import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parent.parent
RISCO_PATH = ROOT / "data" / "processed" / "risco_atual.csv"

DRIVER_LABEL = {
    "academico": "Acadêmico",
    "engajamento": "Engajamento",
    "psicossocial": "Psicossocial",
    "psicopedagogico": "Psicopedagógico",
    "contexto": "Contexto",
}

st.set_page_config(page_title="Passos Mágicos — Triagem de risco", layout="wide")


@st.cache_data
def load_risco() -> pd.DataFrame:
    df = pd.read_csv(RISCO_PATH)
    for col in ("driver_defasagem", "driver_evasao"):
        df[col] = df[col].map(DRIVER_LABEL).fillna(df[col])
    df["fase"] = df["fase"].astype("Int64")
    return df


if not RISCO_PATH.exists():
    st.error(
        "data/processed/risco_atual.csv não encontrado. Rode `just score` "
        "(ou `uv run python -m tc5.score`) antes de abrir o dashboard."
    )
    st.stop()

df = load_risco()

st.title("Dashboard de Triagem — Passos Mágicos")
st.caption(
    f"Safra {int(df['ano'].iloc[0])} · {len(df)} alunos ativos · "
    "ranqueados por risco combinado (defasagem + evasão)"
)

with st.sidebar:
    st.header("Filtros")
    fases = sorted(df["fase"].dropna().unique().tolist())
    fase_sel = st.multiselect("Fase", fases, default=fases)
    turma_sel = st.text_input("Turma contém", "")
    risco_min = st.slider("Risco combinado mínimo", 0.0, 1.0, 0.0, 0.05)

filtrado = df[df["fase"].isin(fase_sel) & (df["risco_combinado"] >= risco_min)]
if turma_sel:
    filtrado = filtrado[filtrado["turma"].str.contains(turma_sel, case=False, na=False)]

def fmt_pct(serie: pd.Series) -> str:
    return f"{serie.mean():.0%}" if len(serie) else "—"


col1, col2, col3 = st.columns(3)
col1.metric("Alunos na lista", len(filtrado))
col2.metric("Risco de defasagem médio", fmt_pct(filtrado["risco_defasagem"]))
col3.metric("Risco de evasão médio", fmt_pct(filtrado["risco_evasao"]))

st.subheader("Lista de priorização")
mostrar = filtrado[
    ["ra", "fase", "turma", "pedra", "risco_combinado", "risco_defasagem",
     "driver_defasagem", "risco_evasao", "driver_evasao"]
].sort_values("risco_combinado", ascending=False)

if mostrar.empty:
    st.info("Nenhum aluno com esse filtro. Ajuste a fase, turma ou risco mínimo na barra lateral.")
else:
    st.dataframe(
        mostrar,
        column_config={
            "ra": "RA",
            "fase": st.column_config.NumberColumn("Fase"),
            "turma": "Turma",
            "pedra": "Pedra",
            "risco_combinado": st.column_config.ProgressColumn("Risco combinado", min_value=0, max_value=1),
            "risco_defasagem": st.column_config.ProgressColumn("Risco defasagem", min_value=0, max_value=1),
            "driver_defasagem": "Driver defasagem",
            "risco_evasao": st.column_config.ProgressColumn("Risco evasão", min_value=0, max_value=1),
            "driver_evasao": "Driver evasão",
        },
        hide_index=True,
        use_container_width=True,
    )

    st.download_button(
        "Exportar CSV",
        mostrar.to_csv(index=False).encode("utf-8"),
        file_name="triagem_passos_magicos.csv",
        mime="text/csv",
    )

st.caption(
    "Risco de evasão é sinalizador para priorização humana, não veredito — "
    "o modelo tem sinal mais fraco que o de defasagem (ver notebooks/01_modelagem.ipynb)."
)
