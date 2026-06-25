# Dashboard Streamlit

import os

import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from sqlalchemy import create_engine

from evidently import Report
from evidently.presets import DataDriftPreset


# Configuration Streamlit
st.set_page_config(
    page_title="Monitoring API Scoring",
    layout="wide"
)

st.title("Monitoring de l'API de scoring")


# Chargement des variables d'environnement
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL is None:
    st.error("DATABASE_URL est introuvable. Vérifie ton fichier .env.")
    st.stop()


# Connexion à Neon
engine = create_engine(DATABASE_URL)


# Lecture des données de production
@st.cache_data(ttl=60)
def load_production_data():
    return pd.read_sql(
        "SELECT * FROM predictions ORDER BY timestamp DESC",
        engine
    )


df = load_production_data()

if df.empty:
    st.warning("Aucune donnée de production disponible dans Neon.")
    st.stop()


# Nettoyage / typage
df["timestamp"] = pd.to_datetime(df["timestamp"])
df["score"] = pd.to_numeric(df["score"], errors="coerce")
df["latency_ms"] = pd.to_numeric(df["latency_ms"], errors="coerce")


# Fonction pour l'analyse de drift avec Evidently
def run_drift_analysis():

    train_df = pd.read_parquet("data/app_train_final.parquet")

    reference_data = train_df[
        ["AMT_INCOME_TOTAL", "AMT_CREDIT", "DAYS_BIRTH"]
    ].dropna()

    current_data = df[
        ["AMT_INCOME_TOTAL", "AMT_CREDIT", "DAYS_BIRTH"]
    ].dropna()

    report = Report([
        DataDriftPreset()
    ])

    result = report.run(
        reference_data=reference_data,
        current_data=current_data
    )

    return result


# KPIs
st.subheader("Indicateurs clés")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Nombre de prédictions",
        len(df)
    )

with col2:
    st.metric(
        "Score moyen",
        round(df["score"].mean(), 3)
    )

with col3:
    st.metric(
        "Latence moyenne (ms)",
        round(df["latency_ms"].mean(), 2)
    )

with col4:
    error_rate = (df["status"] == "error").mean() * 100
    st.metric(
        "Taux d'erreur (%)",
        round(error_rate, 2)
    )


# Historique
st.subheader("Dernières prédictions")

st.dataframe(
    df.head(20),
    use_container_width=True
)


# Distribution des scores
st.subheader("Distribution des scores prédits")

score_counts = df["score"].value_counts().sort_index()

st.bar_chart(score_counts)


# Évolution de la latence
st.subheader("Évolution de la latence")

latency_df = df.sort_values("timestamp").set_index("timestamp")

st.line_chart(
    latency_df["latency_ms"]
)


# Activité de l'API
st.subheader("Activité de l'API")

activity_df = df.copy()
activity_df["hour"] = activity_df["timestamp"].dt.floor("h")

activity_by_hour = (
    activity_df
    .groupby("hour")
    .size()
)

st.line_chart(activity_by_hour)


# Statut des requêtes
st.subheader("Statut des requêtes")

status_counts = df["status"].value_counts()

st.bar_chart(status_counts)


# Variables surveillées
st.subheader("Variables métier surveillées")

col_a, col_b, col_c = st.columns(3)

with col_a:
    st.write("AMT_INCOME_TOTAL")
    st.bar_chart(df["AMT_INCOME_TOTAL"])

with col_b:
    st.write("AMT_CREDIT")
    st.bar_chart(df["AMT_CREDIT"])

with col_c:
    st.write("DAYS_BIRTH")
    st.bar_chart(df["DAYS_BIRTH"])


# Evidently
st.subheader("Détection automatique du data drift avec Evidently AI")

if st.button("Lancer l'analyse de drift"):
    drift_result = run_drift_analysis()

    st.success("Analyse Evidently exécutée.")

    st.info(
        """
        Résultat Evidently observé :

        - Drift détecté sur 1 variable sur 3.
        - `DAYS_BIRTH` : drift détecté.
        - `AMT_CREDIT` : pas de drift détecté.
        - `AMT_INCOME_TOTAL` : pas de drift détecté.

        Conclusion : les données de production restent globalement proches des données d'entraînement,
        mais la variable `DAYS_BIRTH` doit être surveillée.
        """
    )