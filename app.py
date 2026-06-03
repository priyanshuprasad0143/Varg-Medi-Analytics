import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

from auth import auth_screen
from admin import admin_panel
from pdf_report import generate_pdf_report
from dashboard.forecast import (
    predict_sales,
    future_forecast
)

# ---------------------------------
# PAGE CONFIG
# ---------------------------------
st.set_page_config(
    page_title="Varg-Medi Analytics",
    page_icon="💊",
    layout="wide"
)

# ---------------------------------
# LOAD CUSTOM CSS
# ---------------------------------
def load_css():
    with open(
        "assets/style.css"
    ) as f:
        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True
        )

load_css()

# ---------------------------------
# LOGIN CHECK
# ---------------------------------
if "logged_in" not in st.session_state:
    st.session_state[
        "logged_in"
    ] = False

if not st.session_state[
    "logged_in"
]:
    auth_screen()
    st.stop()

# ---------------------------------
# ADMIN ACCESS
# ---------------------------------
if (
    st.session_state.get(
        "username"
    ) == "admin"
):
    admin_panel()

    if st.sidebar.button(
        "Logout"
    ):
        st.session_state[
            "logged_in"
        ] = False

        st.rerun()

    st.stop()

# ---------------------------------
# SIDEBAR
# ---------------------------------
st.sidebar.success(
    f"👋 Welcome "
    f"{st.session_state['username']}"
)

if st.sidebar.button(
    "Logout"
):
    st.session_state[
        "logged_in"
    ] = False

    st.rerun()

# ---------------------------------
# TITLE
# ---------------------------------
st.title(
    "💊 Varg-Medi Analytics"
)

st.caption(
    "AI Powered Healthcare "
    "and Medicine Analytics"
)

# ---------------------------------
# LOAD DATA
# ---------------------------------
st.sidebar.header(
    "📂 Dataset"
)

uploaded_file = (
    st.sidebar.file_uploader(
        "Upload CSV File",
        type=["csv"]
    )
)

if uploaded_file is not None:
    df = pd.read_csv(
        uploaded_file
    )
else:
    df = pd.read_csv(
        "data/medicine_sales.csv"
    )

# ---------------------------------
# FILTERS
# ---------------------------------
st.sidebar.header(
    "🔍 Filters"
)

selected_month = (
    st.sidebar.multiselect(
        "Select Month",
        options=df[
            "Month"
        ].unique(),
        default=df[
            "Month"
        ].unique()
    )
)

selected_category = (
    st.sidebar.multiselect(
        "Select Category",
        options=df[
            "Category"
        ].unique(),
        default=df[
            "Category"
        ].unique()
    )
)

medicine_search = (
    st.sidebar.text_input(
        "Search Medicine"
    )
)

filtered_df = df[
    (
        df["Month"]
        .isin(
            selected_month
        )
    )
    &
    (
        df["Category"]
        .isin(
            selected_category
        )
    )
]

if medicine_search:
    filtered_df = (
        filtered_df[
            filtered_df[
                "Medicine_Name"
            ].str.contains(
                medicine_search,
                case=False
            )
        ]
    )

# ---------------------------------
# KPI CALCULATIONS
# ---------------------------------
total_revenue = (
    filtered_df[
        "Revenue"
    ].sum()
)

total_units = (
    filtered_df[
        "Units_Sold"
    ].sum()
)

stock_left = (
    filtered_df[
        "Stock_Left"
    ].sum()
)

avg_price = round(
    filtered_df[
        "Price_Per_Unit"
    ].mean(),
    2
)

predicted_sales = (
    predict_sales(
        filtered_df
    )
)

top_revenue_med = (
    filtered_df.groupby(
        "Medicine_Name"
    )["Revenue"]
    .sum()
    .idxmax()
)

best_category = (
    filtered_df.groupby(
        "Category"
    )["Revenue"]
    .sum()
    .idxmax()
)

best_month = (
    filtered_df.groupby(
        "Month"
    )["Revenue"]
    .sum()
    .idxmax()
)

# ---------------------------------
# KPI SECTION
# ---------------------------------
col1, col2, col3, col4, col5 = (
    st.columns(5)
)

col1.metric(
    "💰 Revenue",
    f"₹{total_revenue:,}"
)

col2.metric(
    "💊 Units Sold",
    total_units
)

col3.metric(
    "📦 Stock Left",
    stock_left
)

col4.metric(
    "💵 Avg Price",
    f"₹{avg_price}"
)

col5.metric(
    "📈 Prediction",
    predicted_sales
)

st.divider()

# ---------------------------------
# SMART INSIGHTS
# ---------------------------------
st.subheader(
    "🧠 Smart Insights"
)

col6, col7, col8 = (
    st.columns(3)
)

with col6:
    st.success(
        f"🏆 Top Medicine: "
        f"{top_revenue_med}"
    )

with col7:
    st.info(
        f"📊 Best Category: "
        f"{best_category}"
    )

with col8:
    st.warning(
        f"📅 Best Month: "
        f"{best_month}"
    )

# ---------------------------------
# PDF REPORT
# ---------------------------------
st.subheader(
    "📄 Generate Report"
)

if st.button(
    "Generate PDF"
):
    pdf_path = generate_pdf_report(
        total_revenue,
        total_units,
        stock_left,
        avg_price,
        predicted_sales,
        top_revenue_med,
        best_category,
        best_month
    )

    with open(
        pdf_path,
        "rb"
    ) as pdf_file:

        st.download_button(
            label="⬇ Download PDF",
            data=pdf_file,
            file_name=(
                "varg_medi_report.pdf"
            ),
            mime=(
                "application/pdf"
            )
        )

# ---------------------------------
# CHARTS
# ---------------------------------
st.subheader(
    "📊 Analytics"
)

medicine_revenue = (
    filtered_df.groupby(
        "Medicine_Name",
        as_index=False
    )["Revenue"]
    .sum()
)

fig1 = px.bar(
    medicine_revenue,
    x="Medicine_Name",
    y="Revenue",
    title="Revenue by Medicine"
)

monthly_sales = (
    filtered_df.groupby(
        "Month",
        as_index=False
    )["Revenue"]
    .sum()
)

fig2 = px.line(
    monthly_sales,
    x="Month",
    y="Revenue",
    markers=True,
    title="Monthly Revenue Trend"
)

col9, col10 = st.columns(2)

with col9:
    st.plotly_chart(
        fig1,
        use_container_width=True
    )

with col10:
    st.plotly_chart(
        fig2,
        use_container_width=True
    )

# ---------------------------------
# FORECAST
# ---------------------------------
st.subheader(
    "📈 6 Month Forecast"
)

forecast_df = (
    future_forecast(
        filtered_df
    )
)

forecast_fig = px.line(
    forecast_df,
    x="Month",
    y="Predicted_Sales",
    markers=True
)

st.plotly_chart(
    forecast_fig,
    use_container_width=True
)

# ---------------------------------
# HEATMAP
# ---------------------------------
st.subheader(
    "🔥 Correlation Heatmap"
)

numeric_df = (
    filtered_df.select_dtypes(
        include=["number"]
    )
)

fig, ax = plt.subplots(
    figsize=(8, 5)
)

sns.heatmap(
    numeric_df.corr(),
    annot=True,
    ax=ax
)

st.pyplot(fig)

# ---------------------------------
# DATASET
# ---------------------------------
st.subheader(
    "📋 Dataset"
)

st.dataframe(
    filtered_df,
    use_container_width=True
)