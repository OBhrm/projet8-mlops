
# Crée le chargeur du modèle  : pour ne le charger qu'une seule fois au démarrage de l'API
import mlflow.pyfunc

MODEL_PATH = "models/model"

model = mlflow.pyfunc.load_model(MODEL_PATH)

