from __future__ import annotations

import pandas as pd

from src.config import DEFAULT_UNKNOWN_CONTAMINANT_WEIGHT, RISK_LABELS, RISK_WEIGHT_MAP


def score_sources(df: pd.DataFrame) -> pd.DataFrame:
    focus = df.copy()
    scored_rows = []

    for keys, group in focus.groupby(["PWSID", "PWSName", "FacilityName", "FacilityWaterType"], dropna=False):
        pwsid, pwsname, facility_name, water_type = keys
        score = 0.0
        detected = group[group["detected"]]

        for contaminant, sub in group.groupby("Contaminant"):
            weight = RISK_WEIGHT_MAP.get(contaminant, DEFAULT_UNKNOWN_CONTAMINANT_WEIGHT)
            detections = int(sub["detected"].sum())
            max_value = sub.loc[sub["detected"], "result_ng_L"].max() if detections else 0.0
            score += detections * weight
            score += min(float(max_value or 0.0) / 10.0, 8.0)

        label = _label_for_score(score)
        scored_rows.append(
            {
                "PWSID": pwsid,
                "PWSName": pwsname,
                "FacilityName": facility_name,
                "FacilityWaterType": water_type,
                "risk_score": round(score, 2),
                "risk_label": label,
                "detected_contaminants": detected["Contaminant"].nunique(),
                "max_detected_ng_L": round(detected["result_ng_L"].max(), 2) if not detected.empty else 0.0,
                "sample_events": group["SampleID"].nunique(),
            }
        )

    return pd.DataFrame(scored_rows).sort_values("risk_score", ascending=False)


def _label_for_score(score: float) -> str:
    label = RISK_LABELS[0][1]
    for threshold, candidate in RISK_LABELS:
        if score >= threshold:
            label = candidate
    return label
