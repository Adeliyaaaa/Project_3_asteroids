import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu


st.title("Entrée atmosphérique et impacts terrestres")
# l'image de fond de la 1ère page:
page_bg_img1 = """
<style>
.stApp {
    background-image: url("https://www.rmg.co.uk/sites/default/files/styles/full_width_2600/public/Asteroids_passing_Earth.jpg?itok=xrDzSKSD");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
}
</style>
"""
# Appliquer le CSS avec st.markdown
st.markdown(page_bg_img1, unsafe_allow_html=True)

page_style1 = """
    <style>
    .custom-text {
        color: white;
        font-size: 20px;
        text-align: center;
    }
    </style>
"""
st.markdown(page_style1, unsafe_allow_html=True)

# Rajouter des filtres sur cette page : 
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