# Motor Vehicle Theft Analysis Dashboard

<p align="center">
  <img src="logo.webp" alt="Cenfri Logo" width="120" />
</p>

<p align="center">
  <a href="https://www.python.org/"><img src="https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white" alt="Python"></a>
  <a href="https://streamlit.io/"><img src="https://img.shields.io/badge/Streamlit-1.28+-FF4B4B?logo=streamlit&logoColor=white" alt="Streamlit"></a>
  <a href="https://plotly.com/python/"><img src="https://img.shields.io/badge/Plotly-5.17+-3F4F75?logo=plotly&logoColor=white" alt="Plotly"></a>
  <a href="https://pandas.pydata.org/"><img src="https://img.shields.io/badge/Pandas-2.0+-150458?logo=pandas&logoColor=white" alt="Pandas"></a>
  <img src="https://img.shields.io/badge/Data%20Science-Vehicle%20Theft-0a9396" alt="Tag: Vehicle Theft" />
  <img src="https://img.shields.io/badge/Use%20Case-Police%20Analytics-005f73" alt="Tag: Police Analytics" />
</p>

> **Tags:** `streamlit` · `plotly` · `data-science` · `dashboards` · `crime-analytics`

##  Overview

This repository contains an interactive Streamlit dashboard, supporting notebook, and documentation for Cenfri's Motor Vehicle Theft Analysis assessment (November 2025). The dashboard helps the Chief of Police understand theft patterns, high-risk areas, vehicle characteristics, and population dynamics by combining descriptive analytics with actionable recommendations.

Key deliverables include:

- **`app.py`** – Streamlit application presenting KPIs, charts, and tables with dynamic filters.
- **`stolen_vehicles_enhanced.csv`** – Enriched dataset used across the analysis.
- **`cenfri.ipynb`** – Companion notebook for exploratory analysis and experimentation.
- **`.devcontainer/`** – Optional container setup for reproducible development environments.
- **`requirements.txt`** – Dependency list pinned for Streamlit Cloud deployment.

## Repository Structure

```
datascience
├── .devcontainer/           # VS Code dev container definition (optional)
├── app.py                   # Main Streamlit application
├── cenfri.ipynb             # Exploratory notebook used during analysis
├── logo.webp                # Cenfri branding displayed in the UI
├── requirements.txt         # Python dependencies
├── stolen_vehicles_enhanced.csv  # Core dataset (CSV)
└── README.md                # You are here
```

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/chrismazi/datascience.git
cd datascience
```

### 2. Create and activate a virtual environment (recommended)

```bash
python -m venv .venv
source .venv/bin/activate   # On Windows use: .venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Launch the dashboard

```bash
streamlit run app.py
```

Streamlit will open a local development server (default: `http://localhost:8501`). Use the sidebar filters (make, type, color, region) to interact with the data in real time.

##  Dashboard Highlights

- **Executive KPIs** – total incidents, most stolen makes, thefts per 100k population, and more.
- **Model & Make Rankings** – horizontal bar charts spotlighting the top stolen vehicles.
- **Temporal Trends** – quarterly incident trends plus model year analysis to reveal high-risk periods.
- **Demographics Breakdown** – color, vehicle type, and make-color combinations visualized via bar charts and tables.
- **Population Density Impact** – scatter plot with OLS trendline quantifying correlation between density and thefts.
- **Per-Capita Risk Tables** – ranked tables for highest and lowest theft rates per 10k residents.

## Notebooks & Offline Exploration

The `cenfri.ipynb` notebook documents exploratory data analysis, feature engineering trials, and supporting visuals that informed the dashboard narrative. Run it with Jupyter or VS Code notebooks after installing requirements.

## Deployment

- The project is deployable on **Streamlit Cloud**. Ensure `requirements.txt` stays synchronized with the app.
- Include `logo.webp` and `stolen_vehicles_enhanced.csv` in the root directory of the deployment.
- For containerized development, open the repo in VS Code and select “Reopen in Container”.

##  Assessment Deliverables

| Deliverable | Location | Description |
|-------------|----------|-------------|
| Interactive Dashboard | `app.py` | Streamlit app prioritizing key vehicle theft insights for the Chief of Police. |
| Dataset | `stolen_vehicles_enhanced.csv` | Clean, enriched dataset used for all visuals and metrics. |
| Notebook | `cenfri.ipynb` | Exploratory analysis and supplementary charts. |
| README | `README.md` | Project documentation, setup steps, and narrative. |




