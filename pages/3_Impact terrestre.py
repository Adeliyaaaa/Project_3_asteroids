import pandas as pd
import streamlit as st
import folium
import leafmap.foliumap as leafmap
from streamlit_folium import st_folium
from folium.plugins import MarkerCluster
from database import get_data
from streamlit_folium import folium_static

# Configuration de la page Streamlit
st.set_page_config(layout="wide")

st.markdown(f"""
    <div style="background-color:rgba(5, 5, 8, 0.4); padding:5px; border-radius:8px; text-align:center;">
    <h2 style="font-size:45px; font-weight: bold;"> Les impacteurs </h2>
    </div> """, unsafe_allow_html=True)

st.session_state["page"] = "Impact terrestre"

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
    background-image: url("https://images.unsplash.com/photo-1544656376-ffe19d4b7353?q=80&w=2076&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
}
</style>
"""
# Appliquer le CSS avec st.markdown
st.markdown(page_bg_img1, unsafe_allow_html=True)


# Charger les données depuis la base de données
df = get_data("""
            WITH cte_latest AS (
                SELECT
                    nom,
                    id,
                    MAX(date_approche) AS derniere_date_approche
                FROM asteroids1
                GROUP BY nom, id
            )
            SELECT 
                a.nom,
                a.description, 
                TO_CHAR(a.date_entree_athmospherique, 'DD-MM-YYYY') as date_entree_athmospherique, 
                a.lieu_impact,
                a.magnitude_absolue, 
                a.diametre_estime_min_m,
                a.diametre_estime_max_m,
                a.potentiellement_dangeureux,
                a.sentry_surveillance_collisions,
                a.vitesse_relative_km_par_seconde,
                a.vitesse_relative_km_par_heure,
                a."type",
                a.latitude, 
                a.longitude
            FROM asteroids1 a 
            JOIN cte_latest l ON l.id = a.id AND a.date_approche = l.derniere_date_approche
            WHERE lieu_impact NOTNULL AND latitude NOTNULL;
""")

df_nb_asteroids = get_data("""
                        select 
                            DISTINCT(lieu_impact),
                            COUNT(distinct nom) as nb_asteroids, 
                            latitude, 
                            longitude 
                        from asteroids1 a 
                        where lieu_impact notnull and longitude NOTNULL
                        group by 
                            lieu_impact, 
                            latitude, 
                            longitude ;
                           """)

# Filtres de la page : 
if "page" not in st.session_state:
    st.session_state["page"] = "Impact terrestre"  

if st.session_state["page"] == "Impact terrestre":

    st.sidebar.markdown(f"""<p style="font-size:25px; font-weight: 550; color: #DDE2E7">Filtre :</p> 
                        </div> """, unsafe_allow_html=True)
    # lieu = df["lieu_impact"].unique()
    # lieu_with_blank = ["Choisissez un lieu :"] + list(lieu)
    # selection = st.sidebar.selectbox(" ", lieu_with_blank, key='selectbox_key')
    # if selection != "Choisissez un lieu :" :
    #     indexes = df[df["lieu_impact"] == selection].index
    #     for index in indexes: 
    #         asteroid = df.loc[index, 'nom']

    # Choisir le fond de carte
    options = list(leafmap.basemaps.keys())
    index = options.index("HYBRID")
    with st.sidebar:
        basemap = st.selectbox("Fonds de carte :", options, index, key="selectbox_basemap")

# Créer la carte avec le fond choisi
m = leafmap.Map(locate_control=True, latlon_control=True, draw_export=True, minimap_control=True)
m.add_basemap(basemap)

# Fonction pour ajuster la taille en fonction du nombre d'astéroïdes
def get_marker_size(nb_asteroids, min_size=45, max_size=100, scale_factor=4):
    return min(max_size, max(min_size, nb_asteroids * scale_factor))

for index, row in df_nb_asteroids.iterrows():
    nb_asteroids = df_nb_asteroids.loc[index, 'nb_asteroids']
    size = get_marker_size(nb_asteroids)  # Calcul dynamique de la taille

    
    folium.Marker(
        location=row[['latitude', 'longitude']],
        popup= (f"""
            <div style="font-size:14px; color: #050508; text-align: center;">
                <strong>{row['lieu_impact']}</strong><br>
            """),       
        icon=folium.DivIcon(
        html=f"""<div style="font-size:15px; color: #DDE2E7; 
                background: radial-gradient(rgba(19, 21, 29, 0.9) 30%, rgba(19, 21, 29, 0.5) 60%, rgba(19, 21, 29, 0) 100%);
                border-radius: 50%;  
                width: {size}px; height:{size}px; text-align: center; 
                line-height: {size}px; font-weight: bold;">{nb_asteroids}</div>"""
                )
            ).add_to(m)
