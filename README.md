# Demand-Forecasting-System

Store sales forecasting with XGBoost. The trained model is served through a FastAPI service, and a Streamlit dashboard shows a 14-day forecast. Training experiments are tracked with MLflow.

(Includes sample data as well)
## Project layout

```
main.py               FastAPI service (POST /predict)
dashboard.py          Streamlit dashboard, calls the API on localhost:8000
jupyter-test.ipynb    Data prep, training and MLflow tracking
Dockerfile            Container image for the API
models/               model.pkl, feature_cols.pkl (trained model)
data/                 store.csv, train_sample.csv (in git); full train.csv is not
requirements.txt      API dependencies
requirements-dev.txt  Everything: notebook, MLflow, dashboard
```

## Setup

Requires Python 3.14 (the pinned versions were built on it).

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements-dev.txt
```

Other shells: Git Bash `source .venv/Scripts/activate`, macOS/Linux `source .venv/bin/activate`, cmd `.venv\Scripts\activate.bat`.

If PowerShell blocks the activate script, run `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` once.

## Run the API

```bash
uvicorn main:app --port 8000
uvicorn main:app --port 8000
```

- Health check: http://localhost:8000/
- Interactive docs: http://localhost:8000/docs

Example request:

```bash
curl -X POST http://localhost:8000/predict -H "Content-Type: application/json" -d '{"Store":1,"DayOfWeek":0,"Month":1,"Year":2026,"Week":1,"IsWeekend":0,"Promo":0,"SchoolHoliday":0,"Sales_lag1":5000,"Sales_lag7":4800,"Sales_lag14":4700,"Sales_roll7":4900,"Sales_roll30":4850}'
```

## Run the dashboard

The API must be running first. In a second terminal (with the venv active):

```bash
streamlit run dashboard.py
```

Opens at http://localhost:8501.

## Run the API with Docker

```bash
docker build -t demand-forecasting-api .
docker run -p 8000:8000 demand-forecasting-api
```

The dashboard works unchanged against the container.

## Retrain the model

`data/` ships `store.csv` and `train_sample.csv` (stores 1-10, full date range), so the notebook runs out of the box. For the full dataset, put `train.csv` (Rossmann store sales format) in `data/`; the notebook uses it automatically when present. Then:

```bash
jupyter notebook jupyter-test.ipynb
```

Running the notebook writes `models/model.pkl` and `models/feature_cols.pkl`, and logs runs to a local `mlflow.db`. To browse experiments:

```bash
mlflow ui --backend-store-uri sqlite:///mlflow.db
```