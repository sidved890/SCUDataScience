from __future__ import annotations

import pandas as pd

from src.config import CONTAMINANT_DESCRIPTIONS


def build_source_summary(df: pd.DataFrame) -> pd.DataFrame:
    grouped = (
        df.groupby(
            ["PWSID", "PWSName", "FacilityID", "FacilityName", "FacilityWaterType", "Contaminant"],
            dropna=False,
        )
        .agg(
            ucmr_cycles=("ucmr_cycle", lambda s: ", ".join(sorted(set(x for x in s.dropna())))),
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
    focus = df[df["detected"]].copy()
    latest = (
        focus.sort_values("CollectionDate")
        .groupby(["PWSID", "PWSName", "FacilityName", "Contaminant"], dropna=False)
        .tail(1)
    )
    cols = ["ucmr_cycle", "PWSName", "FacilityName", "CollectionDate", "Contaminant", "result_ng_L"]
    return latest.loc[:, cols].sort_values(["FacilityName", "Contaminant"])


def source_profile(df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for keys, group in df.groupby(["PWSID", "PWSName", "FacilityName", "FacilityWaterType"], dropna=False):
        pwsid, pwsname, facility_name, water_type = keys
        detections = group[group["detected"]]
        rows.append(
            {
                "PWSID": pwsid,
                "PWSName": pwsname,
                "FacilityName": facility_name,
                "FacilityWaterType": water_type,
                "ucmr_cycles": ", ".join(sorted(set(x for x in group["ucmr_cycle"].dropna()))),
                "sample_events": group["SampleID"].nunique(),
                "detected_contaminants": detections["Contaminant"].nunique(),
                "total_detections": int(detections.shape[0]),
                "max_detected_ng_L": round(detections["result_ng_L"].max(), 2) if not detections.empty else 0.0,
                "latest_sample_date": group["CollectionDate"].max(),
            }
        )
    return pd.DataFrame(rows).sort_values(["PWSName", "FacilityName"])


def contaminant_glossary(df: pd.DataFrame) -> pd.DataFrame:
    contaminant_cycles = (
        df.groupby("Contaminant", dropna=False)["ucmr_cycle"]
        .apply(lambda s: ", ".join(sorted(set(x for x in s.dropna()))))
        .reset_index(name="ucmr_cycles")
    )
    contaminant_cycles["description"] = contaminant_cycles["Contaminant"].map(_describe_contaminant)
    return contaminant_cycles.sort_values("Contaminant")


def _describe_contaminant(name: str) -> str:
    if name in CONTAMINANT_DESCRIPTIONS:
        return CONTAMINANT_DESCRIPTIONS[name]
    if name.startswith("PF") or "FTS" in name or "FOSAA" in name or "HFPO" in name or "ADONA" in name:
        return "A PFAS-related compound monitored by EPA as part of unregulated contaminant occurrence testing."
    if "HAA" in name:
        return "A haloacetic acid disinfection byproduct monitored in drinking water systems."
    if "nitroso" in name.lower() or name.upper().startswith("NDMA"):
        return "A nitrosamine-class contaminant monitored because of possible health concerns at low concentrations."
    if name.lower() == "lithium":
        return "A naturally occurring element monitored by EPA in drinking water occurrence studies."
    return "An EPA-monitored unregulated contaminant included in one or more UCMR cycles."
