from fastapi import FastAPI
import pandas as pd
import time
import numpy as np

from app.model_loader import model
from app.schemas import PredictionInput
from app.features import FEATURES
from app.database import SessionLocal
from app.models import Prediction
from app.database import engine
from app.models import Base


Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/")
def home():
    return {"message": "API de scoring opérationnelle"}


@app.post("/predict")
def predict(data: PredictionInput):

    start_time = time.time()

    # Vérification des colonnes manquantes
    missing_features = [f for f in FEATURES if f not in data.features]

    # Construction des features d'entrée
    input_features = data.features.copy()

    # Ajout des colonnes manquantes avec NAN
    for feature in FEATURES:
        if feature not in input_features:
            input_features[feature] = np.nan

    # Construction du DataFrame dans le bon ordre
    X = pd.DataFrame([input_features])
    X = X[FEATURES]

    db = SessionLocal()

    try:

        # Prédiction
        score = model.predict(X)[0]

        # Temps d'exécution
        latency_ms = (time.time() - start_time) * 1000

        # Sauvegarde dans PostgreSQL (Neon)
        prediction = Prediction(
            score=float(score),

            AMT_INCOME_TOTAL=float(input_features.get("AMT_INCOME_TOTAL", 0)),
            AMT_CREDIT=float(input_features.get("AMT_CREDIT", 0)),
            DAYS_BIRTH=float(input_features.get("DAYS_BIRTH", 0)),

            latency_ms=latency_ms,
            status="success",
            error_message=None,

            input_features=data.features
        )

        db.add(prediction)
        db.commit()

        return {
            "score": float(score)
        }

    except Exception as e:

        latency_ms = (time.time() - start_time) * 1000

        # Enregistrement de l'erreur dans Neon
        prediction = Prediction(
            score=None,

            AMT_INCOME_TOTAL=float(input_features.get("AMT_INCOME_TOTAL", 0)),
            AMT_CREDIT=float(input_features.get("AMT_CREDIT", 0)),
            DAYS_BIRTH=float(input_features.get("DAYS_BIRTH", 0)),

            latency_ms=latency_ms,
            status="error",
            error_message=str(e),

            input_features=data.features
        )

        db.add(prediction)
        db.commit()

        raise e

    finally:
        db.close()