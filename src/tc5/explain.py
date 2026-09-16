"""Agrupamento de features em eixos pedagógicos para explicabilidade via SHAP."""

import pandas as pd
import shap

AXES = {
    "academico": ["ida", "nota_mat", "nota_port", "nota_ing", "defasagem", "fase", "ian", "inde",
                  "delta_ida", "delta_defasagem", "delta_ian", "delta_inde"],
    "engajamento": ["ieg", "iaa", "delta_ieg", "delta_iaa"],
    "psicossocial": ["ips", "delta_ips"],
    "psicopedagogico": ["ipp", "ipv", "delta_ipp", "delta_ipv"],
    "contexto": ["genero", "tempo_pm", "idade"],
}


def driver_dominante(model, X: pd.DataFrame) -> pd.DataFrame:
    """Para cada linha, soma |SHAP| por eixo pedagógico e retorna o eixo dominante."""
    explainer = shap.TreeExplainer(model)
    shap_vals = explainer(X, check_additivity=False).values
    shap_df = pd.DataFrame(shap_vals, columns=X.columns, index=X.index)
    axis_abs = pd.DataFrame(
        {axis: shap_df[cols].abs().sum(axis=1) for axis, cols in AXES.items()}
    )
    return pd.DataFrame({
        "driver_dominante": axis_abs.idxmax(axis=1),
        "driver_shap_abs": axis_abs.max(axis=1),
    }, index=X.index)
