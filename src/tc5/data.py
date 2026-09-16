"""Consolidação do painel longitudinal PEDE 2022-2024 a partir da planilha bruta."""

import datetime
import re

import numpy as np
import pandas as pd

RAW_PATH = "data/raw/base_pede_2022_2024.xlsx"

# Nome da coluna em cada aba -> nome comum no painel consolidado.
# Colunas de avaliador/recomendação individuais (Avaliador1..6, Rec Av1..4) e
# Escola/Ativo-Inativo (2024) ficam fora: variam de formato ano a ano e não
# carregam sinal usável para os modelos (ver docs/decisions/0001).
COLUMN_MAPS = {
    2022: {
        "RA": "ra", "Fase": "fase_raw", "Turma": "turma", "Idade 22": "idade_raw",
        "Gênero": "genero", "Ano ingresso": "ano_ingresso",
        "Instituição de ensino": "instituicao_ensino", "Pedra 22": "pedra",
        "INDE 22": "inde", "Cg": "cg", "Cf": "cf", "Ct": "ct",
        "IAA": "iaa", "IEG": "ieg", "IPS": "ips", "IDA": "ida",
        "Matem": "nota_mat", "Portug": "nota_port", "Inglês": "nota_ing",
        "Indicado": "indicado", "Atingiu PV": "atingiu_pv", "IPV": "ipv", "IAN": "ian",
        "Defas": "defasagem", "Destaque IEG": "destaque_ieg",
        "Destaque IDA": "destaque_ida", "Destaque IPV": "destaque_ipv",
    },
    2023: {
        "RA": "ra", "Fase": "fase_raw", "Turma": "turma", "Idade": "idade_raw",
        "Gênero": "genero", "Ano ingresso": "ano_ingresso",
        "Instituição de ensino": "instituicao_ensino", "Pedra 2023": "pedra",
        "INDE 2023": "inde", "Cg": "cg", "Cf": "cf", "Ct": "ct",
        "IAA": "iaa", "IEG": "ieg", "IPS": "ips", "IPP": "ipp", "IDA": "ida",
        "Mat": "nota_mat", "Por": "nota_port", "Ing": "nota_ing",
        "Indicado": "indicado", "Atingiu PV": "atingiu_pv", "IPV": "ipv", "IAN": "ian",
        "Defasagem": "defasagem", "Destaque IEG": "destaque_ieg",
        "Destaque IDA": "destaque_ida", "Destaque IPV": "destaque_ipv",
    },
    2024: {
        "RA": "ra", "Fase": "fase_raw", "Turma": "turma", "Idade": "idade_raw",
        "Gênero": "genero", "Ano ingresso": "ano_ingresso",
        "Instituição de ensino": "instituicao_ensino", "Pedra 2024": "pedra",
        "INDE 2024": "inde", "Cg": "cg", "Cf": "cf", "Ct": "ct",
        "IAA": "iaa", "IEG": "ieg", "IPS": "ips", "IPP": "ipp", "IDA": "ida",
        "Mat": "nota_mat", "Por": "nota_port", "Ing": "nota_ing",
        "Indicado": "indicado", "Atingiu PV": "atingiu_pv", "IPV": "ipv", "IAN": "ian",
        "Defasagem": "defasagem", "Destaque IEG": "destaque_ieg",
        "Destaque IDA": "destaque_ida", "Destaque IPV": "destaque_ipv",
    },
}

FASE_RE = re.compile(r"(\d+)")
GENERO_MAP = {"Feminino": "F", "Menina": "F", "Masculino": "M", "Menino": "M"}


def _parse_idade(value):
    """2023 tem idades pequenas corrompidas em data pelo Excel (8 -> 1900-01-08)."""
    if isinstance(value, (pd.Timestamp, datetime.datetime, datetime.date)):
        return value.day
    if pd.isna(value):
        return np.nan
    return float(value)


def _parse_fase(value):
    """Normaliza Fase para 0 (ALFA) .. 8. Fora dessa faixa (ex.: '9'/'9' em 2024) vira NaN."""
    if pd.isna(value):
        return np.nan
    if isinstance(value, str):
        s = value.strip().upper()
        if s == "ALFA":
            return 0
        m = FASE_RE.search(s)
        if not m:
            return np.nan
        n = int(m.group(1))
        return n if 0 <= n <= 8 else np.nan
    n = int(value)
    return n if 0 <= n <= 8 else np.nan


def load_year(ano: int, path: str = RAW_PATH) -> pd.DataFrame:
    sheet = f"PEDE{ano}"
    colmap = COLUMN_MAPS[ano]
    df = pd.read_excel(path, sheet_name=sheet)
    df = df[list(colmap.keys())].rename(columns=colmap)
    df["idade"] = df["idade_raw"].apply(_parse_idade)
    df["fase"] = df["fase_raw"].apply(_parse_fase)
    df = df.drop(columns=["idade_raw", "fase_raw"])
    df["inde"] = pd.to_numeric(df["inde"], errors="coerce")
    df["genero"] = df["genero"].map(GENERO_MAP)
    df["ano"] = ano
    df["ra"] = df["ra"].astype(str)
    return df


def build_panel(path: str = RAW_PATH) -> pd.DataFrame:
    """Empilha 2022/2023/2024 num painel longitudinal por (ra, ano)."""
    anos = [load_year(a, path) for a in (2022, 2023, 2024)]
    panel = pd.concat(anos, ignore_index=True, sort=False)
    return panel.sort_values(["ra", "ano"]).reset_index(drop=True)


def add_targets(panel: pd.DataFrame, idade_saida: int = 21, fase_saida: int = 8) -> pd.DataFrame:
    """Adiciona piora_defasagem e evasao (t -> t+1) por RA.

    evasao exclui saída natural: aluno cujo último registro está na fase/idade
    de saída do programa (ver docs/decisions/0001-criterio-evasao.md).
    """
    df = panel.copy()
    df = df.sort_values(["ra", "ano"])
    grp = df.groupby("ra")

    df["defasagem_prox"] = grp["defasagem"].shift(-1)
    df["ano_prox"] = grp["ano"].shift(-1)
    tem_prox = df["ano_prox"] == (df["ano"] + 1)

    df["piora_defasagem"] = np.where(
        tem_prox, (df["defasagem_prox"] < df["defasagem"]).astype("Int64"), pd.NA
    )

    ultimo_ano_ra = grp["ano"].transform("max")
    e_ultimo_registro = df["ano"] == ultimo_ano_ra
    nao_e_2024 = df["ano"] < 2024
    saida_natural = (df["fase"] >= fase_saida) | (df["idade"] >= idade_saida)

    df["evasao"] = pd.NA
    evade_mask = nao_e_2024 & e_ultimo_registro
    df.loc[evade_mask, "evasao"] = (~saida_natural[evade_mask]).astype("Int64")
    df.loc[nao_e_2024 & ~e_ultimo_registro, "evasao"] = 0

    return df.drop(columns=["defasagem_prox", "ano_prox"])


def main():
    panel = build_panel()
    panel = add_targets(panel)
    panel.to_csv("data/processed/panel_longitudinal.csv", index=False)
    print(f"painel: {len(panel)} linhas, {panel['ra'].nunique()} RAs únicos")
    print(panel.groupby("ano").size())
    print("evasao por ano (excl. saída natural):")
    print(panel[panel["evasao"].notna()].groupby("ano")["evasao"].agg(["sum", "count"]))


if __name__ == "__main__":
    main()
