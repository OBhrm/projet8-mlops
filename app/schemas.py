#Schémas d'entrée de l'API

from pydantic import BaseModel


class PredictionInput(BaseModel):
    features: dict