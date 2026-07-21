import streamlit as st
import pandas as pd
import joblib
import streamlit as st
import base64
import os

def add_bg(image_file):

    if not os.path.exists(image_file):
        st.error(f"Background image not found: {image_file}")
        return

    with open(image_file, "rb") as image:
        encoded = base64.b64encode(image.read()).decode()

    st.markdown(
        f"""
        <style>

        .stApp {{
            background-image:
            linear-gradient(
                rgba(0,0,0,0.55),
                rgba(0,0,0,0.55)
            ),
            url("data:image/png;base64,{encoded}");

            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}

        </style>
        """,
        unsafe_allow_html=True
    )


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
st.title("📊 Financial Sales Intelligence Platform")
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

if st.button("🚀 Predict Sales"):

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
