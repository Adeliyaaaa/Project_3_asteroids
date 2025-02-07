import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu
from datetime import datetime
from database import get_data

st.title("Découvrez les astéroïdes")
st.session_state["page"] = "Découvrez les astéroïdes"

#Couleur de fond : 
page_bg_img2 = """
<style>
.stApp {
    background-color: #050508; /* Black */
}
</style>
"""
# Appliquer le CSS avec st.markdown
st.markdown(page_bg_img2, unsafe_allow_html=True)

page_style2 = """
    <style>
    .custom-text {
        color: white;
        font-size: 10px;
    }
    </style>
"""
st.markdown(page_style2, unsafe_allow_html=True)

# # le titre de la page
#     st.markdown("<h1 style='text-align: center; color: white;'> Les données sur les astéroïdes </h1>", unsafe_allow_html=True)
#     st.markdown("<p class='custom-text'>Les programmes d'observation détectent chaque année plus de 2 000 nouveaux objets géocroiseurs.</p>", unsafe_allow_html=True)


#     # avec l'affichage d'un graphique
#     #st.markdown("<p class='custom-text'>On appelle « astéroïdes potentiellement dangereux » (APD ; potentially hazardous asteroids, PHA, en anglais) les astéroïdes de magnitude absolue H < 22 (mesurant donc typiquement plus de 140 mètres de diamètre moyen) et qui peuvent passer à moins de 0,05 unité astronomique de la Terre.</p>", unsafe_allow_html=True)

df = get_data("""
              SELECT 
                nom, 
                description, 
                TO_CHAR(date_approche, 'YYYY') AS date_approche,
                TO_CHAR(date_entree_athmospherique, 'YYYY-MM-DD') as date_entree_athmospherique, 
                lieu_impact 
              FROM asteroids1 
              WHERE lieu_impact is NOT NULL""")
st.dataframe(df)


# Vérifier si on est sur la bonne page (optionnel)
if "page" not in st.session_state:
    st.session_state["page"] = "Découvrez les astéroïdes"  

if st.session_state["page"] == "Découvrez les astéroïdes":
    st.sidebar.title("Filtres :")
    date = df['date_approche'].unique()
    selected_date = st.sidebar.selectbox("Choisissez une date :", date)

    asteroide = df['nom'].unique()
    selected_asteroide = st.sidebar.selectbox("Choisissez un astéroïde :", asteroide)
