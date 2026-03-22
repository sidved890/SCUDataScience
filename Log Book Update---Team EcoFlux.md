# Log Book---Team EcoFlux

## Table of Contents

**Sunday, March 15**  
[Aim]  
[Achieved]  
[Future]  

**Tuesday, March 17**  
[Aim]  
[Achieved]  
[Future]  

**Thursday, March 19**  
[Aim]  
[Achieved]  
[Future]  

**Friday, March 20**  
[Aim]  
[Achieved]  
[Future]  

**Saturday, March 21**  
[Aim]  
[Achieved]  
[Future]  

**Sunday, March 22**  
[Aim]  
[Achieved]  
[Future]  

---

## Sunday, March 15

### Aim

- Brainstorm a problem connected to the Tri-Valley area that could become a strong datathon project.
- Identify whether Pleasanton water quality and PFAS contamination could support a sustainability-focused idea.

### [Achieved]

- Discussed multiple project directions and narrowed the focus to PFAS contamination in Pleasanton drinking water.
- Chose to center the project on local impact, especially around Pleasanton residents and public water systems.
- Agreed that the project should combine data analysis with a clear public-facing message rather than staying purely theoretical.

### [Future]

- Gather official EPA and local water data sources.
- Test whether Pleasanton-specific records exist in UCMR5 and can support a real analysis.

---

## Tuesday, March 17

### Aim

- Review the available datasets and determine whether the project can be built around real public water records.
- Explore whether ZIP-code-level filtering is possible for Pleasanton.

### [Achieved]

- Located the UCMR5 files and supporting ZIP code mapping files.
- Confirmed that the EPA data includes Pleasanton-linked records through ZIP codes `94566` and `94588`.
- Identified that `CITY OF PLEASANTON` appears directly in the dataset along with source records such as `Zone 7 Intertie`, `Well 5`, and `Well 6`.

### [Future]

- Compare Pleasanton records across sources and contaminants.
- Decide whether to build a simulator, dashboard, or risk tracker.

---

## Thursday, March 19

### Aim

- Evaluate the original PFAS simulation script and determine whether it is robust enough for a datathon submission.
- Choose a final project direction that is data-driven and locally relevant.

### [Achieved]

- Reviewed the existing Python PFAS bioaccumulation model and noted that it relied on hardcoded values and simplified assumptions.
- Decided that a stronger project would be a Pleasanton PFAS Water Risk Tracker rather than only a pharmacokinetic simulator.
- Defined the new core project idea as a source-level dashboard comparing Pleasanton wells and the Zone 7 intertie using EPA UCMR5 data.

### [Future]

- Build a full project structure in VS Code.
- Create a data pipeline to read, clean, and summarize the raw UCMR5 files.

---

## Friday, March 20

### Aim

- Set up the coding environment and create the initial project scaffold.
- Build the first working version of the data pipeline and dashboard.

### [Achieved]

- Created the main project files including `app.py`, `requirements.txt`, `README.md`, and the `src/` module structure.
- Implemented scripts to load raw UCMR5 files, clean the data, convert units, and generate source summaries.
- Added a first transparent risk scoring system based on PFAS detections and concentrations.
- Built a first Streamlit dashboard showing Pleasanton-specific results.

### [Future]

- Improve usability and visual polish.
- Add more interactivity so the dashboard feels stronger for demo day.

---

## Saturday, March 21

### Aim

- Strengthen the dashboard presentation and make the project feel more like a finished product.
- Expand the app beyond a fixed Pleasanton-only view.

### [Achieved]

- Upgraded the dashboard layout and styling with improved typography, a hero section, and clearer visual hierarchy.
- Added more polished charts and organized the app into sections such as overview, source comparison, trends, and policy insights.
- Shifted the app from a static Pleasanton report to a broader PFAS explorer concept.

### [Future]

- Add custom ZIP code filtering so users can explore water systems outside Pleasanton.
- Include a benchmark comparison back to Pleasanton so the local story remains central.

---

## Sunday, March 22

### Aim

- Complete the interactive version of the dashboard.
- Make the app work for any ZIP code while preserving Pleasanton as the benchmark case study.

### [Achieved]

- Added custom ZIP code selection using the UCMR5 ZIP mapping file.
- Added water system selection, contaminant filters, and a detected-results toggle.
- Added an option to compare a selected ZIP back to Pleasanton.
- Fixed a bug where changing ZIP codes could leave old system selections in place and return empty results.
- Cleaned up the Streamlit app and verified that the updated Python files compile successfully.
- Prepared the repository for GitHub and documented how to run and push the project.

### [Future]

- Continue polishing the narrative and charts for final presentation.
- Add stronger explanation text for low-data ZIP codes and improve benchmark storytelling.
- If time permits, add a secondary exposure or health-context view as an optional bonus feature.
