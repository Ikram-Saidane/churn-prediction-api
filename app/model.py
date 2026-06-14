import joblib
import numpy as np
import pandas as pd
from pathlib import Path

MODEL_PATH     = Path(__file__).parent.parent / "model" / "model.pkl"
SCALER_PATH    = Path(__file__).parent.parent / "model" / "scaler.pkl"
THRESHOLD_PATH = Path(__file__).parent.parent / "model" / "threshold.pkl"
FEATURES_PATH  = Path(__file__).parent.parent / "model" / "feature_names.pkl"

BINARY_MAP = {"Yes": 1, "No": 0, "Male": 1, "Female": 0}
BINARY_COLS = ["gender", "Partner", "Dependents", "PhoneService", "PaperlessBilling"]

DUMMIES_COLS = [
    "MultipleLines", "InternetService", "OnlineSecurity", "OnlineBackup",
    "DeviceProtection", "TechSupport", "StreamingTV", "StreamingMovies",
    "Contract", "PaymentMethod"
]

def add_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df['charges_per_month_tenure'] = df['MonthlyCharges'] / (df['tenure'] + 1)
    df['total_charges_ratio'] = df['TotalCharges'] / (df['MonthlyCharges'] * (df['tenure'] + 1) + 1)
    df['is_new_client']   = (df['tenure'] <= 6).astype(int)
    df['is_loyal_client'] = (df['tenure'] >= 48).astype(int)
    df['high_spender']    = (df['MonthlyCharges'] >= 70).astype(int)
    return df

def preprocess(data: dict, feature_names: list) -> pd.DataFrame:
    df = pd.DataFrame([data])

    # 1. Encoder les binaires
    for col in BINARY_COLS:
        if col in df.columns:
            df[col] = df[col].map(BINARY_MAP)

    # 2. One-hot encoding sur les colonnes multi-classes
    df = pd.get_dummies(df, columns=DUMMIES_COLS, drop_first=True)

    # 3. Feature engineering
    df = add_features(df)

    # 4. Aligner exactement sur les colonnes du training
    for col in feature_names:
        if col not in df.columns:
            df[col] = 0  # colonne manquante → 0

    df = df[feature_names]  # ordre exact
    return df

class ModelManager:
    def __init__(self):
        self._model     = None
        self._scaler    = None
        self._threshold = 0.5
        self._features  = None

    def load(self):
        self._model     = joblib.load(MODEL_PATH)
        self._scaler    = joblib.load(SCALER_PATH)
        self._threshold = joblib.load(THRESHOLD_PATH)
        self._features  = joblib.load(FEATURES_PATH)
        print(f"Modèle chargé | Seuil : {self._threshold:.3f} | "
              f"Features : {len(self._features)}")

    def is_loaded(self) -> bool:
        return self._model is not None

    def predict(self, data: dict) -> tuple[int, float, float]:
        df = preprocess(data, self._features)
        X_scaled    = self._scaler.transform(df)
        probability = float(self._model.predict_proba(X_scaled)[0][1])
        prediction  = int(probability >= self._threshold)
        return prediction, round(probability, 3), round(self._threshold, 3)

model_manager = ModelManager()