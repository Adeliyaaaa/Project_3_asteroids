import psycopg2
import pandas as pd
import streamlit as st

# Fonction pour initialiser la connexion à PostgreSQL
@st.cache_resource
def init_connection():
    return psycopg2.connect(**st.secrets["postgres"])

# Fonction pour exécuter une requête et récupérer les données
def get_data(query):
    conn = init_connection()
    return pd.read_sql(query, conn)