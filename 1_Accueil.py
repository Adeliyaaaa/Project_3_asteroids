import pandas as pd
import streamlit as st
import psycopg2
from streamlit_option_menu import option_menu
from database import get_data

# Sélection entre accueil et photos
st.set_page_config(page_title="Main page")
st.title("Astéroïdes géocroiseurs")
st.session_state["page"] = "Accueil"


st.markdown(
    """
    <style>
        [data-testid="stSidebar"] {
            background-color: #050508; /* Black */
            color: white;
            padding: 20px;
            border-right: 2px solid #13151D; /* Bordure Rich black*/
            box-shadow: 5px 5px 15px rgba(0,0,0,0.3);
        }
        
        /* Modifier la couleur du texte dans la sidebar */
        [data-testid="stSidebar"] * {
            color: #DDE2E7; /* Platinum */
        }

        [data-testid="stSidebarNav"] a[aria-current="page"] {
            background-color: #050508; /* Black */
            border-radius: 10px; /* Arrondir les bords */
            padding: 5px 10px; /* Ajoute un peu d'espace */
        }
    </style>
    """,
    unsafe_allow_html=True
    )

page_bg_img1 = """
<style>
.stApp {
    background-image: url("https://cdn.sci.news/images/enlarge3/image_4498e-2016-WF9.jpg");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
}
</style>
"""
# Appliquer le CSS avec st.markdown
st.markdown(page_bg_img1, unsafe_allow_html=True)

# Les titres de la 1ère page
st.markdown("<p class='custom-text'>La notion de planète mineure est la notion générique pour parler des planètes naines, astéroïdes, centaures, objets transneptuniens, objets du nuage d'Oort, etc. Elle entretient également des liens étroits avec celles de petit corps, de planétoïde ou encore de météoroïde.</p>", unsafe_allow_html=True)
st.markdown("<p class='custom-text'>En astronomie, les astéroïdes géocroiseurs sont des astéroïdes évoluant à proximité de la Terre. Pour les nommer on utilise souvent l'abréviation ECA (de l'anglais Earth-Crossing Asteroids, astéroïdes croisant l'orbite de la Terre), astéroïdes dont l'orbite autour du Soleil croise celle de la Terre, ayant une distance aphélique inférieure à celle de Mars, soit 1,381 UA (valeur d'1,300 UA fixée par les spécialistes américains). Les NEA (Near-Earth Asteroids, astéroïdes proches de la Terre) sont aussi souvent, par abus et à tort, appelés en français géocroiseurs même si certains ne croisent pas l'orbite de la Terre</p>", unsafe_allow_html=True)


df = get_data("""
              SELECT 
                nom, 
                description, 
                TO_CHAR(date_approche, 'YYYY') AS date_approche,
                date_entree_athmospherique, 
                lieu_impact 
              FROM asteroids1 
              WHERE lieu_impact is NOT NULL""")
st.dataframe(df)


if "page" not in st.session_state:
    st.session_state["page"] = "Accueil"  

if st.session_state["page"] == "Accueil":
    st.sidebar.title("Filtres :")
    date = df['date_approche'].unique()
    selected_date = st.sidebar.selectbox("Choisissez une date :", date)

    asteroide = df['nom'].unique()
    selected_asteroide = st.sidebar.selectbox("Choisissez un astéroïde :", asteroide)