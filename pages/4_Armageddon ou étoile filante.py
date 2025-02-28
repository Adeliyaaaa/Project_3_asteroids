import pandas as pd
import streamlit as st
import psycopg2
from streamlit_option_menu import option_menu
from database import get_data
import datetime
from datetime import date
import plotly_express as px
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit.components.v1 as components

import numpy as np
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import NearestNeighbors
from datetime import date
from datetime import datetime
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder, MultiLabelBinarizer
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.utils.validation import check_array
import re

st.markdown(f"""
    <div style="background-color:rgba(5, 5, 8, 0.4); padding:5px; border-radius:8px; text-align:center;">
    <h2 style="font-size:45px; font-weight: bold;"> Quel astéroïde pourrait frapper la Terre prochainement ? </h2>
    </div> """, unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

st.session_state["page"] = "Armageddon ou étoile filante"

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
        .custom-text {
        color: white;
        font-size: 15px;
        text-align: center;
        }

    </style>
    """,
    unsafe_allow_html=True
    )

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

df_sans_impact = get_data("""
                        with cte_latest AS(
                            select
                                nom,
                                id,
                                MAX(date_approche) as derniere_date_approche
                            from asteroids1
                            group by nom, id 
                        )
                        select 
                            a.nom AS nom_astéroïde, 
                            a.description, 
                            a.magnitude_absolue,
                            a.diametre_estime_min_m, 
                            a.diametre_estime_max_m,
                            a.potentiellement_dangeureux,
                            a.sentry_surveillance_collisions,
                            a.vitesse_relative_km_par_seconde, 
                            a.vitesse_relative_km_par_heure,
                            a.distance_de_la_terre,
                            a.type
                        from asteroids1 a 
                        join cte_latest l on l.id = a.id AND a.date_approche = l.derniere_date_approche
                        where lieu_impact is null;
                        """)

df_sans_impact['potentiellement_dangeureux'] = df_sans_impact['potentiellement_dangeureux'].factorize()[0] #false = 0, True = 1
df_sans_impact['sentry_surveillance_collisions'] = df_sans_impact['sentry_surveillance_collisions'].factorize()[0]

df_impact = get_data("""
                        with cte_latest AS(
                            select
                                nom,
                                id,
                                MAX(date_approche) as derniere_date_approche
                            from asteroids1
                            group by nom, id 
                        )
                        select 
                            a.nom AS nom_astéroïde,
                            a.description,
                            a.magnitude_absolue,
                            a.diametre_estime_min_m, 
                            a.diametre_estime_max_m,
                            a.potentiellement_dangeureux,
                            a.sentry_surveillance_collisions,
                            a.vitesse_relative_km_par_seconde, 
                            a.vitesse_relative_km_par_heure,
                            a.distance_de_la_terre,
                            a.type,
                            TO_CHAR(a.date_entree_athmospherique, 'DD-MM-YYYY') as date_entree_athmospherique,
                            a.lieu_impact,
                            a.latitude,
                            a.longitude
                        from asteroids1 a 
                        join cte_latest l on l.id = a.id AND a.date_approche = l.derniere_date_approche
                        where lieu_impact notnull 
                        ORDER BY nom_astéroïde;
                        """)

df_date_approche = get_data("""
                        select 
                            nom,
                            TO_CHAR(date_approche, 'YYYY-MM-DD') AS date_approche,
                            vitesse_relative_km_par_seconde
                        from asteroids1 a 
                        where lieu_impact isnull;
                        """)

# les colonnes utilisées pour le ML :
numeric_cols = ['magnitude_absolue', 'diametre_estime_min_m', 'diametre_estime_max_m', 'potentiellement_dangeureux', 
                'sentry_surveillance_collisions', 'vitesse_relative_km_par_seconde', 'vitesse_relative_km_par_heure', 'distance_de_la_terre']
categorical_cols = ['type']

numeric_transformer = Pipeline(steps=[
    ('scaler', StandardScaler())
])

categorical_transformer = Pipeline(steps=[
    ('onehot', OneHotEncoder(handle_unknown='ignore'))
])

# On combine tout dans un ColumnTransformer
preprocessor = ColumnTransformer(
    transformers=[
        ('num', numeric_transformer, numeric_cols),
        ('cat', categorical_transformer, categorical_cols),
    ]
)

pipeline = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('knn', NearestNeighbors(metric="manhattan", n_neighbors=1))
])

pipeline.fit(df_sans_impact)

def similar_asteroids(
        nom,
        pipeline: Pipeline = pipeline,
        ) -> pd.DataFrame:

    asteroid_info = df_impact[df_impact['nom_astéroïde'] == nom]
    asteroid_info_scaled = pipeline.named_steps['preprocessor'].transform(asteroid_info)
    distances, indices = pipeline.named_steps['knn'].kneighbors(asteroid_info_scaled)
    
    df_similar_asteroids = df_sans_impact.iloc[indices[0]].copy()

    # Description de l'Astéroïde avec_impact
    col1, col2 = st.columns(2)
    with col1: 
        st.markdown(f"""
            <br>
            <h1 style="font-size:25px; text-align:center; color: #DDE2E7"> Astéroïde ayant déjà heurté la Terre </h1></div> """, unsafe_allow_html=True)
        st.markdown(f"""
        <div style="background-color:#050508; padding:5px; border-radius:5px; border: 1px solid #050508; text-align:center; height:250px">
            <h2 style="font-size:25px;"> {asteroid_info.iloc[0]['nom_astéroïde']} </h2>
            <h1 style="font-size:17px; font-weight: normal;"> est entré dans l'atmosphère terrestre le {asteroid_info.iloc[0]['date_entree_athmospherique']}</h1>
            <h1 style="font-size:17px; font-weight: normal;">Lieu d'impact : {asteroid_info.iloc[0]['lieu_impact']}</h1>
            <h1 style="font-size:17px; font-weight: normal;">{asteroid_info.iloc[0]['description']}</h1>
            </div> """, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

    # Description de l'Astéroïde similaire : 
    with col2: 
        df_similar_asteroids = df_similar_asteroids.reset_index()
        st.markdown(f"""
                <br>
                <h1 style="font-size:25px; text-align:center; color: #DDE2E7"> Astéroïde similaire au {asteroid_info.iloc[0]['nom_astéroïde']} </h1></div> """, unsafe_allow_html=True)
        st.markdown(f"""
        <div style="background-color:#050508; padding:5px; border-radius:5px; border: 1px solid #050508; text-align:center; height:250px">
            <h2 style="font-size:25px;"> {df_similar_asteroids.loc[0, 'nom_astéroïde']} </h2>
            <h1 style="font-size:17px; font-weight: normal;">{df_similar_asteroids.loc[0, 'description']}</h1>
            <br><br><br>
            </div> """, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
    

    col1, col2 = st.columns(2)
    # DataFrame de l'Astéroïde avec_impact
    with col1: 
        df_asteroid_impact = pd.DataFrame(asteroid_info.iloc[0]).T
        df_asteroid_impact.rename(columns={'magnitude_absolue': 'Magnitude absolue', 'diametre_estime_min_m' : 'Diamètre estimé min, m', 'diametre_estime_max_m' : "Diamètre estimé max, m", 
        'potentiellement_dangeureux' : "Potentiellement dangeureux ", 'sentry_surveillance_collisions' : "Surveillance collisions",
        'vitesse_relative_km_par_seconde': "Vitesse relative km/s", 'vitesse_relative_km_par_heure' : "Vitesse relative km/h", 
        'distance_de_la_terre' : "Distance de la terre, km", 'type' : "Type"}, inplace=True)
        df_asteroid_impact = df_asteroid_impact.T.reset_index()
        firstcol = df_asteroid_impact.columns[0]
        secondcol = df_asteroid_impact.columns[1]
        df_asteroid_impact = df_asteroid_impact.rename(columns={firstcol : 'Caractéristiques', secondcol : 'Données'})
        df_asteroid_impact = df_asteroid_impact.iloc[2 : 11]
        styled_df_asteroid_impact = df_asteroid_impact.style.set_properties(**{'background-color': '#050508', 'color': '#DDE2E7'})
        st.dataframe(styled_df_asteroid_impact, hide_index=True, use_container_width=True)
    # DataFrame de l'Astéroïde similaire : 
    with col2:
        df_similar_asteroids.rename(columns={'magnitude_absolue': 'Magnitude absolue', 'diametre_estime_min_m' : 'Diamètre estimé min, m', 'diametre_estime_max_m' : "Diamètre estimé max, m", 
        'potentiellement_dangeureux' : "Potentiellement dangeureux ", 'sentry_surveillance_collisions' : "Surveillance collisions",
        'vitesse_relative_km_par_seconde': "Vitesse relative km/s", 'vitesse_relative_km_par_heure' : "Vitesse relative km/h", 
        'distance_de_la_terre' : "Distance de la terre, km", 'type' : "Type"}, inplace=True)
        df_asteroid_sans_impact = df_similar_asteroids.T.reset_index().rename(columns={'index' : 'Caractéristiques', 0 : 'Données'})
        df_asteroid_sans_impact = df_asteroid_sans_impact.iloc[3 : ]
        df_asteroid_sans_impact = df_asteroid_sans_impact.replace({1 : True, 0: False})
        styled_df_similar_asteroids = df_asteroid_sans_impact.style.set_properties(**{'background-color': '#050508', 'color': '#DDE2E7'})
        st.dataframe(styled_df_similar_asteroids,  hide_index=True, use_container_width=True)

    # Graphique Px : 
    df_filtered = df_date_approche[df_date_approche['nom'] == df_similar_asteroids.loc[0, 'nom_astéroïde']]
    df_filtered['date_approche'] = pd.to_datetime(df_filtered['date_approche'])

    fig = px.line(df_filtered, 
                    x='date_approche', 
                    y='vitesse_relative_km_par_seconde', 
                    title=f"Dates lorsque l'astéroïde {df_similar_asteroids.loc[0, 'nom_astéroïde']} passe près de la Terre ainsi que sa vitesse relative", 
                    labels={"date_approche": "Dates d'approche", "vitesse_relative_km_par_seconde":"Vitesse relative km/s"},
                    markers=True)
    # Option 2 : Afficher toutes les dates disponibles
    fig.update_xaxes(tickformat="%Y-%m-%d", tickvals=df_filtered['date_approche'], tickangle=-45)
    fig.update_traces(line=dict(color='#0077B6', width=2))
    # Affichage du graphique dans Streamlit
    fig.update_layout(
    plot_bgcolor="#050508", 
    paper_bgcolor="#050508",
    font_color="#DDE2E7",  # Texte 
    title_x= 0.25)
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("<br><br>", unsafe_allow_html=True)

# Filtres de la page : 
if "page" not in st.session_state:
    st.session_state["page"] = "Armageddon ou étoile filante"  

if st.session_state["page"] == "Armageddon ou étoile filante":
    st.sidebar.title("Filtre :")
    # Filtre sélectionne astéroïde : 
    asteroide = df_impact['nom_astéroïde'].unique()

    selection_asteroide = st.sidebar.selectbox("Choisissez un astéroïde :", asteroide)
    st.sidebar.markdown("<br><br><br><br><br><br><br>", unsafe_allow_html=True)

    similar_asteroids(selection_asteroide)


    button_css = """
        <style>
        .stButton > button {
            background-color: #050508;
            color: DDE2E7 !important;
            border: 1px solid #DDE2E7;
            border-radius: 15px;
            center: left;
            font-size: 22px;
            font-weight: bold; /* Ajoute la police en gras */
            padding: 10px 20px;
            height:10px;
            width: 240px;
            transition: background-color 0.3s ease;
        }
        .stButton > button:hover {
            background-color: #13151D;
            border: 3px solid #DDE2E7;
            font-size: 24px;
            color: DDE2E7 !important;
        }
        .stButton > button:active {
        background-color: #807E75; /* Couleur lorsque le bouton est cliqué */
        border: 5px solid #DDE2E7 !important;
        font-size: 26px !important;
        }
        </style>
    """

    # Injecter le CSS dans l'application
    st.markdown(button_css, unsafe_allow_html=True)
    
    st.sidebar.markdown(
    "<h3 style='text-align: center;'>L'astéroïde 2024 YR4 :</h3>",
    unsafe_allow_html=True)

    if st.sidebar.button('(2024 YR4)'): 
        df_yr4 = get_data("""
                select 
                    nom, 
                    magnitude_absolue, 
                    diametre_estime_min_m , 
                    diametre_estime_max_m , 
                    potentiellement_dangeureux, 
                    sentry_surveillance_collisions,
                    to_char(date_approche, 'YYYY-MM-DD') as date_approche,
                    to_char(date_approche, 'DD-MM-YYYY') as date_approche_format_fr, 
                    vitesse_relative_km_par_seconde, 
                    vitesse_relative_km_par_heure,
                    distance_de_la_terre, 
                    description,
                    type,
                    to_char(date_decouverte, 'DD-MM-YYYY') as date_decouverte
                from asteroids1 a 
                where nom = '(2024 YR4)'
                order by date_approche DESC;
                """)
        st.markdown(f"""
        <div style="background-color:rgba(5, 5, 8, 0.8); padding:5px; text-align:center;">
        <h2 style='custom-text'>2024 YR4 </h2>""", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1 : 
            st.markdown(f"""
                    <div style="background-color:rgba(5, 5, 8, 0.8); padding:5px; text-align:center;">
                    <br><br>
                    <p class='custom-text'>YR4, récemment découvert par les astronomes, a désormais 3,1 % de chances de frapper la Terre en 2032, 
                        le niveau le plus élevé jamais enregistré depuis le début de la surveillance, 
                        selon les calculs mardi de la Nasa.<br> </p>""", unsafe_allow_html=True)
            st.markdown(f"""
                    <div style="background-color:rgba(5, 5, 8, 0.8); padding:5px; text-align:center;">
                    <p class='custom-text'>Estimé entre 40 et 90 mètres de large, 
                        cet astéroïde pourrait percuter la Terre le 22 décembre 2032, selon les estimations d’agences spatiales 
                        internationales et potentiellement causer des dommages considérables, comme détruire une ville. 
                        Une prévision à prendre toutefois avec des pincettes car elle est fondée sur des données préliminaires 
                        et est amenée à évoluer dans les semaines et mois qui viennent, insistent des experts interrogés par l’AFP. 
                        <br> </p>""", unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
        
        with col2: 
            st.image("https://www.cite-espace.com/assets/uploads/asteroid-artist-s-impression.jpg")

        col1, col2= st.columns(2)
        with col1: 
            st.markdown(f"""
            <div style="background-color:#050508; padding:5px; border-radius:5px; border: 1px solid #DDE2E7; text-align:center; height:330px">
            <br>
            <h2 style="font-size:25px;"> (2024 YR4)</h2>
            <h1 style="font-size:17px; font-weight: normal;">{df_yr4.loc[0, 'description']}</h1>
            <h1 style="font-size:17px; font-weight: normal;">Il a été découvert le {df_yr4.loc[0, 'date_decouverte']}</h1>        
            </div> """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
            <div style="background-color:#050508; padding:5px; border-radius:5px; border: 1px solid #DDE2E7; text-align:center; height:330px">
            <h1 style="font-size:17px; font-weight: normal;"> Magnitude absolue : {df_yr4.loc[0, 'magnitude_absolue']}</h1>
            <h1 class="reduce-space" style="font-size:17px; font-weight: normal;"> Diamètre estimé : 
            Min {round(df_yr4.loc[0, 'diametre_estime_min_m'],2)} m, Max {round(df_yr4.loc[0, 'diametre_estime_max_m'],2)} m </h1>
            <h1 style="font-size:17px; font-weight: normal;"> Vitesse relative le {df_yr4.loc[0, 'date_approche_format_fr']}: {round(df_yr4.loc[0, 'vitesse_relative_km_par_seconde'],2)} km/s </h1>
            <h1 style="font-size:17px; font-weight: normal;"> Type : {df_yr4.loc[0, 'type']}</h1>
            <h1 style="font-size:15px; font-weight: normal;">Potentiellement dangereux : {df_yr4.loc[0, 'potentiellement_dangeureux']}</h1>
            <h1 style="font-size:15px; font-weight: normal;">Surveillance collision : {df_yr4.loc[0, 'sentry_surveillance_collisions']}</h1>
            </div> """, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        fig = px.line(df_yr4, 
                                x='date_approche', 
                                y='vitesse_relative_km_par_seconde', 
                                title=f"Dates lorsque l'astéroïde (2024 YR4) passe près de la Terre ainsi que sa vitesse relative", 
                                labels={"date_approche": "Dates d'approche", "vitesse_relative_km_par_seconde":"Vitesse relative km/s"},
                                markers=True)
                # Option 2 : Afficher toutes les dates disponibles
        fig.update_xaxes(tickformat="%Y-%m-%d", tickvals=df_yr4['date_approche'], tickangle=-45)
        # Affichage du graphique dans Streamlit
        fig.update_traces(line=dict(color='#0077B6', width=2))
        fig.update_layout(
        plot_bgcolor="#050508", 
        paper_bgcolor="#050508",
        font_color="#DDE2E7",  # Texte 
        title_x= 0.15)
        st.plotly_chart(fig, use_container_width=True)