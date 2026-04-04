from __future__ import annotations

import zipfile
from pathlib import Path

import pandas as pd

from src.config import RESULT_COLUMNS, UCMR_RESULT_SOURCES, ZIP_COLUMNS


def _read_delimited(source_path: Path, inner: str | None, columns: list[str]) -> pd.DataFrame:
    if inner is None:
        return pd.read_csv(source_path, sep="\t", dtype=str, encoding="latin1", usecols=lambda c: c in columns)

    with zipfile.ZipFile(source_path) as zf:
        with zf.open(inner) as handle:
            return pd.read_csv(handle, sep="\t", dtype=str, encoding="latin1", usecols=lambda c: c in columns)


def load_ucmr_results() -> pd.DataFrame:
    frames: list[pd.DataFrame] = []
    for source in UCMR_RESULT_SOURCES:
        frame = _read_delimited(source["path"], source["inner"], RESULT_COLUMNS)
        frame["ucmr_cycle"] = source["cycle"]
        frames.append(frame)
    return pd.concat(frames, ignore_index=True)


def load_zip_codes() -> pd.DataFrame:
    frames: list[pd.DataFrame] = []
    for source in UCMR_RESULT_SOURCES:
        zip_map = source["zip_map"]
        if zip_map is None:
            continue
        if isinstance(zip_map, Path):
            frame = pd.read_csv(zip_map, sep="\t", dtype=str, usecols=lambda c: c in ZIP_COLUMNS)
        else:
            frame = _read_delimited(source["path"], zip_map, ZIP_COLUMNS)
        frame["ucmr_cycle"] = source["cycle"]
        frames.append(frame)
    combined = pd.concat(frames, ignore_index=True).drop_duplicates()
    return combined
