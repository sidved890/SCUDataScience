from __future__ import annotations

import pandas as pd

from src.config import UCMR_ALL_PATH, ZIP_CODES_PATH


def load_ucmr_results() -> pd.DataFrame:
    return pd.read_csv(UCMR_ALL_PATH, sep="\t", dtype=str, encoding="latin1")


def load_zip_codes() -> pd.DataFrame:
    return pd.read_csv(ZIP_CODES_PATH, sep="\t", dtype=str)
