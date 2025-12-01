<!-- Banner with emoji icons for instant visual flair -->
<h1 align="center">🏙️ NYC Housing Pulse <span style="color:#38B6FF">(2015–2025)</span> 📈</h1>
<p align="center">
  <strong>Real Estate Trends, Visualized.</strong><br>
  <kbd>Affordability Index</kbd> 🏠 <kbd>Market Breadth</kbd> 🌐
</p>

---

## 🌟 Highlights

- <b>🏠 Affordability Index:</b> <span style="color:#46b946">Entry-level housing affordability (25th percentile)</span> by borough & year
- <b>🌐 Market Breadth:</b> <span style="color:#f7c143">Share of neighborhoods with positive yearly price growth</span>

---

## 🚀 Quick Overview

<blockquote>
NYC Housing Pulse (2015–2025) is a modern data science pipeline tracking, analyzing, and visualizing housing trends across <b>all five NYC boroughs</b> over ten years.<br>
🔹 <b>Official Data</b> from NYC Department of Finance<br>
🔹 <b>Modular ETL</b>: Clean, analyze, & visualize with ease<br>
🔹 <b>Ready-to-use metrics & beautiful plots</b> for researchers, journalists, and policy analysts
</blockquote>

---

## 🗂️ Directory Map

```diff
data/
│
├── r/   # 📥 Raw Excel files (official, 2015–2025)  
├── c/   # 🧹 Cleaned CSVs (per-year, per-borough)
├── i/   # 🏗️ Intermediate (all boroughs, full years)
├── p/   # 📊 Processed metric tables
└── v/   # 🖼️ Auto-generated visualizations

src/
└── nyc_sales/
    ├── __init__.py       # Main module loader 🚦
    ├── extract.py        # 📑 Excel → CSV schema checker
    ├── clean.py          # 🧼 Cleaning & normalization
    ├── ingest.py         # 🗃️ Smart ingest
    ├── metrics.py        # 📏 Calculates custom metrics
    └── visualize.py      # 🎨 Publication-quality figures

main.ipynb   # 🚀 Notebook: Run the whole pipeline!
nyc_housing_pulse_2015_2025.csv   # 💾 One clean, unified dataset
requirements.txt   # 🐍 Python dependencies         
```

---

## 🛠️ Installation

1. **Clone this repo** & ensure Python 3.8+ 🐍
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Add raw Excel files** from the [NYC Dept. of Finance](https://www.nyc.gov/site/finance/taxes/property-rolling-sales-data.page) (2015–2025) into `data/r/`.

---

## 📒 How to Use (in 1 minute!)

### 💡 Typical Workflow

> 1. Launch Jupyter/Lab, open `main.ipynb` 🚦  
> 2. Run each cell in order:
>    - 🕵️‍♂️ **Extract:** Convert 55+ Excel sheets → clean CSV  
>    - 🧼 **Clean:** Standardize, remove dups, fix headers, normalize text  
>    - 🧮 **Metrics:** Calculate Affordability Index & Market Breadth  
>    - 📊 **Visualize:** Auto-create stunning, publication-ready figures  
>    - 💾 **Reproducible:** All data saved at each pipeline stage

Or:  
```python
from src.nyc_sales import *  # Import any module, use in your own notebook!
```

---

## 📂 Data & Official Sources

- 📅 **Annual Summaries**: Neighborhood-level Excel by borough (`2015–2024`)
- 🔄 **Rolling Sales (2025 YTD)**: Most recent 12-months at transaction level
- 📤 All data from the [NYC Department of Finance Portal](https://www.nyc.gov/site/finance/taxes/property-rolling-sales-data.page)

---

## 🎯 Core Methodology

### 📈 Metrics

| Metric              | Description                                                                         | Formula/Explanation |
|---------------------|-------------------------------------------------------------------------------------|----------------------|
| <b>🏠 Affordability Index</b>  | 25th percentile of neighborhood median/mean prices (entry-level proxy)         | <code>Q_{0.25}(P_{n,b,t})</code> <br><sub>n = neighborhood, b = borough, t = year</sub> |
| <b>🌐 Market Breadth</b>       | % neighborhoods with YoY price growth (is the boom broad?)                   | <code>(1/|N_t|) * Σ 1[P_{n,t} - P_{n,t-1} > 0]</code>        |

### 🔬 ETL Highlights

- **extract.py:** Finds headers, reconciles column names, validates schema 📑
- **clean.py:** Prunes duplicates, parses types, fixes text, normalizes fields 🧹
- **metrics.py:** Adds all required stats and custom metrics 📏
- **ingest.py:** Automates data flows 📦
- **visualize.py:** Breathtaking plots: time series, ranked bars, comparisons 🎨

---

## ❓ Research Questions We Tackle

- 💸 **How have neighborhood prices evolved across NYC since 2015?**
- 💔 **Which boroughs lost the most affordability for entry buyers?**
- 🌍 **Was post-COVID growth citywide, or just a select few neighborhoods?**
- ⏳ **Does 2025 YTD look more like 2019 or 2017 peaks?**

---

## 🎁 Project Outputs

- 🗂️ **One clean, unified dataset:** `nyc_housing_pulse_2015_2025.csv`
- 🔗 **Modular, well-documented codebase:** `src/nyc_sales/`
- 📊 **Auto-generated figures:** Find in `data/v/` or rendered in `main.ipynb`!

---

## 👥 Authors & Acknowledgments

<table>
<tr>
<td>
  <b>Harsh Golani</b> <br>
  <b>Abhishek Agarwal</b>
</td>
<td>
  <b>Group:</b> InsightLoop <br>
  <b>Course:</b> <i>DS-GA 1007 — NYU</i> <br>
  <b>Semester:</b> Fall 2025
</td>
</tr>
</table>

---

<p align="center"><sub>🟣 Data inspires the city — <b>analyze it with us!</b> 🟣</sub></p>
