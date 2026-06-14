from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager
from app.schemas import PredictRequest, PredictResponse, HealthResponse
from app.model import model_manager
import pandas as pd

@asynccontextmanager
async def lifespan(app: FastAPI):
    model_manager.load()
    yield

app = FastAPI(
    title="Churn Prediction API",
    description="Prédit si un client télécom va résilier son abonnement",
    version="2.0.0",
    lifespan=lifespan
)

def encode_input(request: PredictRequest) -> dict:
    """Convertit la requête en dict encodé identique au training."""
    data = request.model_dump()

    # Encoder les binaires comme LabelEncoder l'a fait
    binary_map = {"Yes": 1, "No": 0, "Male": 1, "Female": 0}
    binary_cols = ["gender", "Partner", "Dependents", "PhoneService", "PaperlessBilling"]
    for col in binary_cols:
        data[col] = binary_map.get(data[col], data[col])

    return data

@app.get("/health", response_model=HealthResponse)
def health_check():
    return HealthResponse(
        status="ok",
        model_loaded=model_manager.is_loaded()
    )

@app.post("/predict", response_model=PredictResponse)
def predict(request: PredictRequest):
    try:
        data = encode_input(request)
        prediction, probability, threshold = model_manager.predict(data)

        label = "Churn probable" if prediction == 1 else "Client fidèle"

        if probability >= 0.75:
            risk_level = "Élevé"
        elif probability >= 0.50:
            risk_level = "Moyen"
        else:
            risk_level = "Faible"

        return PredictResponse(
            prediction=prediction,
            probability=probability,
            threshold=threshold,
            label=label,
            risk_level=risk_level
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))