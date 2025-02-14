import pandas as pd
import streamlit as st
import folium
import leafmap.foliumap as leafmap
from streamlit_folium import folium_static, st_folium
from database import get_data

# Configuration de la page Streamlit
st.set_page_config(layout="wide")

# Charger les données depuis la base de données
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

# Créer un DataFrame final_df avec 10 astéroïdes ayant des lieux d'impact différents
final_df = df.drop_duplicates(subset="lieu_impact").head(10)  # Sélectionner 10 lieux d'impact uniques

# --- Titre de la page et de la carte ---
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

    # Ajouter des marqueurs classiques pour chaque lieu d'impact dans final_df
    for _, row in final_df.iterrows():
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
        
        # Appliquer une tolérance pour éviter les petites variations dans les coordonnées
        tolerance = 0.0001  # Ajustez la tolérance selon vos besoins
        selected_row = final_df[
            (final_df["latitude"].between(lat - tolerance, lat + tolerance)) &
            (final_df["longitude"].between(lon - tolerance, lon + tolerance))
        ]
        
        if not selected_row.empty:
            st.session_state["selection"] = selected_row.iloc[0]["nom"]  # Mise à jour du nom sélectionné

# --- Affichage des détails si un astéroïde est sélectionné ---
with col2:
    if "selection" in st.session_state and st.session_state["selection"]:
        # Filtrer le DataFrame final_df selon le nom sélectionné
        selected_asteroid = final_df[final_df["nom"] == st.session_state["selection"]]
        
        # Vérification si l'astéroïde sélectionné n'est pas vide
        if not selected_asteroid.empty:
            asteroid_info = selected_asteroid.iloc[0]
            st.markdown(f"""
            <div style="background-color:#1e1e1e; padding:40px; border-radius:15px; border: 3px solid #333333; text-align:center; color:white; font-size:22px;">
                <h2 style="font-size:30px; font-weight:bold; color:white; text-decoration: underline;">{asteroid_info['nom']}</h2>
                <p><b style="font-size:26px;">Lieu :</b> {asteroid_info['lieu_impact']}</p>
                <p><b style="font-size:26px;">Date :</b> {asteroid_info['date_entree_athmospherique']}</p>
                <p><b style="font-size:26px;">Vitesse :</b> {asteroid_info['vitesse_relative_km_par_seconde']} km/s</p>
                <p><b style="font-size:26px;">Type :</b> {asteroid_info['type'] if pd.notna(asteroid_info['type']) else "Non disponible"}</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.write("Aucune donnée trouvée pour cet astéroïde.")


