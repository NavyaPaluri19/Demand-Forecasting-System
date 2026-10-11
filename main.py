
from fastapi import FastAPI
from pydantic import BaseModel 
import joblib
import pandas as pd

app = FastAPI(title="Demand Forecasting API")

model = joblib.load("models/model.pkl")
feature_cols = joblib.load("models/feature_cols.pkl")

class ForecastRequest(BaseModel):
    Store: int
    DayOfWeek: int        # 0 = Monday, 6 = Sunday
    Month: int
    Year: int
    Week: int
    IsWeekend: int        # 0 or 1
    Promo: int            # 0 or 1
    SchoolHoliday: int    # 0 or 1
    Sales_lag1: float
    Sales_lag7: float
    Sales_lag14: float
    Sales_roll7: float
    Sales_roll30: float

@app.get("/")
def root():
    return {"message": "Demand Forecasting API is running"}

@app.post("/predict")
def predict(request: ForecastRequest):
    data = pd.DataFrame([request.dict()])
    data = data[feature_cols]
    prediction = model.predict(data)[0]
    return {
        "store": request.Store,
        "predicted_sales": round(float(prediction), 2)
    }
