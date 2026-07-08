---
title: Projet8 Mlops Api
emoji: 🚀
colorFrom: blue
colorTo: green
sdk: docker
app_port: 7860
pinned: false
---

# Projet 8 — API MLOps de scoring crédit

Ce projet met en production un modèle de scoring crédit via une API FastAPI conteneurisée avec Docker.  
L’API reçoit les informations d’un client, retourne un score de prédiction et enregistre les données de monitoring dans une base PostgreSQL.

## Fonctionnalités

- API FastAPI exposant un endpoint `/predict`
- Chargement du modèle au démarrage de l’application
- Prédiction d’un score de risque crédit
- Logging des prédictions en base PostgreSQL
- Monitoring :
  - score prédit
  - latence
  - utilisation mémoire
  - utilisation CPU
  - statut de la requête
  - erreurs éventuelles
- Analyse de performance dans un notebook
- Analyse du data drift
- Tests automatisés
- Déploiement Docker sur Hugging Face Spaces
- Pipeline CI/CD avec GitHub Actions

## Structure du projet

```text
app/
├── main.py              # API FastAPI
├── model_loader.py      # Chargement du modèle
├── schemas.py           # Schémas Pydantic
├── database.py          # Connexion à la base
├── models.py            # Modèle SQLAlchemy
├── features.py          # Liste des variables attendues

models/
└── model/               # Artefact MLflow du modèle

notebooks/
├── data_drift_analysis.ipynb
├── data_drift_evidently.ipynb
└── performance_analysis.ipynb

tests/
└── test_api.py

monitoring/
└── dashboard.py

Dockerfile
requirements.txt
generate_load.py
README.md


# Installation

Installer les dépendances :

```bash
pip install -r requirements.txt
```

---

## Lancement de l'API

Depuis la racine du projet :

```bash
uvicorn app.main:app --reload
```

L'API est disponible à l'adresse :

```
locale : http://127.0.0.1:8000
déployée : https://bhmo-projet8-mlops-api.hf.space
```

La documentation interactive est accessible via Swagger :

```
locale : http://127.0.0.1:8000/docs
déployée : https://bhmo-projet8-mlops-api.hf.space/docs
```

L'endpoint principal `/predict` reçoit les caractéristiques d'un client et retourne un score de prédiction.

---

## Base de données

Les données de monitoring sont enregistrées dans une base PostgreSQL hébergée sur **Neon**.

La connexion est réalisée via la variable d'environnement :

```text
DATABASE_URL
```

En l'absence de cette variable, une base SQLite (`test.db`) est utilisée pour les tests locaux.

---

## Monitoring

Chaque prédiction est enregistrée avec les informations suivantes :

- Horodatage
- Score prédit
- Variables d'entrée principales
- Latence (ms)
- Utilisation CPU
- Utilisation mémoire
- Statut de la requête
- Message d'erreur éventuel
- Features d'entrée

Les analyses sont réalisées dans le notebook :

```
notebooks/performance_analysis.ipynb
```

Les principaux indicateurs étudiés sont :

- distribution des scores prédits ;
- latence de l'API ;
- temps d'inférence ;
- consommation mémoire ;
- consommation CPU ;
- taux de succès des requêtes.

---

## Analyse des performances

Le profiling a été réalisé avec **cProfile** afin d'identifier les goulots d'étranglement.

Les résultats montrent que :

- le modèle LightGBM est rapide ;
- la préparation des données (création du DataFrame Pandas) représente la plus grande partie du temps d'exécution.

Une optimisation expérimentale basée sur **NumPy** a permis de réduire le temps moyen d'inférence d'environ **52 %**.

La version robuste de l'API a néanmoins été conservée afin de garantir la fiabilité du traitement des données d'entrée.

---

## Analyse du Data Drift

Deux notebooks permettent d'analyser la dérive des données :

```
notebooks/data_drift_analysis.ipynb

notebooks/data_drift_evidently.ipynb
```

Les distributions des données de production sont comparées aux données de référence afin de détecter d'éventuelles dérives.

---

## Tests

Les tests unitaires sont exécutés avec :

```bash
pytest
```

Ils sont également lancés automatiquement dans le pipeline CI/CD.

---

## Docker

Construire l'image :

```bash
docker build -t projet8-mlops-api .
```

Lancer le conteneur :

```bash
docker run -p 7860:7860 projet8-mlops-api
```

---

## Pipeline CI/CD

Le projet utilise **GitHub Actions** afin de :

- installer les dépendances ;
- exécuter les tests automatisés ;
- valider le code avant déploiement.

---

## Déploiement

API :

https://huggingface.co/spaces/BhmO/projet8-mlops-api

Dashboard :

https://huggingface.co/spaces/BhmO/projet8-mlops-dashboard

---

## Technologies utilisées

- Python
- FastAPI
- MLflow
- LightGBM
- Pandas
- NumPy
- SQLAlchemy
- PostgreSQL (Neon)
- Docker
- GitHub Actions
- Hugging Face Spaces
- Evidently
- Streamlit

---

## Auteur

Projet réalisé dans le cadre du parcours **Data Scientist / Machine Learning Engineer** – OpenClassrooms.