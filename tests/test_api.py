from fastapi.testclient import TestClient
from app.main import app
import json 

client = TestClient(app)

# Vérification de l'API : API démarre et retourne un message de bienvenue, route / existe
def test_home():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "message": "API de scoring opérationnelle"
    }


# Vérification de l'endpoint de prédiction : endpoint /predict fonctionne, modèle bien chargé, réponse contient un score     
def test_predict_empty_features():

    response = client.post(
        "/predict",
        json={"features": {}}
    )

    assert response.status_code == 200

    result = response.json()

    assert "score" in result

# Vérification de l'endpoint de prédiction avec un échantillon réel : endpoint /predict fonctionne, modèle bien chargé, réponse contient un score
def test_predict_real_sample():

    with open("data/sample_request.json", encoding="utf-8") as file:
        payload = json.load(file)

    response = client.post("/predict", json=payload)

    assert response.status_code == 200

    result = response.json()

    assert "score" in result
    assert result["score"] in [0.0, 1.0]



# Vérification d'entrée invalide : endpoint /predict retourne une erreur 422 pour des données invalides
def test_predict_invalid_input():

    response = client.post(
        "/predict",
        json={"features": "bonjour"}
    )

    assert response.status_code == 422


# Vérification d'entrée partielle : endpoint /predict fonctionne, modèle bien chargé, réponse contient un score même si certaines colonnes sont manquantes
def test_predict_partial_features():

    response = client.post(
        "/predict",
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