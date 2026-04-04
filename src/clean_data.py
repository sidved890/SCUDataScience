from __future__ import annotations

import pandas as pd

from src.config import KEY_CONTAMINANTS, UGL_TO_NGL


def _normalize_units(series: pd.Series) -> pd.Series:
    return (
        series.fillna("")
        .str.replace("Â", "", regex=False)
        .str.replace("µ", "u", regex=False)
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
    zip_map = zip_map.loc[:, ["PWSID", "ZIPCode"]].drop_duplicates()
    df = df.merge(zip_map, on="PWSID", how="left")

    df["is_key_contaminant"] = df["Contaminant"].isin(KEY_CONTAMINANTS)
    df["result_ng_L"] = df["AnalyticalResultValue"]
    df["mrl_ng_L"] = df["MRL"]

    ug_mask = df["Units"].eq("ug/L")
    df.loc[ug_mask, "result_ng_L"] = df.loc[ug_mask, "AnalyticalResultValue"] * UGL_TO_NGL
    df.loc[ug_mask, "mrl_ng_L"] = df.loc[ug_mask, "MRL"] * UGL_TO_NGL

    return df


def subset_by_zip(df: pd.DataFrame, zip_code: str) -> pd.DataFrame:
    subset = df[df["ZIPCode"].eq(zip_code)].copy()
    return subset.sort_values(["PWSName", "FacilityName", "CollectionDate", "Contaminant"])
