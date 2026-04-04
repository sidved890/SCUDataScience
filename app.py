from __future__ import annotations

import streamlit as st
import pandas as pd

from src.analyze import build_source_summary, contaminant_glossary, latest_detected_values, source_profile
from src.charts import heatmap_chart, max_concentration_chart, trend_chart
from src.clean_data import clean_ucmr_data, subset_by_zip
from src.load_data import load_ucmr_results, load_zip_codes
from src.risk_score import score_sources
from src.config import KEY_CONTAMINANTS

st.set_page_config(page_title="PFAS Contamination Risk Tracker", layout="wide")

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Manrope:wght@500;700;800&family=Source+Serif+4:wght@400;600&display=swap');

    html, body, [class*="css"] {
        font-family: "Manrope", "Avenir Next", sans-serif;
    }

    .stApp {
        background:
            radial-gradient(circle at 8% 10%, rgba(48, 164, 170, 0.26), transparent 24%),
            radial-gradient(circle at 88% 8%, rgba(119, 64, 112, 0.22), transparent 25%),
            linear-gradient(135deg, #255e68 0%, #314f67 35%, #62435e 100%);
        color: #f7f4ee;
    }

    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, rgba(17,22,30,0.95), rgba(14,18,25,0.96));
        border-right: 1px solid rgba(255,255,255,0.08);
    }

    h1, h2, h3 {
        font-family: "Manrope", "Avenir Next", sans-serif;
        letter-spacing: -0.04em;
        color: #fffaf3;
    }

    .hero {
        border: 1px solid rgba(255,255,255,0.12);
        border-radius: 28px;
        padding: 1.8rem 1.9rem 1.5rem 1.9rem;
        background: linear-gradient(180deg, rgba(8,12,18,0.24), rgba(8,12,18,0.36));
        box-shadow: 0 18px 48px rgba(0,0,0,0.18);
        margin-bottom: 1rem;
        backdrop-filter: blur(8px);
    }

    .hero h1 {
        font-size: 4.25rem;
        line-height: 0.95;
        margin-bottom: 0.7rem;
    }

    .hero p {
        font-family: "Source Serif 4", Georgia, serif;
        font-size: 1.2rem;
        line-height: 1.6;
        color: rgba(255,255,255,0.88);
        max-width: 980px;
    }

    .hero-pill {
        display: inline-block;
        padding: 0.45rem 0.85rem;
        border-radius: 999px;
        margin-right: 0.5rem;
        margin-top: 0.4rem;
        background: rgba(255,255,255,0.09);
        border: 1px solid rgba(255,255,255,0.12);
        color: #eef8e6;
        font-size: 0.92rem;
    }

    .section-card {
        border: 1px solid rgba(255,255,255,0.09);
        border-radius: 24px;
        padding: 1.1rem 1.2rem 0.8rem 1.2rem;
        background: rgba(12,16,24,0.42);
        backdrop-filter: blur(10px);
        margin-bottom: 1rem;
    }

    .microcopy {
        color: rgba(255,255,255,0.82);
        font-size: 1rem;
        line-height: 1.6;
    }

    .metric-card {
        border: 1px solid rgba(255,255,255,0.09);
        border-radius: 20px;
        padding: 1rem;
        background: linear-gradient(180deg, rgba(255,255,255,0.05), rgba(255,255,255,0.02));
        min-height: 120px;
    }

    .metric-label {
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 0.09em;
        color: rgba(255,255,255,0.66);
    }

    .metric-value {
        font-size: 2.2rem;
        font-weight: 800;
        line-height: 1.05;
        color: #ffffff;
        margin-top: 0.4rem;
    }

    .metric-sub {
        color: rgba(255,255,255,0.72);
        font-size: 0.92rem;
        margin-top: 0.45rem;
    }

    div[data-testid="stTextInput"] input {
        font-size: 1.45rem !important;
        font-weight: 700 !important;
        padding: 0.9rem 1rem !important;
        border-radius: 18px !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_data
def load_app_data():
    raw_results = load_ucmr_results()
    zip_codes = load_zip_codes()
    cleaned = clean_ucmr_data(raw_results, zip_codes)
    glossary = contaminant_glossary(cleaned)
    return cleaned, glossary


def render_metric_card(label: str, value: str, subtext: str):
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
            <div class="metric-sub">{subtext}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def selected_zip_subset(df, selected_zip, selected_systems, selected_contaminants, detected_only):
    zip_df = subset_by_zip(df, selected_zip)
    if selected_systems:
        zip_df = zip_df[zip_df["PWSID"].isin(selected_systems)]
    if selected_contaminants:
        zip_df = zip_df[zip_df["Contaminant"].isin(selected_contaminants)]
    if detected_only:
        zip_df = zip_df[zip_df["detected"]]
    return zip_df


cleaned_df, glossary_df = load_app_data()
latest_cycle_df = cleaned_df[cleaned_df["ucmr_cycle"].eq("UCMR5")].copy()
available_zips = sorted(z for z in latest_cycle_df["ZIPCode"].dropna().unique() if z.isdigit())

st.markdown(
    """
    <div class="hero">
        <h1>PFAS Contamination Risk Tracker</h1>
        <p>
            Enter any ZIP code to explore the latest EPA UCMR drinking water data for that area, then use the trends page
            to look back across all UCMR cycles and see how contaminant patterns change over time.
        </p>
        <span class="hero-pill">Latest results from UCMR5</span>
        <span class="hero-pill">Historical trends from UCMR1-5</span>
        <span class="hero-pill">ZIP-based search</span>
        <span class="hero-pill">Interactive source comparison</span>
        <span class="hero-pill">Contaminant glossary included</span>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.subheader("Start With A ZIP Code")
st.markdown(
    '<div class="microcopy">Enter a 5-digit ZIP code to load matching water systems. The app will then unlock system filters, contaminant filters, trend views, and source scoring for that geography.</div>',
    unsafe_allow_html=True,
)
selected_zip = st.text_input("ZIP code", value="", placeholder="Enter ZIP code, for example 94566")
st.markdown("</div>", unsafe_allow_html=True)

st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.subheader("Contaminant Glossary")
st.markdown(
    '<div class="microcopy">This table lists contaminants found across the integrated UCMR datasets and explains them in plain language. Use it as a reference before searching by ZIP.</div>',
    unsafe_allow_html=True,
)
st.dataframe(glossary_df, width="stretch", hide_index=True)
st.markdown("</div>", unsafe_allow_html=True)

if not selected_zip:
    st.info("Enter a ZIP code above to activate the explorer.")
    st.stop()

selected_zip = selected_zip.strip()
if selected_zip not in available_zips:
    st.error("That ZIP code was not found in the available UCMR ZIP mappings. Try another ZIP from the supported dataset.")
    st.stop()

latest_zip_base_df = subset_by_zip(latest_cycle_df, selected_zip)
zip_system_options = (
    latest_zip_base_df.loc[:, ["PWSID", "PWSName"]]
    .drop_duplicates()
    .sort_values(["PWSName", "PWSID"])
)
system_labels = {row["PWSID"]: f'{row["PWSName"]} ({row["PWSID"]})' for _, row in zip_system_options.iterrows()}
default_systems = list(system_labels.keys())

zip_contaminant_options = sorted(latest_zip_base_df["Contaminant"].dropna().unique())
default_contaminants = [contaminant for contaminant in KEY_CONTAMINANTS if contaminant in zip_contaminant_options]
if not default_contaminants:
    default_contaminants = zip_contaminant_options.copy()

with st.sidebar:
    st.header("Filters")
    st.caption(f"Active ZIP: {selected_zip}")
    selected_systems = st.multiselect(
        "Water systems in this ZIP",
        options=default_systems,
        default=default_systems,
        format_func=lambda pwsid: system_labels[pwsid],
    )
    selected_contaminants = st.multiselect(
        "Contaminants in this ZIP",
        options=zip_contaminant_options,
        default=default_contaminants,
    )
    detected_only = st.toggle("Detected results only", value=False)

selected_df = selected_zip_subset(latest_cycle_df, selected_zip, selected_systems, selected_contaminants, detected_only)
trend_df = selected_zip_subset(cleaned_df, selected_zip, selected_systems, selected_contaminants, detected_only)

selected_summary_df = build_source_summary(selected_df) if not selected_df.empty else pd.DataFrame(
    columns=["PWSID", "PWSName", "FacilityID", "FacilityName", "FacilityWaterType", "Contaminant", "ucmr_cycles", "sample_events", "detections", "latest_date", "max_result_ng_L", "avg_detected_ng_L"]
)
selected_scored_df = score_sources(selected_df) if not selected_df.empty else None
selected_profiles_df = source_profile(selected_df) if not selected_df.empty else None
selected_latest_df = latest_detected_values(selected_df) if not selected_df.empty else pd.DataFrame(
    columns=["ucmr_cycle", "PWSName", "FacilityName", "CollectionDate", "Contaminant", "result_ng_L"]
)

if selected_scored_df is None or selected_scored_df.empty:
    top_source_name = "No scored source"
    top_risk_score = "0.0"
else:
    top_source_name = selected_scored_df.iloc[0]["FacilityName"]
    top_risk_score = f'{selected_scored_df.iloc[0]["risk_score"]:.1f}'

metrics = st.columns(4)
with metrics[0]:
    render_metric_card("Selected ZIP", selected_zip, "Current geographic focus")
with metrics[1]:
    render_metric_card("Water Systems", str(len(selected_systems)), "Systems mapped to this ZIP")
with metrics[2]:
    render_metric_card("Top Source", top_source_name, "Highest source score under the current filters")
with metrics[3]:
    render_metric_card("Top Score", top_risk_score, "Explainable prioritization score")

tabs = st.tabs(["Overview", "Source Comparison", "Contaminant Trends", "Latest Results"])
overview_tab, sources_tab, trends_tab, latest_tab = tabs

with overview_tab:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.subheader(f"ZIP {selected_zip} Overview")
    st.markdown(
        '<div class="microcopy">This view summarizes the latest UCMR cycle for the selected ZIP, so the homepage reflects the newest EPA screening results instead of mixing current and historical records.</div>',
        unsafe_allow_html=True,
    )
    if selected_scored_df is not None and not selected_scored_df.empty:
        st.dataframe(
            selected_scored_df[
                ["PWSName", "FacilityName", "FacilityWaterType", "risk_score", "risk_label", "detected_contaminants", "max_detected_ng_L", "sample_events"]
            ],
            width="stretch",
            hide_index=True,
        )
    else:
        st.warning("No rows match the current filters. Try enabling more systems, more contaminants, or turning off the detected-only filter.")
    st.markdown("</div>", unsafe_allow_html=True)

with sources_tab:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.subheader("Source Comparison")
    st.plotly_chart(
        max_concentration_chart(
            selected_summary_df,
            selected_contaminants,
            f"Maximum UCMR5 Contaminant Concentrations by Source for ZIP {selected_zip}",
        ),
        config={"responsive": True},
    )
    st.plotly_chart(
        heatmap_chart(
            selected_summary_df,
            selected_contaminants,
            f"Source-by-Contaminant Heatmap for ZIP {selected_zip}",
        ),
        config={"responsive": True},
    )
    if selected_profiles_df is not None and not selected_profiles_df.empty:
        st.dataframe(
            selected_profiles_df[
                ["PWSName", "FacilityName", "FacilityWaterType", "ucmr_cycles", "sample_events", "detected_contaminants", "max_detected_ng_L"]
            ],
            width="stretch",
            hide_index=True,
        )
    st.markdown("</div>", unsafe_allow_html=True)

with trends_tab:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.subheader("Contaminant Trends")
    st.plotly_chart(
        trend_chart(
            trend_df,
            selected_contaminants,
            f"Contaminant Trends Across UCMR Cycles for ZIP {selected_zip}",
            detected_only,
        ),
        config={"responsive": True},
    )
    st.markdown(
        '<div class="microcopy">The trend graph is the only place where the app reaches across UCMR1-5. Everything outside this tab stays focused on the latest cycle.</div>',
        unsafe_allow_html=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)

with latest_tab:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.subheader("Latest Detected Results")
    st.dataframe(selected_latest_df, width="stretch", hide_index=True)
    st.markdown("</div>", unsafe_allow_html=True)
