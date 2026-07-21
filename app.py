import streamlit as st
import pandas as pd
import joblib
import base64
import streamlit as st

def add_bg(image_file):

    with open(image_file, "rb") as image:
        encoded = base64.b64encode(image.read()).decode()

    st.markdown(
        f"""
        <style>

        /* ===== Background ===== */
        .stApp {{
            background-image:
            linear-gradient(
                rgba(5,15,30,0.78),
                rgba(5,15,30,0.78)
            ),
            url("data:image/png;base64,{encoded}");

            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}


        /* ===== Main Text ===== */
        h1, h2, h3, h4, h5, h6 {{
            color: white !important;
            text-shadow: 2px 2px 5px black;
        }}

        p, label {{
            color: white !important;
            text-shadow: 1px 1px 3px black;
        }}


        /* ===== Select Boxes ===== */

        div[data-baseweb="select"] > div {{
            background-color: rgba(255,255,255,0.15) !important;
            border: 1px solid rgba(255,255,255,0.35) !important;
            border-radius: 10px;
        }}


        /* Selected item text */
        div[data-baseweb="select"] span {{
            color: white !important;
        }}


        /* Dropdown menu container */
        ul[role="listbox"] {{
            background-color: rgba(10,20,40,0.95) !important;
            backdrop-filter: blur(15px);
            border-radius: 12px;
            border: 1px solid rgba(255,255,255,0.2);
        }}


        /* Dropdown items */
        li[role="option"] {{
            color: white !important;
            background-color: transparent !important;
        }}


        /* Dropdown hover */
        li[role="option"]:hover {{
            background-color: rgba(37,99,235,0.8) !important;
            color:white !important;
        }}


        /* ===== Number Inputs ===== */

        div[data-baseweb="input"] {{
            background-color: rgba(255,255,255,0.15) !important;
            border-radius: 10px;
            border:1px solid rgba(255,255,255,0.3);
        }}


        div[data-baseweb="input"] input {{
            color:white !important;
        }}


        /* ===== Metric Cards ===== */

        div[data-testid="metric-container"] {{
            background:
            rgba(0,0,0,0.45);

            border-radius:15px;
            padding:15px;

            border:1px solid rgba(255,255,255,0.25);

            backdrop-filter:blur(12px);
        }}


        /* ===== Prediction Button ===== */

        .stButton button {{
            width:100%;
            background:#2563eb;
            color:white;

            font-size:18px;
            font-weight:bold;

            border-radius:12px;
            padding:12px;

            border:none;
        }}


        .stButton button:hover {{
            background:#1d4ed8;
            color:white;
        }}


        /* ===== Sidebar ===== */

        section[data-testid="stSidebar"] {{
            background:
            rgba(0,0,0,0.65);

            backdrop-filter:blur(15px);
        }}


        </style>
        """,
        unsafe_allow_html=True
    )


# Apply your image
add_bg("Executive sales Dashboard.png")
# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="Financial Sales Forecast AI Model",
    page_icon="📊",
    layout="centered"
)

# -----------------------------
# Load Model
# -----------------------------
@st.cache_resource
def load_model():
    return joblib.load("sales_prediction_model.pkl")

model = load_model()

# -----------------------------
# Header
# -----------------------------
st.title("📊 Financial Sales Forecast AI Model"
)
st.subheader("AI Sales Prediction System")

st.write(
    "Use the trained Random Forest model to predict expected sales "
    "based on product, market, pricing, and sales factors."
)

st.divider()

# -----------------------------
# Input Features
# -----------------------------

st.subheader("Enter Sales Information")

col1, col2 = st.columns(2)

with col1:

    segment = st.selectbox(
        "Segment",
        [
            "Channel Partners",
            "Enterprise",
            "Government",
            "Midmarket",
            "Small Business"
        ]
    )

    country = st.selectbox(
        "Country",
        [
            "Canada",
            "France",
            "Germany",
            "Mexico",
            "United States of America"
        ]
    )

    product = st.selectbox(
        "Product",
        [
            "Amarilla",
            "Carretera",
            "Montana",
            "Paseo",
            "VTT",
            "Velo"
        ]
    )

    discount = st.selectbox(
        "Discount Band",
        [
            "None",
            "Low",
            "Medium",
            "High"
        ]
    )


with col2:

    units_sold = st.number_input(
        "Units Sold",
        min_value=0,
        value=100
    )

    manufacturing_price = st.number_input(
        "Manufacturing Price",
        min_value=0.0,
        value=10.0
    )

    sale_price = st.number_input(
        "Sale Price",
        min_value=0.0,
        value=20.0
    )

    month_number = st.number_input(
        "Month Number",
        min_value=1,
        max_value=12,
        value=1
    )

    year = st.number_input(
        "Year",
        min_value=2013,
        max_value=2035,
        value=2014
    )


# -----------------------------
# Prediction
# -----------------------------

st.divider()

if st.button(" Predict Sales"):

    input_data = pd.DataFrame(
        {
            "Segment": [segment],
            "Country": [country],
            "Product": [product],
            "Discount Band": [discount],
            "Units Sold": [units_sold],
            "Manufacturing Price": [manufacturing_price],
            "Sale Price": [sale_price],
            "Month Number": [month_number],
            "Year": [year]
        }
    )


    try:

        prediction = model.predict(input_data)

        predicted_sales = prediction[0]


        st.success("Prediction Completed Successfully!")

        st.metric(
            label="Predicted Sales",
            value=f"${predicted_sales:,.2f}"
        )


    except Exception as e:

        st.error("Prediction failed.")

        st.write("Error details:")
        st.code(e)


# -----------------------------
# Model Information
# -----------------------------

st.divider()

st.subheader("Model Information")

info_col1, info_col2, info_col3 = st.columns(3)

with info_col1:
    st.metric(
        "Model",
        "Random Forest"
    )

with info_col2:
    st.metric(
        "R² Score",
        "98.70%"
    )

with info_col3:
    st.metric(
        "RMSE",
        "29,093"
    )
# -----------------------------
# Power BI Dashboard
# -----------------------------

st.divider()

st.subheader("📊 Executive Power BI Dashboard")

st.write(
    "View the complete interactive financial sales analytics dashboard "
    "built with Microsoft Power BI."
)

powerbi_link = "https://app.powerbi.com/view?r=eyJrIjoiMjAzNzkxNWUtNmU3YS00M2FlLTk1OTctMjhmNDE4ZTAyOGUyIiwidCI6IjcwOGY3YjViLTIwZmMtNGJjOC05MTUwLWIxMDE1YTMwOGI5YyJ9"

st.markdown(
    f"""
    <a href="{powerbi_link}" target="_blank">
        <button style="
            background-color:#f2c811;
            color:black;
            padding:12px 25px;
            border:none;
            border-radius:10px;
            font-size:18px;
            font-weight:bold;
            cursor:pointer;">
            ↗️Open Power BI Dashboard
        </button>
    </a>
    """,
    unsafe_allow_html=True
)
# -----------------------------
# Footer
# -----------------------------

st.markdown(
    """
    <style>
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background: rgba(0,0,0,0.65);
        color: white;
        text-align: center;
        padding: 10px;
        font-size: 14px;
        backdrop-filter: blur(8px);
        border-top: 1px solid rgba(255,255,255,0.2);
    }
    </style>

    <div class="footer">
        Trained using Microsoft`s Financial Dataset by <b> Pride @ Cyber_Ninja</b>
    </div>
    """,
    unsafe_allow_html=True
)
