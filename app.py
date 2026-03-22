from __future__ import annotations

import streamlit as st

from src.analyze import benchmark_subset, build_source_summary, latest_detected_values, source_profile
from src.charts import heatmap_chart, max_concentration_chart, trend_chart
from src.clean_data import clean_ucmr_data, pleasanton_subset
from src.config import KEY_CONTAMINANTS, PLEASANTON_PROCESSED_PATH, PLEASANTON_SUMMARY_PATH, TARGET_PWSIDS, TARGET_ZIPS
from src.load_data import load_ucmr_results, load_zip_codes
from src.risk_score import score_sources

st.set_page_config(page_title="Pleasanton PFAS Water Risk Tracker", layout="wide")

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;700&family=Source+Serif+4:wght@400;600&display=swap');

    html, body, [class*="css"]  {
        font-family: "Space Grotesk", "Avenir Next", sans-serif;
    }

    .stApp {
        background:
            radial-gradient(circle at top left, rgba(239, 88, 88, 0.14), transparent 28%),
            radial-gradient(circle at 85% 10%, rgba(255, 199, 94, 0.10), transparent 22%),
            radial-gradient(circle at top right, rgba(69, 179, 157, 0.12), transparent 24%),
            #0d1017;
    }

    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, rgba(19,24,36,0.98), rgba(10,14,23,0.98));
        border-right: 1px solid rgba(255,255,255,0.06);
    }

    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3,
    section[data-testid="stSidebar"] label {
        color: #f7f3ed;
    }

    h1, h2, h3 {
        font-family: "Space Grotesk", "Avenir Next", sans-serif;
        letter-spacing: -0.03em;
    }

    .hero-card {
        padding: 1.5rem 1.6rem;
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 24px;
        background:
            linear-gradient(135deg, rgba(239,88,88,0.10), rgba(255,255,255,0.02) 35%, rgba(69,179,157,0.08)),
            rgba(14, 18, 28, 0.92);
        box-shadow: 0 18px 48px rgba(0,0,0,0.24);
        margin-bottom: 1.1rem;
    }

    .hero-subtitle {
        font-family: "Source Serif 4", Georgia, serif;
        font-size: 1.15rem;
        line-height: 1.6;
        color: rgba(255,255,255,0.82);
    }

    .hero-grid {
        display: grid;
        grid-template-columns: 1.5fr 1fr;
        gap: 1rem;
        align-items: start;
    }

    .hero-note {
        border-left: 3px solid rgba(255, 199, 94, 0.8);
        padding-left: 1rem;
        color: rgba(255,255,255,0.78);
        font-size: 0.98rem;
        line-height: 1.6;
    }

    .insight-pill {
        display: inline-block;
        padding: 0.45rem 0.75rem;
        border-radius: 999px;
        margin: 0.2rem 0.35rem 0.2rem 0;
        background: rgba(239, 88, 88, 0.14);
        border: 1px solid rgba(239, 88, 88, 0.24);
        color: #ffd9d9;
        font-size: 0.92rem;
    }

    .stat-card {
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 20px;
        background: linear-gradient(180deg, rgba(255,255,255,0.04), rgba(255,255,255,0.015));
        padding: 1rem 1rem 0.95rem 1rem;
        min-height: 132px;
        box-shadow: 0 10px 24px rgba(0,0,0,0.18);
    }

    .stat-label {
        font-size: 0.88rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: rgba(255,255,255,0.62);
        margin-bottom: 0.5rem;
    }

    .stat-value {
        font-size: 2.25rem;
        line-height: 1.05;
        font-weight: 700;
        color: #fff6ec;
    }

    .stat-caption {
        font-size: 0.9rem;
        margin-top: 0.55rem;
        color: rgba(255,255,255,0.68);
    }

    .section-card {
        border: 1px solid rgba(255,255,255,0.07);
        border-radius: 22px;
        background: rgba(14, 18, 28, 0.78);
        padding: 1rem 1.1rem 0.75rem 1.1rem;
        margin-bottom: 0.9rem;
    }

    .microcopy {
        color: rgba(255,255,255,0.72);
        font-size: 0.97rem;
        line-height: 1.6;
    }

    .callout {
        padding: 0.9rem 1rem;
        border-radius: 18px;
        background: linear-gradient(180deg, rgba(69,179,157,0.12), rgba(69,179,157,0.06));
        border: 1px solid rgba(69,179,157,0.18);
        color: #dff8f2;
        margin: 0.5rem 0 1rem 0;
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
    pleasanton = pleasanton_subset(cleaned)
    summary = build_source_summary(pleasanton)
    scored = score_sources(pleasanton)
    profiles = source_profile(pleasanton)
    latest = latest_detected_values(pleasanton)

    PLEASANTON_PROCESSED_PATH.parent.mkdir(parents=True, exist_ok=True)
    pleasanton.to_csv(PLEASANTON_PROCESSED_PATH, index=False)
    summary.to_csv(PLEASANTON_SUMMARY_PATH, index=False)

    return pleasanton, summary, scored, profiles, latest


pleasanton_df, summary_df, scored_df, profiles_df, latest_df = load_app_data()
raw_results = load_ucmr_results()
zip_codes = load_zip_codes()
cleaned_df = clean_ucmr_data(raw_results, zip_codes)
benchmark_df = benchmark_subset(cleaned_df)
available_zips = sorted(z for z in cleaned_df["ZIPCode"].dropna().unique() if z.isdigit())


def filter_for_selection(df, selected_zip, selected_systems, contaminants, detected_only):
    scoped = df[df["Contaminant"].isin(contaminants)].copy()
    zip_match = scoped["ZIPCode"].eq(selected_zip)
    if selected_systems:
        scoped = scoped[zip_match & scoped["PWSID"].isin(selected_systems)]
    else:
        scoped = scoped[zip_match]
    if detected_only:
        scoped = scoped[scoped["detected"]]
    return scoped


def pleasanton_reference(df, contaminants):
    ref = df[df["PWSID"].isin(TARGET_PWSIDS) & df["Contaminant"].isin(contaminants)].copy()
    return ref


def render_stat_card(label: str, value: str, caption: str):
    st.markdown(
        f"""
        <div class="stat-card">
            <div class="stat-label">{label}</div>
            <div class="stat-value">{value}</div>
            <div class="stat-caption">{caption}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


with st.sidebar:
    st.header("Explore By ZIP")
    st.caption("Choose a ZIP code, narrow to water systems, and compare PFAS signals interactively.")
    selected_zip = st.selectbox("ZIP code", available_zips, index=available_zips.index("94566") if "94566" in available_zips else 0)
    zip_system_options = (
        cleaned_df.loc[cleaned_df["ZIPCode"].eq(selected_zip), ["PWSID", "PWSName"]]
        .drop_duplicates()
        .sort_values(["PWSName", "PWSID"])
    )
    system_labels = {
        row["PWSID"]: f'{row["PWSName"]} ({row["PWSID"]})'
        for _, row in zip_system_options.iterrows()
    }
    default_systems = list(system_labels.keys())
    systems_state_key = f"systems_for_{selected_zip}"
    selected_systems = st.multiselect(
        "Water systems tied to this ZIP",
        options=default_systems,
        default=default_systems,
        key=systems_state_key,
        format_func=lambda pwsid: system_labels[pwsid],
    )
    selected_contaminants = st.multiselect(
        "Contaminants",
        options=KEY_CONTAMINANTS,
        default=["PFOS", "PFOA", "PFHxS"],
    )
    detected_only = st.toggle("Detected results only", value=False)
    compare_to_pleasanton = st.toggle("Compare selected ZIP to Pleasanton", value=True)

selected_df = filter_for_selection(cleaned_df, selected_zip, selected_systems, selected_contaminants, detected_only)
comparison_df = selected_df.copy()
if compare_to_pleasanton and selected_zip not in TARGET_ZIPS:
    comparison_df = st.session_state.get("comparison_df", comparison_df)
    comparison_df = comparison_df
    comparison_df = selected_df.copy()
    pleasanton_df_for_compare = pleasanton_reference(cleaned_df, selected_contaminants)
    if detected_only:
        pleasanton_df_for_compare = pleasanton_df_for_compare[pleasanton_df_for_compare["detected"]]
    comparison_df = comparison_df.copy()
    comparison_df = comparison_df._append(pleasanton_df_for_compare, ignore_index=True)

selected_summary_df = build_source_summary(selected_df) if not selected_df.empty else summary_df.iloc[0:0].copy()
selected_scored_df = score_sources(selected_df) if not selected_df.empty else scored_df.iloc[0:0].copy()
selected_profiles_df = source_profile(selected_df) if not selected_df.empty else profiles_df.iloc[0:0].copy()
selected_latest_df = latest_detected_values(selected_df) if not selected_df.empty else latest_df.iloc[0:0].copy()

selected_system_count = len(selected_systems)
top_source_name = selected_scored_df.iloc[0]["FacilityName"] if not selected_scored_df.empty else "No detected source"
top_risk_score = f'{selected_scored_df.iloc[0]["risk_score"]:.1f}' if not selected_scored_df.empty else "0.0"
detected_source_count = int(selected_profiles_df["detected_contaminants"].gt(0).sum()) if not selected_profiles_df.empty else 0

st.markdown(
    f"""
    <div class="hero-card">
        <div class="hero-grid">
            <div>
                <h1>PFAS Water Risk Explorer</h1>
                <p class="hero-subtitle">
                    Explore EPA UCMR5 drinking water data by ZIP code, compare source-level PFAS detections,
                    and keep Pleasanton as a benchmark for local water risk storytelling.
                </p>
                <span class="insight-pill">Current ZIP: {selected_zip}</span>
                <span class="insight-pill">Systems selected: {selected_system_count}</span>
                <span class="insight-pill">Detected sources: {detected_source_count}</span>
                <span class="insight-pill">Contaminants: {", ".join(selected_contaminants) if selected_contaminants else "None"}</span>
            </div>
            <div class="hero-note">
                This app is designed to feel like a public-facing decision tool, not just a static chart sheet.
                It translates raw monitoring rows into ranked sources, trend views, and policy-friendly takeaways.
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

metric_cols = st.columns(4)
with metric_cols[0]:
    render_stat_card("Selected ZIP", selected_zip, "User-controlled geographic view")
with metric_cols[1]:
    render_stat_card("Sources Analyzed", str(int(selected_scored_df.shape[0])), "Water sources in the active filter")
with metric_cols[2]:
    render_stat_card("Top Risk Source", top_source_name, "Highest-ranked source under current settings")
with metric_cols[3]:
    render_stat_card("Top Risk Score", top_risk_score, "Transparent heuristic score for prioritization")

tab_overview, tab_sources, tab_trends, tab_policy = st.tabs(
    ["Overview", "Source Comparison", "Contaminant Trends", "Policy Insights"]
)

with tab_overview:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.subheader("What This App Shows")
    st.markdown(
        '<div class="microcopy">This view translates EPA monitoring records into source-level comparisons for the selected ZIP. '
        "Use the controls on the left to change ZIPs, limit the systems shown, and focus on specific PFAS compounds.</div>",
        unsafe_allow_html=True,
    )
    if not selected_scored_df.empty:
        st.markdown(
            f'<div class="callout">Right now, <strong>{top_source_name}</strong> is the highest-priority source in ZIP <strong>{selected_zip}</strong> '
            f'with a risk score of <strong>{top_risk_score}</strong>.</div>',
            unsafe_allow_html=True,
        )
    st.dataframe(
        selected_scored_df[["FacilityName", "FacilityWaterType", "risk_score", "risk_label", "detected_contaminants", "max_detected_ng_L"]] if not selected_scored_df.empty else selected_scored_df,
        width="stretch",
        hide_index=True,
    )
    st.plotly_chart(
        max_concentration_chart(
            selected_summary_df,
            selected_contaminants,
            f"Maximum PFAS Concentrations by Source for ZIP {selected_zip}",
        ),
        width="stretch",
    )
    st.markdown("</div>", unsafe_allow_html=True)

with tab_sources:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.subheader("Source Risk Profile")
    st.markdown(
        '<div class="microcopy">Compare which sources are driving the strongest PFAS signals and which contaminants dominate each source profile.</div>',
        unsafe_allow_html=True,
    )
    left, right = st.columns([3, 2])
    with left:
        st.plotly_chart(
            heatmap_chart(
                selected_summary_df,
                selected_contaminants,
                f"Source-by-Contaminant Heatmap for ZIP {selected_zip}",
            ),
            width="stretch",
        )
    with right:
        st.dataframe(
            selected_profiles_df[["FacilityName", "FacilityWaterType", "sample_events", "detected_contaminants", "total_detections", "max_detected_ng_L"]] if not selected_profiles_df.empty else selected_profiles_df,
            width="stretch",
            hide_index=True,
        )
    st.subheader("Latest Detected Values")
    st.dataframe(selected_latest_df, width="stretch", hide_index=True)
    st.markdown("</div>", unsafe_allow_html=True)

with tab_trends:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.subheader("Trend View")
    st.markdown(
        '<div class="microcopy">Track how measured concentrations change across sample events and benchmark the selected ZIP against Pleasanton when useful.</div>',
        unsafe_allow_html=True,
    )
    trend_title = f"PFAS Trends for ZIP {selected_zip}"
    if compare_to_pleasanton:
        trend_title += " with Pleasanton benchmark"
    st.plotly_chart(
        trend_chart(comparison_df, selected_contaminants, trend_title, detected_only),
        width="stretch",
    )
    if selected_zip in TARGET_ZIPS:
        st.write(
            "For Pleasanton, the strongest signals in the current dataset appear in `Well 5` and `Well 6`, "
            "while `Zone 7 Intertie` generally appears lower in the filtered records."
        )
    else:
        st.write(
            "Use this chart to compare the selected ZIP's systems against Pleasanton. This helps turn a local case study "
            "into a broader public-facing exploration tool."
        )
    st.markdown("</div>", unsafe_allow_html=True)

with tab_policy:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.subheader("Policy-Oriented Takeaways")
    if not selected_scored_df.empty:
        highest = selected_scored_df.iloc[0]
        st.markdown(
            f"""
            - Highest current priority source: `{highest["FacilityName"]}` with a risk score of `{highest["risk_score"]:.1f}`.
            - Focus communication around `{", ".join(selected_contaminants)}` because those are the contaminants currently selected.
            - Use ZIP-level filtering carefully: these are systems associated with the ZIP, not a guaranteed household-specific service map.
            - Treat the tool as a screening and prioritization dashboard, not a medical diagnosis engine.
            """
        )
    else:
        st.info("No records match the current filters. Try turning off `Detected results only` or selecting more systems.")
    st.subheader("Hackathon framing")
    st.write(
        "Our project turns raw federal monitoring files into a ZIP-based decision-support tool. "
        "Instead of acting like a static report, it lets residents, judges, or policymakers explore PFAS detections "
        "interactively and compare another community's systems back to Pleasanton."
    )
    st.markdown("</div>", unsafe_allow_html=True)
