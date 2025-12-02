<!-- Banner with emoji icons for instant visual flair -->
<h1 align='center'>🏙️ NYC Housing Pulse <span style='color:#38B6FF'>(2015–2025)</span> 📈</h1>
<p align='center'>
  <strong>Real Estate Trends, Visualized.</strong><br>
  <kbd>Affordability Index</kbd> 🏠 <kbd>Market Breadth</kbd> 🌐
</p>

---

## 🌟 Highlights

- <b>🏠 Affordability Index:</b> <span style='color:#46b946'>Entry-level housing affordability (25th percentile)</span> by borough & year
- <b>🌐 Market Breadth:</b> <span style='color:#f7c143'>Share of neighborhoods with positive yearly price growth</span>

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

main.ipynb   # 🚀 Notebook: Run the whole pipeline end-to-end!
requirements.txt   # 🐍 Python dependencies
.gitignore   # 📝 Excludes data directories and cache files
```

---

## 🛠️ Installation

1. **Clone this repo** & ensure Python 3.8+ 🐍
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
   > **Note:** 
   > - For `.xls` files (2015-2017), install `xlrd>=2.0.1`: `pip install xlrd>=2.0.1`
   > - For downloading files, install `requests`: `pip install requests`
   > - The code automatically handles both `.xls` (via xlrd) and `.xlsx` (via openpyxl) formats.
3. **Option A - Automatic Download:** Use the built-in download function in `main.ipynb` (Step 1) to fetch all files automatically.
   
   **Option B - Manual:** Download raw Excel files from the [NYC Dept. of Finance](https://www.nyc.gov/site/finance/taxes/property-rolling-sales-data.page) (2015–2025) and place them in `data/r/`.

---

## 📒 How to Use (in 1 minute!)

### 💡 Complete Workflow (7 Steps)

> 1. Launch Jupyter/Lab, open `main.ipynb` 🚦  
> 2. Run each cell in sequential order:
>    - **Step 1:** 📥 **Download** raw Excel files from NYC Dept. of Finance (55 files total)
>    - **Step 2:** 🕵️‍♂️ **Extract** Excel files → CSV with schema validation & column normalization
>    - **Step 3:** 📦 **Load** all extracted CSVs into a unified DataFrame
>    - **Step 4:** 🧼 **Clean** data (remove dupes, normalize text, parse dates, aggregate stats)
>    - **Step 5:** 🗃️ **Ingest** & aggregate by borough/neighborhood/building class/year → year-partitioned summaries
>    - **Step 6:** 🧮 **Compute** Affordability Index & Market Breadth metrics
>    - **Step 7:** 📊 **Visualize** 5 publication-quality figures answering research questions
>    - 💾 **Reproducible:** All data saved at each pipeline stage (c/, i/, p/, v/)

### 🔧 Programmatic Usage

Use the modules directly in your own scripts:

```python
from src.nyc_sales import DataExtractor, DataCleaner, DataIngester, MetricsCalculator, Visualizer

# Or import specific classes
from nyc_sales.extract import DataExtractor as de
from nyc_sales.clean import DataCleaner as dc
from nyc_sales.ingest import DataIngester as di
from nyc_sales.metrics import MetricsCalculator as mc
from nyc_sales.visualize import Visualizer as v
```

All classes follow a **singleton pattern** for efficient resource management.

### 🏗️ Technical Architecture

- **Design Pattern:** All classes implement singleton pattern to ensure single instance per class
- **Versioning:** Each method is tagged with "dogtag" version identifiers (e.g., `DataCleaner-v1.0`) for traceability
- **Error Handling:** Schema validation with detailed error messages for column mismatches
- **Data Pipeline:** ETL pipeline with clear separation of concerns (Extract → Clean → Ingest → Metrics → Visualize)
- **Reproducibility:** Each pipeline stage saves intermediate outputs for debugging and reproducibility

---

## 📂 Data & Official Sources

- 📅 **Annual Summaries (2015–2024)**: Neighborhood-level Excel files by borough, summarizing statistics by building class category
- 🔄 **Rolling Sales (2025 YTD)**: Transaction-level files for the most recent 12 months, one per borough
- 📤 **Data Source:** All data from the [NYC Department of Finance](https://www.nyc.gov/site/finance/taxes/property-rolling-sales-data.page):
  - Annualized Neighborhood Sales Summaries: `https://www.nyc.gov/assets/finance/downloads/pdf/rolling_sales/annualized-sales/{year}/{year}_{borough}.{xlsx|xls}`
  - Rolling Sales: `https://www.nyc.gov/assets/finance/downloads/pdf/rolling_sales/rollingsales_{borough}.{xlsx|xls}`
- 📊 **Coverage:** 400+ neighborhoods across 5 boroughs, 2015-2025, multiple building class categories

### 📋 Data Schema

The unified dataset (`data/i/nyc_sales_2015_2025.csv`) contains the following key columns:

| Column | Description |
|--------|-------------|
| `BOROUGH` | Borough code (1-5) |
| `BOROUGH NAME` | Borough name (Manhattan, Bronx, Brooklyn, Queens, Staten Island) |
| `NEIGHBORHOOD` | NYC Department of Finance-defined neighborhood label |
| `BUILDING CLASS CATEGORY` | High-level use/class grouping |
| `YEAR` | Calendar year (2015-2025) |
| `SALE PRICE` | Individual transaction sale price |
| `NUM SALES` | Annual transaction count per neighborhood/building class |
| `AVG SALE PRICE` | Mean sale price per group |
| `MEDIAN SALE PRICE` | Median sale price per group |
| `MIN SALE PRICE` | Minimum sale price per group |
| `MAX SALE PRICE` | Maximum sale price per group |
| `MEDIAN PRICE YOY PCT` | Year-over-year percentage change in median sale price by borough |

