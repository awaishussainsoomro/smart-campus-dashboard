# ============================================================
# SMART CAMPUS ANALYTICS - INTERACTIVE DASHBOARD
# Same data generation logic as smart_campus.py, just wrapped
# in Streamlit so it becomes clickable/explorable in a browser.
# ============================================================

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(
    page_title="Smart Campus Analytics",
    page_icon="🎓",
    layout="wide"
)

np.random.seed(42)


# ------------------------------------------------------------
# Data generation (identical logic to smart_campus.py)
# ------------------------------------------------------------
@st.cache_data
def generate_data():
    n = 500

    student_id = np.arange(1, n + 1)

    age = np.random.normal(20, 1.5, n)
    age = np.clip(age, 18, 25).astype(int)

    gender = np.random.choice(["Male", "Female"], n, p=[0.5, 0.5])
    major = np.random.choice(
        ["CS", "Engineering", "Business", "Sciences", "Arts"], n
    )

    high_school_gpa = np.random.normal(3.2, 0.5, n)
    high_school_gpa = np.clip(high_school_gpa, 2.0, 4.0).round(2)

    study_hours = np.random.normal(30, 8, n)
    study_hours = np.clip(study_hours, 10, 50)

    work_hours = 30 - (study_hours * 0.5) + np.random.normal(0, 5, n)
    work_hours = np.clip(work_hours, 0, 30)

    social_hours = np.random.normal(12, 5, n)
    social_hours = np.clip(social_hours, 0, 25)

    sleep_hours = 6 + (study_hours / 50) * 2 + np.random.normal(0, 0.8, n)
    sleep_hours = np.clip(sleep_hours, 4, 9)

    current_gpa = (
        2.0
        + (study_hours / 50) * 1.5
        + (sleep_hours / 9) * 0.5
        - (work_hours / 30) * 0.7
        + np.random.normal(0, 0.2, n)
    )
    current_gpa = np.clip(current_gpa, 2.0, 4.0).round(2)

    happiness = (
        4
        + (social_hours / 25) * 3
        + (sleep_hours / 9) * 2
        + (current_gpa / 4) * 1
        + np.random.normal(0, 0.5, n)
    )
    happiness = np.clip(happiness, 1, 10).round(1)

    df = pd.DataFrame({
        "student_id": student_id,
        "age": age,
        "gender": gender,
        "major": major,
        "high_school_gpa": high_school_gpa,
        "study_hours_per_week": study_hours,
        "work_hours_per_week": work_hours,
        "social_hours_per_week": social_hours,
        "sleep_hours_per_night": sleep_hours,
        "current_gpa": current_gpa,
        "happiness_score": happiness
    })

    df["study_category"] = pd.cut(
        df["study_hours_per_week"],
        bins=[0, 20, 35, 50],
        labels=["Low", "Medium", "High"]
    )

    return df


df = generate_data()

# ------------------------------------------------------------
# Header
# ------------------------------------------------------------
st.title("🎓 Smart Campus Analytics")
st.caption("What Makes Students Successful? | Interactive Dashboard by Awais Hussain")

# ------------------------------------------------------------
# Sidebar filters
# ------------------------------------------------------------
st.sidebar.header("Filters")

selected_gender = st.sidebar.multiselect(
    "Gender", options=df["gender"].unique(), default=list(df["gender"].unique())
)

selected_major = st.sidebar.multiselect(
    "Major", options=df["major"].unique(), default=list(df["major"].unique())
)

selected_category = st.sidebar.multiselect(
    "Study Category",
    options=["Low", "Medium", "High"],
    default=["Low", "Medium", "High"]
)

filtered_df = df[
    (df["gender"].isin(selected_gender))
    & (df["major"].isin(selected_major))
    & (df["study_category"].isin(selected_category))
]

st.sidebar.markdown("---")
st.sidebar.metric("Students matching filters", len(filtered_df))

# ------------------------------------------------------------
# KPI row
# ------------------------------------------------------------
col1, col2, col3, col4 = st.columns(4)

col1.metric("Average GPA", f"{filtered_df['current_gpa'].mean():.2f}")
col2.metric("Average Happiness", f"{filtered_df['happiness_score'].mean():.1f} / 10")
col3.metric(
    "High Performers (GPA > 3.5)",
    f"{(filtered_df['current_gpa'] > 3.5).sum()}"
)
col4.metric(
    "At-Risk (GPA < 2.5)",
    f"{(filtered_df['current_gpa'] < 2.5).sum()}"
)

st.markdown("---")

# ------------------------------------------------------------
# Tabs for each analysis area
# ------------------------------------------------------------
tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ["📈 Study vs GPA", "🏫 Majors", "😀 Happiness", "💼 Work vs GPA", "🔗 Correlations"]
)

