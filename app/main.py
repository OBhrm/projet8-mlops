from fastapi import FastAPI
import pandas as pd

from app.model_loader import model
from app.schemas import PredictionInput
from app.features import FEATURES


app = FastAPI()


@app.get("/")
def home():
    return {"message": "API de scoring opérationnelle"}


@app.post("/predict")
def predict(data: PredictionInput):

    # Vérification des colonnes manquantes
    missing_features = [f for f in FEATURES if f not in data.features]

    # Construction du DataFrame
    input_features = data.features.copy()

    # Compléter les colonnes manquantes avec 0
    for feature in FEATURES:
        if feature not in input_features:
            input_features[feature] = 0

    X = pd.DataFrame([input_features])
    X = X[FEATURES]

    # Prédiction
    score = model.predict(X)[0]

    return {
        "score": float(score)
    }