from __future__ import annotations

import pandas as pd

from src.config import KEY_CONTAMINANTS, TARGET_PWSIDS, TARGET_ZIPS, UGL_TO_NGL


def _normalize_units(series: pd.Series) -> pd.Series:
    return (
        series.fillna("")
        .str.replace("Â", "", regex=False)
        .str.replace("µ", "u", regex=False)
        .str.replace("ug/L", "ug/L", regex=False)
        .str.strip()
    )


def clean_ucmr_data(results_df: pd.DataFrame, zip_df: pd.DataFrame) -> pd.DataFrame:
    df = results_df.copy()
    df["CollectionDate"] = pd.to_datetime(df["CollectionDate"], errors="coerce")
    df["AnalyticalResultValue"] = pd.to_numeric(df["AnalyticalResultValue"], errors="coerce")
    df["MRL"] = pd.to_numeric(df["MRL"], errors="coerce")
    df["Units"] = _normalize_units(df["Units"])
    df["detected"] = df["AnalyticalResultsSign"].eq("=") & df["AnalyticalResultValue"].notna()

    zip_map = zip_df.rename(columns={"ZIPCODE": "ZIPCode"}).copy()
    zip_map["ZIPCode"] = zip_map["ZIPCode"].astype(str)
    df = df.merge(zip_map, on="PWSID", how="left")

    df["is_target_zip"] = df["ZIPCode"].isin(TARGET_ZIPS)
    df["is_target_system"] = df["PWSID"].isin(TARGET_PWSIDS)
    df["is_key_contaminant"] = df["Contaminant"].isin(KEY_CONTAMINANTS)

    df["result_ng_L"] = df["AnalyticalResultValue"]
    df["mrl_ng_L"] = df["MRL"]

    ug_mask = df["Units"].eq("ug/L")
    df.loc[ug_mask, "result_ng_L"] = df.loc[ug_mask, "AnalyticalResultValue"] * UGL_TO_NGL
    df.loc[ug_mask, "mrl_ng_L"] = df.loc[ug_mask, "MRL"] * UGL_TO_NGL

    return df


def pleasanton_subset(df: pd.DataFrame) -> pd.DataFrame:
    mask = df["PWSID"].isin(TARGET_PWSIDS) | df["is_target_zip"]
    subset = df.loc[mask].copy()
    subset = subset.sort_values(["FacilityName", "CollectionDate", "Contaminant"])
    return subset
