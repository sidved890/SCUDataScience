from __future__ import annotations

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from src.config import KEY_CONTAMINANTS


def _empty_figure(title: str):
    fig = go.Figure()
    fig.update_layout(
        title=title,
        xaxis={"visible": False},
        yaxis={"visible": False},
        annotations=[
            {
                "text": "No data available for the current filters.",
                "xref": "paper",
                "yref": "paper",
                "showarrow": False,
                "font": {"size": 16},
            }
        ],
    )
    return fig


def max_concentration_chart(summary_df: pd.DataFrame, contaminants: list[str], title: str):
    focus = summary_df[summary_df["Contaminant"].isin(contaminants)].copy()
    if focus.empty:
        return _empty_figure(title)
    fig = px.bar(
        focus,
        x="FacilityName",
        y="max_result_ng_L",
        color="Contaminant",
        barmode="group",
        title=title,
        labels={"max_result_ng_L": "Concentration (ng/L)", "FacilityName": "Water Source"},
    )
    fig.update_layout(legend_title_text="Contaminant")
    return fig


def trend_chart(df: pd.DataFrame, contaminants: list[str], title: str, detected_only: bool):
    focus = df[df["Contaminant"].isin(contaminants)].copy()
    if detected_only:
        focus = focus[focus["detected"]]
    if focus.empty:
        return _empty_figure(title)
    fig = px.line(
        focus,
        x="CollectionDate",
        y="result_ng_L",
        color="FacilityName",
        line_dash="Contaminant",
        markers=True,
        title=title,
        labels={"result_ng_L": "Detected concentration (ng/L)", "CollectionDate": "Sample date"},
    )
    return fig


def heatmap_chart(summary_df: pd.DataFrame, contaminants: list[str], title: str):
    pivot = (
        summary_df[summary_df["Contaminant"].isin(contaminants)]
        .pivot_table(
            index="FacilityName",
            columns="Contaminant",
            values="max_result_ng_L",
            aggfunc="max",
            fill_value=0.0,
        )
        .reset_index()
    )
    if pivot.empty:
        return _empty_figure(title)
    melted = pivot.melt(id_vars="FacilityName", var_name="Contaminant", value_name="max_result_ng_L")
    fig = px.density_heatmap(
        melted,
        x="Contaminant",
        y="FacilityName",
        z="max_result_ng_L",
        text_auto=".1f",
        color_continuous_scale="YlOrRd",
        title=title,
        labels={"max_result_ng_L": "Max concentration (ng/L)"},
    )
    return fig
