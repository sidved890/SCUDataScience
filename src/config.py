from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DATA_DIR = BASE_DIR / "UCMR-5"
PROCESSED_DATA_DIR = BASE_DIR / "data" / "processed"
OUTPUTS_DIR = BASE_DIR / "outputs" / "figures"

UCMR_ALL_PATH = RAW_DATA_DIR / "UCMR5_All.txt"
ZIP_CODES_PATH = RAW_DATA_DIR / "UCMR5_ZIPCodes.txt"

TARGET_ZIPS = {"94566", "94588"}
TARGET_PWSIDS = {"CA0110008"}
BENCHMARK_PWSIDS = {"CA0110003"}

KEY_CONTAMINANTS = ["PFOS", "PFOA", "PFHxS", "PFBS", "PFBA", "PFPeA"]
RISK_WEIGHT_MAP = {
    "PFOS": 5.0,
    "PFOA": 5.0,
    "PFHxS": 4.0,
    "PFBS": 2.0,
    "PFBA": 2.0,
    "PFPeA": 1.5,
}

RISK_LABELS = [
    (0, "Low"),
    (8, "Moderate"),
    (15, "High"),
    (24, "Very High"),
]

UGL_TO_NGL = 1000.0

PLEASANTON_PROCESSED_PATH = PROCESSED_DATA_DIR / "pleasanton_ucmr5.csv"
PLEASANTON_SUMMARY_PATH = PROCESSED_DATA_DIR / "pleasanton_summary.csv"
