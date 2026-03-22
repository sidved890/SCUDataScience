from __future__ import annotations

import pandas as pd

from src.config import BENCHMARK_PWSIDS, KEY_CONTAMINANTS, TARGET_PWSIDS


def build_source_summary(df: pd.DataFrame) -> pd.DataFrame:
    focus = df[df["Contaminant"].isin(KEY_CONTAMINANTS)].copy()
    grouped = (
        focus.groupby(["PWSID", "PWSName", "FacilityID", "FacilityName", "FacilityWaterType", "Contaminant"], dropna=False)
        .agg(
            sample_events=("SampleID", "nunique"),
            detections=("detected", "sum"),
            latest_date=("CollectionDate", "max"),
            max_result_ng_L=("result_ng_L", "max"),
            avg_detected_ng_L=("result_ng_L", lambda s: s.dropna().mean()),
        )
        .reset_index()
    )
    grouped["avg_detected_ng_L"] = grouped["avg_detected_ng_L"].round(2)
    grouped["max_result_ng_L"] = grouped["max_result_ng_L"].round(2)
    return grouped.sort_values(["PWSName", "FacilityName", "Contaminant"])


def latest_detected_values(df: pd.DataFrame) -> pd.DataFrame:
    focus = df[(df["Contaminant"].isin(KEY_CONTAMINANTS)) & (df["detected"])].copy()
    latest = (
        focus.sort_values("CollectionDate")
        .groupby(["PWSID", "PWSName", "FacilityName", "Contaminant"], dropna=False)
        .tail(1)
    )
    cols = ["PWSName", "FacilityName", "CollectionDate", "Contaminant", "result_ng_L"]
    return latest.loc[:, cols].sort_values(["FacilityName", "Contaminant"])


def source_profile(df: pd.DataFrame) -> pd.DataFrame:
    focus = df[df["Contaminant"].isin(KEY_CONTAMINANTS)].copy()
    rows = []
    for keys, group in focus.groupby(["PWSID", "PWSName", "FacilityName", "FacilityWaterType"], dropna=False):
        pwsid, pwsname, facility_name, water_type = keys
        detections = group[group["detected"]]
        rows.append(
            {
                "PWSID": pwsid,
                "PWSName": pwsname,
                "FacilityName": facility_name,
                "FacilityWaterType": water_type,
                "sample_events": group["SampleID"].nunique(),
                "detected_contaminants": detections["Contaminant"].nunique(),
                "total_detections": int(detections.shape[0]),
                "max_detected_ng_L": round(detections["result_ng_L"].max(), 2) if not detections.empty else 0.0,
                "latest_sample_date": group["CollectionDate"].max(),
            }
        )
    return pd.DataFrame(rows).sort_values(["PWSID", "FacilityName"])


def benchmark_subset(df: pd.DataFrame) -> pd.DataFrame:
    return df[df["PWSID"].isin(TARGET_PWSIDS | BENCHMARK_PWSIDS)].copy()
