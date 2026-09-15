# 🎓 Smart Campus Analytics Dashboard

An interactive data analysis dashboard exploring what drives student success | built on a synthetic dataset of 500 students with deliberately engineered correlations between study habits, work hours, sleep, and academic performance.

**🔗 Live demo:** [(https://smart-campus-dashboard-d25s24j6kmawh8cq9fzblu.streamlit.app/)]

---

## About

This started as a Python for Data Science assignment analyzing student success factors using NumPy, Pandas, and Matplotlib. This repo extends that original analysis into a full interactive web app, so the findings are genuinely explorable instead of fixed images, filter the data and watch every chart and metric update live.

## Features

- **Live KPI cards** — average GPA, average happiness, high performer count, and at-risk student count, all recalculated instantly as filters change
- **Sidebar filters** — gender, major, and study category, applied across the entire dashboard at once
- **5 analysis tabs:**
  - 📈 Study Hours vs GPA — scatter plot with trend line and live correlation coefficient
  - 🏫 Majors — average GPA per major with error bars, plus a GPA distribution boxplot by study category
  - 😀 Happiness — score distribution with mean/median markers, and social hours vs happiness
  - 💼 Work vs GPA — binned work-hour analysis with a shaded standard-deviation band
  - 🔗 Correlations — full interactive correlation heatmap across all numeric variables
- **Downloadable data** — export the currently filtered subset as CSV
- All charts built with Plotly, so every plot supports hover tooltips, zoom, and pan

## Tech Stack

- **Python** — core language
- **Pandas / NumPy** — data generation and statistical analysis
- **Plotly** — interactive charting
- **Streamlit** — web app framework and hosting

## How the data works

The dataset is synthetically generated (`np.random.seed(42)` for reproducibility) with intentional relationships built into the formulas — for example, work hours are modeled to decrease as study hours increase, and GPA is calculated as a weighted combination of study hours, sleep, and work hours. This mirrors how real academic datasets tend to behave, without using any real student records.

## Running locally

```bash
git clone https://github.com/awaishussainsoomro/smart-campus-dashboard.git
cd smart-campus-dashboard
pip install -r requirements.txt
streamlit run app.py
```

The app will open automatically in your browser at `http://localhost:8501`.

## Deployment

Deployed for free on [Streamlit Community Cloud](https://share.streamlit.io), connected directly to this repository.

## Author

**Awais Hussain Soomro**
BSCS Student, University of Larkano
[GitHub](https://github.com/awaishussainsoomro)