---

## 🎯 Core Methodology

### 📈 Metrics

| Metric              | Description                                                                         | Formula/Explanation |
|---------------------|-------------------------------------------------------------------------------------|----------------------|
| <b>🏠 Affordability Index</b>  | 25th percentile of neighborhood median/mean prices (entry-level proxy)         | <code>Q_{0.25}(P_{n,b,t})</code> <br><sub>n = neighborhood, b = borough, t = year</sub> |
| <b>🌐 Market Breadth</b>       | % neighborhoods with YoY price growth (is the boom broad?)                   | <code>(1/|N_t|) * Σ 1[P_{n,t} - P_{n,t-1} > 0]</code>        |

### 🔬 Module Details

#### 📑 **extract.py** - DataExtractor
- **Download:** Automatically fetches Excel files from NYC Dept. of Finance URLs
- **Extract:** Auto-detects header rows, normalizes column names (handles variations like "EASE-MENT" → "EASEMENT")
- **Validate:** Ensures all files match required schema (21 columns including BOROUGH, NEIGHBORHOOD, BUILDING CLASS CATEGORY, SALE PRICE, SALE DATE, etc.)
- **Engine Support:** Uses `xlrd` for legacy `.xls` files (2015-2017) and `openpyxl` for modern `.xlsx` files

#### 🧼 **clean.py** - DataCleaner
- **Deduplication:** Removes duplicate records based on key columns (BOROUGH, NEIGHBORHOOD, BUILDING CLASS CATEGORY, BLOCK, LOT, ADDRESS, etc.)
- **Header Removal:** Strips embedded header rows from concatenated Excel files
- **Normalization:** Normalizes neighborhood names (uppercase, trimmed, standardized spacing)
- **Validation:** Filters invalid/zero/negative sale prices
- **Type Conversion:** Parses dates, converts borough codes (1-5) to names (Manhattan, Bronx, Brooklyn, Queens, Staten Island)
- **Aggregation:** Computes min/mean/median/max sale price and transaction counts by borough/neighborhood/building class/year
- **YoY Metrics:** Calculates year-over-year percentage change in median sale price by borough

#### 🗃️ **ingest.py** - DataIngester
- **Aggregation:** Groups data by BOROUGH NAME, NEIGHBORHOOD, BUILDING CLASS CATEGORY, and YEAR
- **Statistics:** Computes NUM SALES, AVG SALE PRICE, MEDIAN SALE PRICE per group
- **Partitioning:** Outputs year-partitioned summary files (e.g., `2025_nyc_sales_summary.csv`)

#### 📏 **metrics.py** - MetricsCalculator
- **Affordability Index:** Calculates 25th percentile of median sale prices by borough/year (entry-level affordability proxy)
- **Market Breadth:** Computes the share of neighborhoods with positive YoY median price growth (citywide metric)
- **Output:** Generates a custom matrix combining both metrics at borough/year granularity

#### 🎨 **visualize.py** - Visualizer
- **Borough Trajectories:** Time series of median sale prices across boroughs (2015-2025) with COVID and peak markers
- **Affordability Index Plot:** Entry-level affordability trends with steepest decline annotations
- **Market Breadth Plot:** Percentage of neighborhoods with price growth over time (with 50% threshold line)
- **2025 Snapshot:** Top/bottom 10 neighborhoods by median price with 2017 and 2019 reference markers
- **Publication Quality:** All figures use consistent styling, color-blind-safe palettes, and 300 DPI resolution

---

## ❓ Research Questions We Tackle

- 💸 **How have neighborhood prices evolved across NYC since 2015?**
- 💔 **Which boroughs lost the most affordability for entry buyers?**
- 🌍 **Was post-COVID growth citywide, or just a select few neighborhoods?**
- ⏳ **Does 2025 YTD look more like 2019 or 2017 peaks?**

---

## 🎁 Project Outputs

- 🗂️ **Unified Dataset:** `data/i/nyc_sales_2015_2025.csv` - Complete cleaned dataset with all transformations
- 📊 **Year-Partitioned Summaries:** `data/p/*_nyc_sales_summary.csv` - Annual aggregated summaries
- 📈 **Metrics Matrix:** `data/p/nyc_sales_custom_matrix.csv` - Affordability Index & Market Breadth by borough/year
- 🔗 **Modular Codebase:** `src/nyc_sales/` - Well-documented, singleton-pattern classes with "dogtag" versioning
- 🖼️ **Visualizations:** 5 publication-quality figures in `data/v/`:
  - `borough_trajectories.png` - Price evolution across boroughs
  - `borough_affordability_index.png` - Entry-level affordability trends
  - `market_breadth.png` - Neighborhood participation in price growth
  - `snapshot_2025_vs_benchmarks_0.png` - Top 10 neighborhoods in 2025
  - `snapshot_2025_vs_benchmarks_1.png` - Bottom 10 neighborhoods in 2025

---

## ⚠️ Important Notes

- **Data Directories:** The `data/` subdirectories (`c/`, `i/`, `p/`, `r/`, `v/`) are excluded from version control (see `.gitignore`) to keep the repository lightweight
- **File Formats:** Older files (2015-2017) use `.xls` format, newer files use `.xlsx` - the code handles both automatically
- **Borough Codes:** Manhattan=1, Bronx=2, Brooklyn=3, Queens=4, Staten Island=5
- **Rolling Sales:** The 2025 YTD rolling sales files aggregate transactions from the most recent 12 months

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

<p align='center'><sub>🟣 Data inspires the city — <b>analyze it with us!</b> 🟣</sub></p>
