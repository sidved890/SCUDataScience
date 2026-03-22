from __future__ import annotations

import pandas as pd
import plotly.express as px

from src.config import KEY_CONTAMINANTS


def max_concentration_chart(summary_df: pd.DataFrame):
    focus = summary_df[summary_df["Contaminant"].isin(["PFOS", "PFOA", "PFHxS"])].copy()
    fig = px.bar(
        focus,
        x="FacilityName",
        y="max_result_ng_L",
        color="Contaminant",
        barmode="group",
        title="Maximum Pleasanton PFAS Concentrations by Source",
        labels={"max_result_ng_L": "Concentration (ng/L)", "FacilityName": "Water Source"},
    )
    fig.update_layout(legend_title_text="Contaminant")
    return fig


def trend_chart(df: pd.DataFrame):
    focus = df[(df["Contaminant"].isin(["PFOS", "PFOA", "PFHxS"])) & (df["detected"])].copy()
    fig = px.line(
        focus,
        x="CollectionDate",
        y="result_ng_L",
        color="FacilityName",
        line_dash="Contaminant",
        markers=True,
        title="Pleasanton PFAS Trends Across Sample Events",
        labels={"result_ng_L": "Detected concentration (ng/L)", "CollectionDate": "Sample date"},
    )
    return fig


def heatmap_chart(summary_df: pd.DataFrame):
    pivot = (
        summary_df[summary_df["Contaminant"].isin(KEY_CONTAMINANTS)]
        .pivot_table(
            index="FacilityName",
            columns="Contaminant",
            values="max_result_ng_L",
            aggfunc="max",
            fill_value=0.0,
        )
        .reset_index()
    )
    melted = pivot.melt(id_vars="FacilityName", var_name="Contaminant", value_name="max_result_ng_L")
    fig = px.density_heatmap(
        melted,
        x="Contaminant",
        y="FacilityName",
        z="max_result_ng_L",
        text_auto=".1f",
        color_continuous_scale="YlOrRd",
        title="Pleasanton Source-by-Contaminant Heatmap",
        labels={"max_result_ng_L": "Max concentration (ng/L)"},
    )
    return fig
