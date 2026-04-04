from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
PROCESSED_DATA_DIR = BASE_DIR / "data" / "processed"
OUTPUTS_DIR = BASE_DIR / "outputs" / "figures"

UCMR_RESULT_SOURCES = [
    {
        "cycle": "UCMR1",
        "path": BASE_DIR / "UCMR1" / "ucmr1-occurrence-data.zip",
        "inner": "UCMR1_All.txt",
        "zip_map": None,
    },
    {
        "cycle": "UCMR2",
        "path": BASE_DIR / "UCMR2" / "ucmr2-occurrence-data.zip",
        "inner": "UCMR2_All.txt",
        "zip_map": None,
    },
    {
        "cycle": "UCMR3",
        "path": BASE_DIR / "UCMR3" / "ucmr3-occurrence-data.zip",
        "inner": "UCMR3_All.txt",
        "zip_map": "UCMR3_ZIPCodes.txt",
    },
    {
        "cycle": "UCMR4",
        "path": BASE_DIR / "UCMR4" / "ucmr4-occurrence-data.zip",
        "inner": "UCMR4_All.txt",
        "zip_map": "UCMR4_ZIPCodes.txt",
    },
    {
        "cycle": "UCMR5",
        "path": BASE_DIR / "UCMR-5" / "UCMR5_All.txt",
        "inner": None,
        "zip_map": BASE_DIR / "UCMR-5" / "UCMR5_ZIPCodes.txt",
    },
]

RESULT_COLUMNS = [
    "PWSID",
    "PWSName",
    "FacilityID",
    "FacilityName",
    "FacilityWaterType",
    "CollectionDate",
    "SampleID",
    "Contaminant",
    "MRL",
    "Units",
    "MethodID",
    "AnalyticalResultsSign",
    "AnalyticalResultValue",
    "State",
]

ZIP_COLUMNS = ["PWSID", "ZIPCODE"]

KEY_CONTAMINANTS = ["PFOS", "PFOA", "PFHxS", "PFBS", "PFBA", "PFPeA"]
RISK_WEIGHT_MAP = {
    "PFOS": 5.0,
    "PFOA": 5.0,
    "PFHxS": 4.0,
    "PFBS": 2.0,
    "PFBA": 2.0,
    "PFPeA": 1.5,
}
DEFAULT_UNKNOWN_CONTAMINANT_WEIGHT = 1.0

RISK_LABELS = [
    (0, "Low"),
    (8, "Moderate"),
    (15, "High"),
    (24, "Very High"),
]

UGL_TO_NGL = 1000.0

ALL_RESULTS_PROCESSED_PATH = PROCESSED_DATA_DIR / "ucmr_1_5_combined.csv"
SUMMARY_PROCESSED_PATH = PROCESSED_DATA_DIR / "ucmr_1_5_summary.csv"

CONTAMINANT_DESCRIPTIONS = {
    "PFOS": "A long-chain PFAS historically tied to firefighting foam and stain-resistant products, often treated as a high-priority contaminant because it persists for years in water and soil.",
    "PFOA": "A widely studied PFAS once used in industrial manufacturing, notable for its strong regulatory attention and long-term persistence in the environment.",
    "PFHxS": "A PFAS commonly linked to firefighting foam that tends to remain in water systems for long periods and can appear alongside PFOS in contamination profiles.",
    "PFBS": "A shorter-chain PFAS introduced as a replacement for older chemicals, often viewed as more mobile in water even when concentrations are relatively low.",
    "PFBA": "A very short-chain PFAS that can show up as a low-level detection and may signal broader PFAS presence even when legacy compounds are absent.",
    "PFPeA": "A short-chain perfluorinated acid used here as an indicator of lower-molecular-weight PFAS activity in a source or treatment system.",
    "1,4-dioxane": "A synthetic industrial chemical and solvent stabilizer monitored because it dissolves easily in water and is difficult to remove once present.",
    "chlorate": "A treatment-related contaminant that can form during disinfection and storage, making it useful for understanding operational water quality conditions.",
    "HAA9": "A grouped measure of nine haloacetic acids, used to capture overall disinfection byproduct burden rather than a single chemical alone.",
    "HAA6Br": "A brominated subset of haloacetic acids that can help distinguish bromine-influenced disinfection chemistry from other byproduct patterns.",
    "lithium": "A naturally occurring element included by EPA as an occurrence marker rather than a PFAS contaminant, useful for broader water chemistry context.",
}
