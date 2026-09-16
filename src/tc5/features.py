"""Feature engineering sobre o painel longitudinal: snapshot do ano + deltas vs. ano anterior."""

import numpy as np
import pandas as pd

SNAPSHOT_COLS = [
    "inde", "iaa", "ieg", "ips", "ipp", "ida", "ipv", "ian",
    "nota_mat", "nota_port", "nota_ing", "defasagem", "fase", "idade",
]
DELTA_SOURCE_COLS = ["inde", "iaa", "ieg", "ips", "ipp", "ida", "ipv", "ian", "defasagem"]


def _with_deltas(panel: pd.DataFrame) -> pd.DataFrame:
    df = panel.sort_values(["ra", "ano"]).copy()
    grp = df.groupby("ra")

    for col in DELTA_SOURCE_COLS:
        anterior = grp[col].shift(1)
        ano_anterior = grp["ano"].shift(1)
        tem_anterior = ano_anterior == (df["ano"] - 1)
        df[f"delta_{col}"] = np.where(tem_anterior, df[col] - anterior, np.nan)

    df["tempo_pm"] = df["ano"] - df["ano_ingresso"]
    return df


def build_features(panel: pd.DataFrame) -> pd.DataFrame:
    """Uma linha por (ra, ano) com target válido: snapshot do ano t + delta (t vs t-1)."""
    df = _with_deltas(panel)
    keep = (
        ["ra", "ano", "genero", "tempo_pm"]
        + SNAPSHOT_COLS
        + [f"delta_{c}" for c in DELTA_SOURCE_COLS]
        + ["piora_defasagem", "evasao"]
    )
    feats = df[keep].copy()
    return feats[feats["piora_defasagem"].notna() | feats["evasao"].notna()].reset_index(drop=True)


def build_inference_features(panel: pd.DataFrame, ano: int) -> pd.DataFrame:
    """Snapshot + delta do `ano` mais recente, sem exigir target — para escorar a safra ativa."""
    df = _with_deltas(panel)
    df = df[df["ano"] == ano]
    keep = (
        ["ra", "ano", "turma", "pedra", "genero", "tempo_pm"]
        + SNAPSHOT_COLS
        + [f"delta_{c}" for c in DELTA_SOURCE_COLS]
    )
    return df[keep].reset_index(drop=True)


def main():
    panel = pd.read_csv("data/processed/panel_longitudinal.csv")
    feats = build_features(panel)
    feats.to_csv("data/processed/features.csv", index=False)
    print(f"features: {len(feats)} linhas, {feats.shape[1]} colunas")
    print("nulos por coluna (%):")
    print((feats.isna().mean() * 100).round(1).sort_values(ascending=False).head(12))
    print("\ntargets:")
    print("piora_defasagem:", feats["piora_defasagem"].value_counts(dropna=False).to_dict())
    print("evasao:", feats["evasao"].value_counts(dropna=False).to_dict())


if __name__ == "__main__":
    main()
