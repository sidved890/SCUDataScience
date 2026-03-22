from __future__ import annotations

import streamlit as st

from src.analyze import benchmark_subset, build_source_summary, latest_detected_values, source_profile
from src.charts import heatmap_chart, max_concentration_chart, trend_chart
from src.clean_data import clean_ucmr_data, pleasanton_subset
from src.config import PLEASANTON_PROCESSED_PATH, PLEASANTON_SUMMARY_PATH, TARGET_ZIPS
from src.load_data import load_ucmr_results, load_zip_codes
from src.risk_score import score_sources

st.set_page_config(page_title="Pleasanton PFAS Water Risk Tracker", layout="wide")


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
benchmark_df = benchmark_subset(pleasanton_df)

st.title("Pleasanton PFAS Water Risk Tracker")
st.caption("EPA UCMR5 monitoring results tailored to Pleasanton ZIP codes 94566 and 94588.")

top_source = scored_df.iloc[0]
metric_cols = st.columns(4)
metric_cols[0].metric("Pleasanton ZIPs", ", ".join(sorted(TARGET_ZIPS)))
metric_cols[1].metric("Sources analyzed", int(scored_df.shape[0]))
metric_cols[2].metric("Top risk source", top_source["FacilityName"])
metric_cols[3].metric("Top risk score", f'{top_source["risk_score"]:.1f}')

tab_overview, tab_sources, tab_trends, tab_policy = st.tabs(
    ["Overview", "Source Comparison", "Contaminant Trends", "Policy Insights"]
)

with tab_overview:
    st.subheader("What this app shows")
    st.write(
        "This dashboard compares Pleasanton drinking water sources using EPA UCMR5 data, "
        "highlighting where PFAS detections are strongest and how they differ between "
        "local groundwater wells and the Zone 7 intertie."
    )
    st.dataframe(
        scored_df[["FacilityName", "FacilityWaterType", "risk_score", "risk_label", "detected_contaminants", "max_detected_ng_L"]],
        use_container_width=True,
        hide_index=True,
    )
    st.plotly_chart(max_concentration_chart(summary_df), use_container_width=True)

with tab_sources:
    st.subheader("Source risk profile")
    left, right = st.columns([3, 2])
    with left:
        st.plotly_chart(heatmap_chart(summary_df), use_container_width=True)
    with right:
        st.dataframe(
            profiles_df[["FacilityName", "FacilityWaterType", "sample_events", "detected_contaminants", "total_detections", "max_detected_ng_L"]],
            use_container_width=True,
            hide_index=True,
        )
    st.subheader("Latest detected values")
    st.dataframe(latest_df, use_container_width=True, hide_index=True)

with tab_trends:
    st.subheader("Trend view")
    st.plotly_chart(trend_chart(benchmark_df), use_container_width=True)
    st.write(
        "The strongest Pleasanton signals in the current dataset appear in `Well 5` and `Well 6`, "
        "while `Zone 7 Intertie` tends to show fewer and lower PFAS detections in the rows reviewed."
    )

with tab_policy:
    st.subheader("Policy-oriented takeaways")
    st.markdown(
        """
        - Prioritize continued monitoring and treatment for `Well 6`, which shows the strongest PFOS, PFOA, and PFHxS detections.
        - Use source blending and imported surface water strategically when local well concentrations are elevated.
        - Communicate source-level water quality clearly to residents in ZIP codes `94566` and `94588`.
        - Treat this dashboard as a screening and prioritization tool, not a clinical exposure model.
        """
    )
    st.subheader("Hackathon framing")
    st.write(
        "Our project turns raw federal monitoring files into a local decision-support tool for Pleasanton. "
        "Instead of only reporting detections, it ranks sources, visualizes PFAS trends, and supports "
        "data-backed water management conversations."
    )
