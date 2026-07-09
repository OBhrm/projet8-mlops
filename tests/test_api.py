from fastapi.testclient import TestClient
from app.main import app
import json
import os

API_KEY = os.getenv("API_KEY", "ma_cle_api_super_secrete")
HEADERS = {"x-api-key": API_KEY}

client = TestClient(app)


# Vérification de l'API : API démarre et retourne un message de bienvenue
def test_home():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "message": "API de scoring opérationnelle"
    }


# Vérification que l'API refuse une requête sans clé API
def test_predict_without_api_key():

    response = client.post(
        "/predict",
        json={"features": {}}
    )

    assert response.status_code == 401


# Vérification de l'endpoint de prédiction : endpoint /predict fonctionne,
# modèle bien chargé, réponse contient un score
def test_predict_empty_features():

    response = client.post(
        "/predict",
        headers=HEADERS,
        json={"features": {}}
    )

    assert response.status_code == 200

    result = response.json()

    assert "score" in result


# Vérification de l'endpoint de prédiction avec un échantillon réel
def test_predict_real_sample():

    with open("data/sample_request.json", encoding="utf-8") as file:
        payload = json.load(file)

    response = client.post(
        "/predict",
        headers=HEADERS,
        json=payload
    )

    assert response.status_code == 200

    result = response.json()

    assert "score" in result
    assert result["score"] in [0.0, 1.0]


# Vérification d'entrée invalide : retourne une erreur 422
def test_predict_invalid_input():

    response = client.post(
        "/predict",
        headers=HEADERS,
        json={"features": "bonjour"}
    )

    assert response.status_code == 422


# Vérification d'entrée partielle
def test_predict_partial_features():

    response = client.post(
        "/predict",
        headers=HEADERS,
        json={
            "features": {
                "AMT_INCOME_TOTAL": 150000
            }
        }
    )

    assert response.status_code == 200

    result = response.json()

    assert "score" in result
    assert result["score"] in [0.0, 1.0]
    