import streamlit as st
import pandas as pd
import requests
import matplotlib.pyplot as plt

st.title("Demand Forecasting Dashboard")
st.write("Generate a sales forecast for any store and date range")

store_id = st.selectbox("Select Store", list(range(1, 11)))
promo = st.checkbox("Promotion active?", value=False)

# Build a 14-day forecast by calling the API for each day
if st.button("Generate Forecast"):
    dates = pd.date_range(start=pd.Timestamp.today(), periods=14)
    predictions = []

    for date in dates:
        payload = {
            "Store": store_id,
            "DayOfWeek": date.dayofweek,
            "Month": date.month,
            "Year": date.year,
            "Week": int(date.isocalendar().week),
            "IsWeekend": int(date.dayofweek >= 5),
            "Promo": int(promo),
            "SchoolHoliday": 0,
            "Sales_lag1": 5000,   # placeholder values
            "Sales_lag7": 4800,
            "Sales_lag14": 4700,
            "Sales_roll7": 4900,
            "Sales_roll30": 4850,
        }
        response = requests.post("http://localhost:8000/predict", json=payload)
        predictions.append(response.json()["predicted_sales"])

    results = pd.DataFrame({"Date": dates, "Predicted Sales": predictions})

    fig, ax = plt.subplots(figsize=(12, 4))
    ax.plot(results["Date"], results["Predicted Sales"], marker='o')
    ax.set_title(f"14-Day Sales Forecast — Store {store_id}")
    ax.set_ylabel("Predicted Sales (€)")
    ax.grid(True, alpha=0.3)
    st.pyplot(fig)
    st.dataframe(results)