import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu

st.title("Découvrez les astéroïdes")
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

df = pd.read_parquet(".ignore\df_asteroides.parquet")
# Vérifier si on est sur la bonne page (optionnel)
if "page" not in st.session_state:
    st.session_state["page"] = "Planètes mineurs ou astéroïdes"  

if st.session_state["page"] == "Planètes mineurs ou astéroïdes":
    st.sidebar.title("Filtres :")
    date = df['date'].unique()
    selected_date = st.sidebar.selectbox("Choisissez une date :", date)

    asteroide = df['name'].unique()
    selected_asteroide = st.sidebar.selectbox("Choisissez un astéroïde :", asteroide)