# Affichage de la carte dans Streamlit
map_data = st_folium(m, width=1250, height=400)

if map_data and "last_object_clicked" in map_data and map_data["last_object_clicked"]:
    lat, lon = map_data["last_object_clicked"]["lat"], map_data["last_object_clicked"]["lng"]

    # Appliquer une tolérance pour éviter les petites variations dans les coordonnées
    tolerance = 0.0001  # Ajustez la tolérance selon vos besoins
    selected_row = df[
        (df["latitude"].between(lat - tolerance, lat + tolerance)) &
        (df["longitude"].between(lon - tolerance, lon + tolerance))
    ]
    

    if not selected_row.empty:
        selected_row_indexes = selected_row.index # Indexes des astéroïdes sélectionnés

        for index in selected_row_indexes: 
            nom = selected_row.loc[index, "nom"]  # nom sélectionné
            dict = selected_row.to_dict('index')
        
            col1, col2, col3 = st.columns([0.2, 0.4, 0.4])

            button_css = """
                <style>
                .stButton > button {
                    background-color: #050508;
                    color: DDE2E7 !important;
                    border: 1px solid #DDE2E7;
                    border-radius: 15px;
                    font-size: 22px;
                    font-weight: bold; /* Ajoute la police en gras */
                    padding: 10px 20px;
                    height:100px;
                    width: 200px;
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

            with col1: 
                if st.button(nom) : 
                    with col2: 
                        st.markdown(f"""
                    <div style="background-color:#050508; padding:5px; border-radius:5px; border: 1px solid #DDE2E7; text-align:center; height:250px">
                        <h2 style="font-size:25px;"> {selected_row.loc[index, 'nom']} </h2>
                        <h1 style="font-size:17px; font-weight: normal;"> est entré dans l'atmosphère terrestre le {selected_row.loc[index, 'date_entree_athmospherique']}. </h1>
                        <h1 style="font-size:16px; font-weight: normal;">Potentiellement dangereux : {selected_row.loc[index, 'potentiellement_dangeureux']}</h1>
                        <h1 style="font-size:16px; font-weight: normal;">Surveillance collision : {selected_row.loc[index, 'sentry_surveillance_collisions']}</h1>
                        </div> """, unsafe_allow_html=True)
                    with col3:
                        st.markdown(f"""
                    <div style="background-color:#050508; padding:5px; border-radius:5px; border: 1px solid #DDE2E7; text-align:center; height:250px">
                        <h1 style="font-size:16px; font-weight: normal;"> Magnitude absolue : {selected_row.loc[index, 'magnitude_absolue']}</h1>
                        <h1 class="reduce-space" style="font-size:16px; font-weight: normal;"> Diamètre estimé : 
                            Min {round(selected_row.loc[index, 'diametre_estime_min_m'],2)} m, Max {round(selected_row.loc[index, 'diametre_estime_max_m'],2)} m </h1>
                        <h1 style="font-size:16px; font-weight: normal;"> Vitesse relative : {round(selected_row.loc[index, 'vitesse_relative_km_par_seconde'],2)} km/s </h1>
                        <h1 style="font-size:16px; font-weight: normal;"> Type : {selected_row.loc[index, 'type']}</h1>
                        </div> """, unsafe_allow_html=True)


