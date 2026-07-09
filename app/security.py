import os
from fastapi import Header, HTTPException
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")


def verify_api_key(x_api_key: str = Header(None)):
    if API_KEY is None:
        raise HTTPException(status_code=500, detail="Configuration API_KEY manquante")

    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Clé API invalide")

    return x_api_key