with tab1:
    st.subheader("Study Hours vs GPA")
    fig = px.scatter(
        filtered_df,
        x="study_hours_per_week",
        y="current_gpa",
        color="gender",
        trendline="ols",
        hover_data=["major", "happiness_score"],
        labels={
            "study_hours_per_week": "Study Hours per Week",
            "current_gpa": "Current GPA"
        },
        color_discrete_map={"Male": "#3b82f6", "Female": "#ef4444"}
    )
    fig.update_layout(height=500)
    st.plotly_chart(fig, use_container_width=True)
    corr_val = filtered_df["study_hours_per_week"].corr(filtered_df["current_gpa"])
    st.info(f"Correlation between study hours and GPA: **r = {corr_val:.2f}**")

with tab2:
    st.subheader("Average GPA by Major")
    major_stats = filtered_df.groupby("major")["current_gpa"].agg(["mean", "std"]).reset_index()
    fig2 = px.bar(
        major_stats,
        x="major",
        y="mean",
        error_y="std",
        labels={"mean": "Average GPA", "major": "Major"},
        color="major",
        text_auto=".2f"
    )
    fig2.update_layout(height=450, showlegend=False)
    st.plotly_chart(fig2, use_container_width=True)

    st.subheader("GPA Distribution by Study Category")
    fig2b = px.box(
        filtered_df,
        x="study_category",
        y="current_gpa",
        color="study_category",
        category_orders={"study_category": ["Low", "Medium", "High"]},
        labels={"current_gpa": "GPA", "study_category": "Study Category"}
    )
    fig2b.update_layout(height=450, showlegend=False)
    st.plotly_chart(fig2b, use_container_width=True)

with tab3:
    st.subheader("Distribution of Happiness Scores")
    fig3 = px.histogram(
        filtered_df,
        x="happiness_score",
        nbins=18,
        labels={"happiness_score": "Happiness Score"}
    )
    mean_h = filtered_df["happiness_score"].mean()
    median_h = filtered_df["happiness_score"].median()
    fig3.add_vline(x=mean_h, line_dash="dash", line_color="red",
                    annotation_text=f"Mean = {mean_h:.2f}")
    fig3.add_vline(x=median_h, line_dash="dash", line_color="blue",
                    annotation_text=f"Median = {median_h:.2f}")
    fig3.update_layout(height=450)
    st.plotly_chart(fig3, use_container_width=True)

    st.subheader("Social Hours vs Happiness")
    fig3b = px.scatter(
        filtered_df,
        x="social_hours_per_week",
        y="happiness_score",
        trendline="ols",
        labels={"social_hours_per_week": "Social Hours per Week", "happiness_score": "Happiness"}
    )
    fig3b.update_layout(height=450)
    st.plotly_chart(fig3b, use_container_width=True)

with tab4:
    st.subheader("The Cost of Working: GPA vs Work Hours")
    work_bins = [0, 5, 10, 15, 20, 25, 30]
    work_labels = ["0-5", "5-10", "10-15", "15-20", "20-25", "25-30"]
    filtered_df = filtered_df.copy()
    filtered_df["work_bin"] = pd.cut(
        filtered_df["work_hours_per_week"], bins=work_bins, labels=work_labels, include_lowest=True
    )
    grouped_work = filtered_df.groupby("work_bin", observed=True)["current_gpa"].agg(["mean", "std"]).reset_index()

    fig4 = go.Figure()
    fig4.add_trace(go.Scatter(
        x=grouped_work["work_bin"], y=grouped_work["mean"],
        mode="lines+markers", name="Average GPA", line=dict(width=3)
    ))
    fig4.add_trace(go.Scatter(
        x=grouped_work["work_bin"], y=grouped_work["mean"] + grouped_work["std"],
        mode="lines", line=dict(width=0), showlegend=False
    ))
    fig4.add_trace(go.Scatter(
        x=grouped_work["work_bin"], y=grouped_work["mean"] - grouped_work["std"],
        mode="lines", line=dict(width=0), fill="tonexty",
        fillcolor="rgba(59,130,246,0.2)", name="± 1 Std Dev"
    ))
    fig4.update_layout(
        height=450,
        xaxis_title="Work Hours Range",
        yaxis_title="Average GPA"
    )
    st.plotly_chart(fig4, use_container_width=True)

with tab5:
    st.subheader("Correlation Matrix")
    correlation_columns = [
        "study_hours_per_week", "work_hours_per_week", "social_hours_per_week",
        "sleep_hours_per_night", "current_gpa", "happiness_score"
    ]
    corr_matrix = filtered_df[correlation_columns].corr().round(2)
    fig5 = px.imshow(
        corr_matrix,
        text_auto=True,
        color_continuous_scale="RdBu_r",
        zmin=-1, zmax=1,
        aspect="auto"
    )
    fig5.update_layout(height=500)
    st.plotly_chart(fig5, use_container_width=True)

# ------------------------------------------------------------
# Raw data table
# ------------------------------------------------------------
st.markdown("---")
with st.expander("📋 View Raw Data"):
    st.dataframe(filtered_df, use_container_width=True)
    csv = filtered_df.to_csv(index=False).encode("utf-8")
    st.download_button("Download filtered data as CSV", csv, "filtered_students.csv", "text/csv")
