# Sample-Super-Store-EDA-

## 📌 Overview
This repository provides a complete, ready-to-upload Super Store data analysis project. It includes a Streamlit dashboard, EDA notebooks, preprocessing scripts, visual assets, and a detailed README/project report explaining dashboard features and key business insights.

# Super Store Sales Analysis — Repository Report

> *Project:* Interactive Dashboard & EDA for Sample Super Store dataset

---

## 🧾 Dataset

*File:* data/sample_superstore.csv (or a link to publicly available dataset). Typical columns include:

* Order ID, Order Date, Ship Date, Customer ID, Segment, Category, Sub-Category, Product Name, Sales, Quantity, Discount, Profit, Region, City, State

*Source:* (If you used Kaggle or public sample store, add the URL here.)

*Notes:* Place the raw CSV in data/. If dataset is large or proprietary, include a small sample CSV and provide download instructions in data/README.md.


---

## 🧼 Data cleaning & feature engineering (what we do)

* Parse *Order Date* and *Ship Date* as datetime.
* Remove/flag duplicates and missing critical values (Order ID, Sales, Profit).
* Convert numeric columns to float (Sales, Profit, Discount). Ensure Quantity is integer.
* Create year, month, month_year (for time series aggregation), and order_month columns.
* Aggregate sales by Category, Sub-Category, Region, City and over time for trend analysis.
* Compute KPIs: Total Sales, Total Profit, Total Quantity, Average Order Value, Profit Margin.

Implementation detail: src/data_processing.py contains load_data(path), clean_data(df), and aggregate_monthly(df) helper functions.

---

## 📊 Dashboard components and what they show

The Streamlit dashboard mirrors the screenshots and includes the following sections. For each one we document what it visualizes and the business insight to draw:

### 1. Header & File Upload

* *Component:* File uploader and date range selectors.
* *Function:* Allows user to upload a CSV and limit the analysis window via start/end dates.
* *Why:* Makes the dashboard reusable for different SuperStore datasets or time windows.

### 2. KPI Row (Top)

* *Metrics:* Total Sales, Total Profit, Total Quantity.
* *Interpretation:* Quick health check of business performance over the selected period.
* *Derived:* Show currency formatting and possible small delta indicators from previous period (optional enhancement).

### 3. Category-wise Sales (Bar Chart)

* *Plot:* Bar chart showing total sales per Category (Furniture, Office Supplies, Technology).
* *Insight:* Identify which category drives revenue. From screenshots Technology > Furniture > Office Supplies.
* *Actionable:* Focus marketing and stocking on top categories or investigate high-volume but low-margin categories.

### 4. Region-wise Sales (Donut Chart)

* *Plot:* Donut chart showing sales distribution by Region (West, East, Central, South).
* *Insight:* Regions where sales are concentrated (West appears highest in screenshots).
* *Actionable:* Regional campaigns or logistics adjustments.

### 5. Time Series Analysis (Line chart)

* *Plot:* Monthly aggregated sales over time (month_year). Shows seasonal spikes and overall trend.
* *Insight:* Identify high-sales months, seasonality, and upward/downward trends — screenshot shows large spikes toward 2017 end.
* *Actionable:* Prepare inventory and staffing for peak months, investigate outlier months for promotions.

### 6. Tree Map — Hierarchical View

* *Plot:* Treemap organized by Region → Category → Sub-Category using Sales as size.
* *Insight:* Visual hierarchical contribution of sub-categories per region. E.g., Phones in Technology are large contributors in multiple regions.
* *Actionable:* Region-specific sub-category focus.

### 7. Segment & Category Pie Charts

* *Plot:* Pie charts for Segment (Consumer, Corporate, Home Office) and category share.
* *Insight:* Consumer segment contributes the majority of sales (~50% in screenshot). Category shares reflect previous bar chart.
* *Actionable:* Personalize campaigns for dominant segments; consider SMB offers for under-indexed segments.

### 8. Month-wise Sub-Category Summary (Table)

* *Component:* Collapsible data table showing monthly sums by sub-category.
* *Insight:* Drill-down to discover which sub-categories are growing month-to-month.

---

## 🔍 Key insights (interpretation based on the dashboard screenshots)

> Use these as the reports/dashboard_insights.md narrative — they belong in your repo's reports/ folder.

1. *Technology is the largest revenue category.* — Focus: inventory and supplier relationships for Technology items like Phones, Accessories.
2. *West region generates the highest sales share.* — Consider studying promotional efficacy and customer demographics in West.
3. *Consumer segment is ~50% of sales.* — Consumer-focused UX, offers and loyalty programs may yield highest ROI.
4. *Pronounced seasonality / spikes toward year-end (Nov–Dec, and late 2017).* — Plan for marketing and inventory ahead of typical peak months.
5. *Sub-categories like Chairs, Phones, Machines show substantial size on treemap.* — These are high-impact SKUs.
6. *Profit vs Sales caution:* If any categories show large sales but low profit (or negative profit), investigate discounting, returns, or pricing strategy.

---

## ✅ Proposed extensions & advanced analyses (next steps)

* *Profitability drill-down:* show Profit Margin per sub-category and highlight negative-margin SKUs.
* *Cohort analysis* for Customer retention (if Customer ID available).
* *ARIMA / Prophet forecasting* on monthly sales for future planning.
* *Dashboard improvements:* add interactive filters (State, City, Category, Segment), export PDF, schedule daily data refresh via GitHub Actions + Streamlit Cloud.
* *A/B test results* (if marketing data available) to link promotions to spikes.

---

## 🗂 Files to include in repository (suggested content)

* src/streamlit_app.py — full Streamlit app code (well-structured with functions and caching).
* src/data_processing.py — reusable cleaning/aggregation functions.
* notebooks/01_data_exploration.ipynb — step-by-step EDA (images exported into reports/figures).
* reports/dashboard_insights.md — human-readable narrative of what dashboard shows and business recommendations.
* requirements.txt — pinned dependency versions (optional: pip-compile to generate).
* README.md — the repository landing page (this document)
* LICENSE — e.g., MIT License.

---

## 📝 Suggested content for reports/dashboard_insights.md (short example)

> *Executive Summary*
> 
>Between 2014 and 2017, total sales were *$2.29M* with a total profit of *$286k* (as shown in KPI header). Technology drove the largest share of revenue, and the West region contributed the most sales. The Consumer segment is the primary buyer. Strong seasonal spikes appear at year-end, indicating promotional periods or shopping seasons.
> 
---
## ⚙️ How to run (Local)

1. Clone the repository

bash
git clone https://github.com/<your-username>/super-store-eda.git
cd super-store-eda


2. Create virtual environment & install dependencies

bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate
pip install -r requirements.txt


3. Put sample_superstore.csv into data/ or update src/data_processing.py to point to the dataset path.
4. Run Jupyter notebooks for the EDA (optional)

bash
jupyter lab notebooks/01_data_exploration.ipynb


5. Run Streamlit dashboard

bash
streamlit run src/streamlit_app.py


---

## 🧩 Tech stack & dependencies

* Python 3.8+
* pandas, numpy
* matplotlib, plotly.express
* streamlit
* seaborn (optional for static plots in notebooks)
* scikit-learn (optional for feature transformations or basic models)

A minimal requirements.txt (examples):


pandas
numpy
streamlit
plotly
matplotlib
seaborn
scikit-learn
openpyxl
