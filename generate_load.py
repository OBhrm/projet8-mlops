import requests
import random
import time

URL = "http://127.0.0.1:8000/predict"

for i in range(200):

    payload = {
        "features": {
            "AMT_INCOME_TOTAL": random.randint(50000, 500000),
            "AMT_CREDIT": random.randint(50000, 1000000),
            "DAYS_BIRTH": -random.randint(7000, 25000)
        }
    }

    response = requests.post(URL, json=payload)

    if response.status_code != 200:
        print(i, response.status_code, response.text)

    time.sleep(0.02)

print("Terminé")