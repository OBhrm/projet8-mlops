from fastapi import FastAPI
import pandas as pd
import time
import numpy as np
import os
import psutil

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

    start_time = time.perf_counter()

    process = psutil.Process(os.getpid())
    process.cpu_percent(interval=None)

    input_features = {
        feature: data.features.get(feature, np.nan)
        for feature in FEATURES
    }

    X = pd.DataFrame([input_features], columns=FEATURES)

    db = SessionLocal()

    try:
        score = model.predict(X)[0]

        latency_ms = (time.perf_counter() - start_time) * 1000
        cpu_percent = process.cpu_percent(interval=None)
        memory_mb = process.memory_info().rss / (1024 * 1024)

        prediction = Prediction(
            score=float(score),

            AMT_INCOME_TOTAL=float(input_features.get("AMT_INCOME_TOTAL", 0) or 0),
            AMT_CREDIT=float(input_features.get("AMT_CREDIT", 0) or 0),
            DAYS_BIRTH=float(input_features.get("DAYS_BIRTH", 0) or 0),

            latency_ms=latency_ms,
            cpu_percent=cpu_percent,
            memory_mb=memory_mb,

            status="success",
            error_message=None,
            input_features=data.features
        )

        db.add(prediction)
        db.commit()

        return {
            "score": float(score),
            "latency_ms": latency_ms
        }

    except Exception as e:
        latency_ms = (time.perf_counter() - start_time) * 1000
        cpu_percent = process.cpu_percent(interval=None)
        memory_mb = process.memory_info().rss / (1024 * 1024)

        prediction = Prediction(
            score=None,

            AMT_INCOME_TOTAL=float(input_features.get("AMT_INCOME_TOTAL", 0) or 0),
            AMT_CREDIT=float(input_features.get("AMT_CREDIT", 0) or 0),
            DAYS_BIRTH=float(input_features.get("DAYS_BIRTH", 0) or 0),

            latency_ms=latency_ms,
            cpu_percent=cpu_percent,
            memory_mb=memory_mb,

            status="error",
            error_message=str(e),
            input_features=data.features
        )

        db.add(prediction)
        db.commit()

        raise e

    finally:
        db.close()