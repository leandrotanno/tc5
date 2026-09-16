"""Escora a safra ativa (ano mais recente do painel) com os modelos treinados."""

import joblib
import pandas as pd

from tc5.explain import driver_dominante
from tc5.features import build_inference_features

ANO_ATUAL = 2024
DISPLAY_COLS = ["ra", "ano", "turma", "pedra", "fase", "idade"]


def score_safra_atual() -> pd.DataFrame:
    panel = pd.read_csv("data/processed/panel_longitudinal.csv")
    feats = build_inference_features(panel, ano=ANO_ATUAL)
    feats["genero"] = feats["genero"].astype("category")

    model_cols = [c for c in feats.columns if c not in ("ra", "ano", "turma", "pedra")]
    X = feats[model_cols]

    model_defasagem = joblib.load("data/processed/model_defasagem.joblib")
    model_evasao = joblib.load("data/processed/model_evasao.joblib")

    out = feats[DISPLAY_COLS].copy()
    out["risco_defasagem"] = model_defasagem.predict_proba(X)[:, 1]
    out["driver_defasagem"] = driver_dominante(model_defasagem, X)["driver_dominante"].values
    out["risco_evasao"] = model_evasao.predict_proba(X)[:, 1]
    out["driver_evasao"] = driver_dominante(model_evasao, X)["driver_dominante"].values
    out["risco_combinado"] = (out["risco_defasagem"] + out["risco_evasao"]) / 2
    return out.sort_values("risco_combinado", ascending=False).reset_index(drop=True)


def main():
    out = score_safra_atual()
    out.to_csv("data/processed/risco_atual.csv", index=False)
    print(f"{len(out)} alunos escorados (safra {ANO_ATUAL})")
    print(out.head(10))


if __name__ == "__main__":
    main()
