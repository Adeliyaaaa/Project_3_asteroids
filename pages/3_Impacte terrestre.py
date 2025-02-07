import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu
from database import get_data


st.title("Entrée atmosphérique et impacts terrestres")
st.session_state["page"] = "Impact terrestre"

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


# Rajouter des filtres sur cette page : 

# Vérifier si on est sur la bonne page (optionnel)
if "page" not in st.session_state:
    st.session_state["page"] = "Impact terrestre" 

if st.session_state["page"] == "Impact terrestre":
    st.sidebar.title("Filtres :")
    date = df['date_approche'].unique()
    selected_date = st.sidebar.selectbox("Choisissez une date :", date)

    asteroide = df['nom'].unique()
    selected_asteroide = st.sidebar.selectbox("Choisissez un astéroïde :", asteroide)

