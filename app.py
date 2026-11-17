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
            "Inflation Rate (Dec 2022)",
            "54.1%"
        )

    with col2:
        st.metric(
            "Avg. Inflation (2022)",
            "31.45%"
        )

    with col3:
        st.metric(
            "Model Accuracy",
            "98%"
        )

    with col4:
        st.metric(
            "Policy Stance",
            "HAWKISH"
        )

    st.subheader("MPC Snapshot")

    st.success(
        """
Headline inflation ended 2022 at 54.1%, significantly above historical trends and indicative of substantial price pressures within the economy.

Inflation persistence remains elevated, suggesting that inflationary dynamics continue to carry over between periods.

Credit-to-Deposit Ratio, Inflation Lag and Non-Food Inflation are the most influential predictors of inflation within the forecasting model.

The overall macroeconomic environment supports a hawkish monetary policy stance aimed at restoring price stability.

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



# =====================================================
# FORECAST ANALYSIS
# =====================================================

elif page == "Forecast Analysis":

    st.title("📉 Forecast Analysis")

    # Load Forecast Data
    forecast = pd.read_excel(
        FILE_PATH,
        sheet_name="Forecast Output"
    )

    # ============================
    # KPI SECTION
    # ============================
    st.subheader("Model Performance")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("R²", "98%")

    with col2:
        st.metric("MAE", "0.0052")

    with col3:
        st.metric("RMSE", "0.0079")

    with col4:
        st.metric("Forecast Accuracy", "98%")

    st.markdown("---")

    # ============================
    # MODEL INTERPRETATION
    # ============================
    st.success(
        """
        The XGBoost model demonstrates strong predictive
        performance, explaining approximately 98% of
        inflation movements in the dataset.

        Low MAE and RMSE values indicate minimal forecast
        errors and high reliability of inflation predictions.
        """
    )

    # ============================
    # PREPARE DATA
    # ============================

    chart_df = forecast.copy()

    chart_df["Actual (%)"] = (
        chart_df["Actual_Inflation"] * 100
    )

    chart_df["Predicted (%)"] = (
        chart_df["Predicted_Inflation"] * 100
    )

    # ============================
    # ACTUAL VS PREDICTED CHART
    # ============================

    st.subheader("Actual vs Predicted Inflation")

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
        height=550,
        legend_title=""
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # ============================
    # FORECAST ERROR ANALYSIS
    # ============================

    chart_df["Error (%)"] = (
        chart_df["Actual (%)"]
        - chart_df["Predicted (%)"]
    )

    st.subheader("Forecast Error Analysis")

    error_fig = px.bar(
        chart_df,
        x="Date",
        y="Error (%)",
        title="Forecast Errors"
    )

    error_fig.update_layout(
        template="plotly_white",
        height=400
    )

    st.plotly_chart(
        error_fig,
        use_container_width=True
    )

    # ============================
    # FORECAST OUTPUT TABLE
    # ============================

    st.subheader("Forecast Results")

    st.dataframe(
        chart_df[
            [
                "Date",
                "Actual (%)",
                "Predicted (%)",
                "Error (%)"
            ]
        ],
        use_container_width=True
    )

    # ============================
    # MPC INSIGHTS
    # ============================

    st.subheader("Monetary Policy Insights")

    st.info(
        """
        • The model closely tracks historical inflation movements.

        • Forecast errors remain relatively low across the sample.

        • Major inflation turning points are accurately captured.

        • The model can serve as a supporting tool for
          Monetary Policy Committee (MPC) discussions.

        • Results should complement economic judgement,
          macroeconomic analysis and policy assessment.
        """
    )

    st.markdown("---")

    st.caption(
        "MPC Dashboard | Ghana Inflation Forecasting using XGBoost"
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

# =====================================================
# LAG TRANSMISSION
# =====================================================

elif page == "Lag Transmission":

    st.title("⏳ Lag Transmission Analysis")

    st.markdown("""
    This page shows how long selected macroeconomic variables
    take to transmit their impact to inflation.
    
    Understanding transmission lags helps policymakers assess
    the timing of monetary policy actions and other economic shocks.
    """)

    # =====================================
    # LOAD DATA
    # =====================================

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

    # =====================================
    # KPI CARDS
    # =====================================

    st.subheader("Lag Summary")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Longest Lag",
            "12 Months"
        )

    with col2:
        st.metric(
            "Shortest Lag",
            "0 Months"
        )

    with col3:
        st.metric(
            "Average Lag",
            "5 Months"
        )

    # =====================================
    # BAR CHART
    # =====================================

    st.subheader("Transmission Lag by Variable")

    fig = px.bar(
        lag_data,
        x="Transmission Lag (Months)",
        y="Variable",
        orientation="h",
        text="Transmission Lag (Months)",
        color="Transmission Lag (Months)",
        color_continuous_scale="Oranges",
        title="Lag Structure of Inflation Drivers"
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

    # =====================================
    # TABLE
    # =====================================

    st.subheader("Lag Data")

    st.dataframe(
        lag_data,
        use_container_width=True
    )

    # =====================================
    # INTERPRETATION
    # =====================================

    st.subheader("Policy Interpretation")

    st.info(
        """
        • Gold price changes take approximately 12 months
        to fully affect inflation.

        • Oil price movements influence inflation after
        roughly 6 months.

        • Cocoa price effects are observed after
        approximately 6 months.

        • Private sector credit impacts inflation after
        around 1 month.

        • Monetary Policy Rate adjustments have an
        immediate effect in the model.
        """
    )

    # =====================================
    # MPC INSIGHTS
    # =====================================

    st.subheader("Monetary Policy Insights")

    st.success(
        """
        The results suggest that commodity prices operate
        through relatively long transmission channels,
        while monetary policy and credit conditions affect
        inflation more rapidly.

        Policymakers should therefore adopt a forward-looking
        approach when responding to inflation pressures,
        particularly those driven by external commodity shocks.
        """
    )

    st.markdown("---")

    st.caption(
        "MPC Dashboard | Ghana Inflation Transmission Analysis"
    )
# =====================================================
# MODEL DIAGNOSTICS
# =====================================================

elif page == "Model Diagnostics":

    st.title("🔍 Model Diagnostics")

    st.markdown("""
    This section evaluates the overall performance of the
    inflation forecasting model.
    """)

    # =====================================
    # KPI CARDS
    # =====================================

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "R²",
            "98%"
        )

    with col2:
        st.metric(
            "MAE",
            "0.0052"
        )

    with col3:
        st.metric(
            "RMSE",
            "0.0079"
        )

    with col4:
        st.metric(
            "Model Accuracy",
            "98%"
        )

    st.markdown("---")

    # =====================================
    # PERFORMANCE SCORE
    # =====================================

    st.subheader("Model Health")

    st.progress(98)

    st.success("""
    The model achieved excellent predictive performance,
    explaining approximately 98% of inflation variation.
    Forecast errors remain very low across observations.
    """)

    # =====================================
    # METRIC DEFINITIONS
    # =====================================

    st.subheader("Metric Interpretation")

    metric_df = pd.DataFrame({

        "Metric": [
            "R²",
            "MAE",
            "RMSE"
        ],

        "Value": [
            "98%",
            "0.0052",
            "0.0079"
        ],

        "Interpretation": [

            "Excellent explanatory power",

            "Average forecast error is very small",

            "Prediction errors remain low"

        ]

    })

    st.dataframe(
        metric_df,
        use_container_width=True
    )

    # =====================================
    # PERFORMANCE CHART
    # =====================================

    st.subheader("Diagnostic Summary")

    diagnostics = pd.DataFrame({

        "Metric": [
            "R²",
            "Accuracy"
        ],

        "Score": [
            98,
            98
        ]

    })

    fig = px.bar(
        diagnostics,
        x="Metric",
        y="Score",
        text="Score",
        color="Score",
        color_continuous_scale="Greens",
        title="Model Performance Indicators"
    )

    fig.update_layout(
        template="plotly_white",
        height=450
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # =====================================
    # MPC INTERPRETATION
    # =====================================

    st.subheader("Economic Interpretation")

    st.info("""
    • The model exhibits strong predictive accuracy.

    • Forecast errors are small and stable.

    • Results support inflation forecasting for monetary
      policy analysis.

    • Feature importance and lag transmission analysis
      should be reviewed alongside diagnostic metrics.

    • Model output should complement expert judgement
      rather than replace policy deliberation.
    """)

    # =====================================
    # FINAL ASSESSMENT
    # =====================================

    st.subheader("Overall Assessment")

    st.success("""
    Based on R², MAE and RMSE results, the XGBoost model
    demonstrates a high degree of reliability for forecasting
    inflation dynamics in Ghana.

    The model is suitable as a decision-support tool for
    Monetary Policy Committee discussions.
    """)

    st.markdown("---")

    st.caption(
        "MPC Dashboard | Model Diagnostics"
    )