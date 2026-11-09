import streamlit as st
import pandas as pd
import plotly.express as px

# ==================================
# PAGE CONFIG
# ==================================

FILE_PATH = "MPC Data.xlsx"

st.set_page_config(
    page_title="MPC Dashboard",
    layout="wide"
)

# ==================================
# LOAD DATA
# ==================================

historical = pd.read_excel(
    FILE_PATH,
    sheet_name="Historical Data"
)

annual = pd.read_excel(
    FILE_PATH,
    sheet_name="Annual Inflation"
)

# ==================================
# SIDEBAR
# ==================================

st.sidebar.title("MPC Dashboard")

page = st.sidebar.radio(
    "Navigation",
    [
        "Executive Dashboard",
        "Forecast Analysis",
        "Inflation Drivers",
        "Lag Transmission",
        "Model Diagnostics"
    ]
)

# ==================================
# EXECUTIVE DASHBOARD
# ==================================

if page == "Executive Dashboard":

    st.title("📈 Monetary Policy Committee Dashboard")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Latest Inflation",
            "54.1%"
        )

    with col2:
        st.metric(
            "Annual Inflation Avg",
            "31.45%"
        )

    with col3:
        st.metric(
            "Forecast Accuracy",
            "98%"
        )

    with col4:
        st.metric(
            "Policy Signal",
            "HAWKISH"
        )

    st.subheader("MPC Snapshot")

    st.success(
        """
        Inflation remains elevated at 54.1%, with annual
        inflation averaging 31.45% in 2022.

        The forecasting model demonstrates strong
        performance with an R² of approximately 0.98.

        Credit-to-Deposit Ratio, Inflation Persistence
        and Non-Food Inflation remain the dominant
        drivers of inflationary pressures.

        Current conditions support a relatively
        hawkish monetary policy stance.
        """
    )

    annual_chart = annual.copy()

    annual_chart["Inflation (%)"] = (
        annual_chart["Headline Inflation (%)"] * 100
    )

    st.subheader(
        "Ghana Inflation Trend (2009-2022)"
    )

    fig = px.line(
        annual_chart,
        x="Year",
        y="Inflation (%)",
        markers=True
    )

    fig.update_yaxes(
        ticksuffix="%"
    )

    fig.update_layout(
        template="plotly_white",
        height=500
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# ==================================
# FORECAST ANALYSIS
# ==================================

elif page == "Forecast Analysis":

    st.title("📉 Forecast Analysis")

    forecast = pd.read_excel(
        FILE_PATH,
        sheet_name="Forecast Output"
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("R²", "98%")

    with col2:
        st.metric("MAE", "0.0052")

    with col3:
        st.metric("RMSE", "0.0079")

    with col4:
        st.metric("Forecast Accuracy", "98%")

    chart_df = forecast.copy()

    chart_df["Actual (%)"] = (
        chart_df["Actual_Inflation"] * 100
    )

    chart_df["Predicted (%)"] = (
        chart_df["Predicted_Inflation"] * 100
    )

    fig = px.line(
        chart_df,
        x="Date",
        y=["Actual (%)", "Predicted (%)"],
        title="Actual vs Predicted Inflation"
    )

    fig.update_yaxes(
        ticksuffix="%"
    )

    fig.update_layout(
        template="plotly_white",
        height=550
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# ==================================
# INFLATION DRIVERS
# ==================================

elif page == "Inflation Drivers":

    st.title("📊 Inflation Drivers")

    feature_df = pd.read_excel(
        FILE_PATH,
        sheet_name="XGBoost_Feature",
        header=1
    )

    feature_df = feature_df[
        ["feature", "importance"]
    ]

    feature_df["importance"] = (
        feature_df["importance"] * 100
    )

    feature_df = feature_df.sort_values(
        "importance",
        ascending=False
    )

    top6 = feature_df.head(6)

    fig = px.bar(
        top6,
        x="importance",
        y="feature",
        orientation="h",
        text="importance",
        color="importance",
        color_continuous_scale="Blues"
    )

    fig.update_traces(
        texttemplate="%{text:.1f}%"
    )

    fig.update_layout(
        template="plotly_white",
        height=550,
        yaxis=dict(
            categoryorder="total ascending"
        )
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.success(
        """
        Inflation pressures are primarily driven by
        credit expansion, inflation persistence and
        non-food inflation developments.

        Credit-to-Deposit Ratio is the most influential
        predictor of inflation in the model.
        """
    )

# ==================================
# LAG TRANSMISSION
# ==================================

elif page == "Lag Transmission":

    st.title("⏳ Lag Transmission Analysis")

    lag_data = pd.DataFrame({

        "Variable": [
            "Gold Price",
            "Oil Price",
            "Cocoa Price",
            "Private Sector Credit",
            "Monetary Policy Rate"
        ],

        "Transmission Lag (Months)": [
            12,
            6,
            6,
            1,
            0
        ]
    })

    fig = px.bar(
        lag_data,
        x="Transmission Lag (Months)",
        y="Variable",
        orientation="h",
        text="Transmission Lag (Months)",
        color="Transmission Lag (Months)",
        color_continuous_scale="Oranges"
    )

    fig.update_layout(
        template="plotly_white",
        height=550,
        yaxis=dict(
            categoryorder="total ascending"
        )
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.dataframe(lag_data)

# ==================================
# MODEL DIAGNOSTICS
# ==================================

elif page == "Model Diagnostics":

    st.title("🔍 Model Diagnostics")

    st.metric(
        "R²",
        "98%"
    )

    st.metric(
        "RMSE",
        "0.0079"
    )

    st.metric(
        "MAE",
        "0.0052"
    )

    st.info(
        """
        Model diagnostics indicate strong predictive
        performance and low forecast errors.

        Interpretation of OLS coefficients should be
        complemented with XGBoost feature importance
        and lag transmission analysis.
        """
    )
    git commit -m "Initial MPC Dashboard"