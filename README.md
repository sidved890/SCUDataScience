# Pleasanton PFAS Water Risk Tracker

This project analyzes EPA UCMR5 drinking water monitoring data for Pleasanton, California, with a focus on ZIP codes `94566` and `94588`.

## Project Goal

Build a clear, local dashboard that compares PFAS detections across Pleasanton water sources such as:

- `Well 5`
- `Well 6`
- `Zone 7 Intertie`

The app turns raw EPA text files into source-level rankings, trend charts, and policy-oriented insights.

## Why This Project Works

- It is based on real EPA UCMR5 data already included in the repository.
- It is tightly tailored to Pleasanton rather than being a generic PFAS analysis.
- It provides an explainable source risk score instead of making overstated health claims.

## Setup

Create and activate a virtual environment, then install dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Run the dashboard:

```bash
streamlit run app.py
```

## Data Sources

- `UCMR-5/UCMR5_All.txt`
- `UCMR-5/UCMR5_ZIPCodes.txt`

## Project Structure

```text
app.py
src/
  config.py
  load_data.py
  clean_data.py
  analyze.py
  risk_score.py
  charts.py
data/processed/
outputs/figures/
```

## Current Scope

The current dashboard:

- loads raw UCMR5 files
- filters to Pleasanton systems and ZIPs
- converts reported concentrations to `ng/L`
- flags detections
- compares sources across key PFAS compounds
- computes a transparent risk score

## Suggested Demo Narrative

"We built a Pleasanton-specific PFAS risk tracker using EPA UCMR5 data. Instead of showing a giant raw spreadsheet, the app identifies which water sources have the strongest PFAS signals, compares wells to imported water, and gives the city a more actionable view of risk."
