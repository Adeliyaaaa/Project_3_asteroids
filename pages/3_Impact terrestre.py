import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu
from database import get_data
import folium
import leafmap.foliumap as leafmap
from streamlit_folium import folium_static
import psycopg2
from streamlit_folium import folium_static, st_folium

st.set_page_config(layout="wide")

#st.title("Entrée atmosphérique et impacts terrestres")
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

# l'image de fond de la 1ère page:
page_bg_img1 = """
<style>
.stApp {
    background-color: #050508;
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
}
</style>
"""
# Appliquer le CSS avec st.markdown
st.markdown(page_bg_img1, unsafe_allow_html=True)

df = get_data("""
SELECT 
    nom, 
    lieu_impact,
    latitude,  
    longitude, 
    description,
    type,
    TO_CHAR(date_entree_athmospherique, 'DD-MM-YYYY') AS date_entree_athmospherique,
    masse_estimee_kg,
    vitesse_relative_km_par_seconde 
FROM asteroids1
WHERE lieu_impact IS NOT NULL AND latitude IS NOT NULL AND longitude IS NOT NULL
GROUP BY lieu_impact, latitude, longitude, nom, description, type, date_entree_athmospherique, masse_estimee_kg, vitesse_relative_km_par_seconde;
""")


# --- titre de la carte ---
st.title("Carte des impacts terrestres des astéroïdes")

# --- Interface pour choisir le fond de carte ---
col1, col2 = st.columns([4, 1])
options = list(leafmap.basemaps.keys())
index = options.index("SATELLITE")
with st.sidebar:
    basemap = st.selectbox("Sélectionnez un fond de carte :", options, index, key="selectbox_basemap")

with col1:
    m = leafmap.Map(
        locate_control=True, latlon_control=True, draw_export=True, minimap_control=True
    )
    m.add_basemap(basemap)

    # Ajouter des marqueurs classiques pour chaque lieu d'impact
    for _, row in df.iterrows():
        popup_content = f"""
        <div style="text-align: center;">
            <h4 style="color: darkred;">🌠 {row["nom"]}</h4>
            <b>Lieu :</b> {row["lieu_impact"]}<br>
        </div>
        """

        folium.Marker(
            location=[row["latitude"], row["longitude"]],
            popup=folium.Popup(popup_content, max_width=300),
            icon=folium.Icon()  # Utilise l'icône par défaut de Folium
        ).add_to(m)


    # Afficher la carte interactive dans Streamlit
    map_data = st_folium(m, width=1100, height=530)

    # Vérifier si un marqueur a été cliqué
    if map_data and "last_object_clicked" in map_data and map_data["last_object_clicked"]:
        lat, lon = map_data["last_object_clicked"]["lat"], map_data["last_object_clicked"]["lng"]
        selected_row = df[(df["latitude"] == lat) & (df["longitude"] == lon)]

        if not selected_row.empty:
            st.session_state["selection"] = selected_row.iloc[0]["nom"]  # Mise à jour du nom sélectionné

# --- Affichage des détails si un astéroïde est sélectionné --- 
with col2:
    if "selection" in st.session_state and st.session_state["selection"]:
        df = df[df["nom"] == st.session_state["selection"]]
        index = df.index[-1]

        st.markdown(f"""
        <div style="background-color:#1e1e1e; padding:40px; border-radius:15px; border: 3px solid #333333; text-align:center; color:white; font-size:22px;">
            <h2 style="font-size:30px; font-weight:bold; color:white; text-decoration: underline;">{df.loc[index, 'nom']}</h2>
            <p><b style="font-size:26px;">Lieu :</b> {df.loc[index, 'lieu_impact']}</p>
            <p><b style="font-size:26px;">Date :</b> {df.loc[index, 'date_entree_athmospherique']}</p>
            <p><b style="font-size:26px;">Masse estimée :</b> {df.loc[index, 'masse_estimee_kg'] if pd.notna(df.loc[index, 'masse_estimee_kg']) else "Non disponible"}</p>
            <p><b style="font-size:26px;">Vitesse :</b> {df.loc[index, 'vitesse_relative_km_par_seconde']} km/s</p>
            <p><b style="font-size:26px;">Type :</b> {df.loc[index, 'type'] if pd.notna(df.loc[index, 'type']) else "Non disponible"}</p>
        </div>
        """, unsafe_allow_html=True)
