import pandas as pd
import streamlit as st
import folium
import leafmap.foliumap as leafmap
from streamlit_folium import st_folium
from folium.plugins import MarkerCluster
from database import get_data

# Configuration de la page Streamlit
st.set_page_config(layout="wide")

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
    a.date_entree_athmospherique,
    a.lieu_impact, 
    a.latitude, 
    a.longitude
FROM asteroids1 a 
JOIN cte_latest l ON l.id = a.id AND a.date_approche = l.derniere_date_approche
WHERE lieu_impact NOTNULL AND latitude NOTNULL;
""")

# Afficher les premières lignes pour vérification
st.write(df)
# Compter le nombre d'astéroïdes par lieu
asteroids_count = df.groupby(['latitude', 'longitude']).size().reset_index(name='count')

# Créer un dictionnaire où chaque clé est un lieu d'impact et la valeur est une liste d'astéroïdes
impact_dict = {}
for idx, row in df.dropna(subset=['lieu_impact']).iterrows():
    impact = row['lieu_impact']
    name = row['nom']
    
    if impact in impact_dict:
        impact_dict[impact].append(name)
    else:
        impact_dict[impact] = [name]

# Créer un DataFrame avec comme colonnes les lieux d'impact et comme valeurs les noms des astéroïdes
df_n = pd.DataFrame(dict([(key, pd.Series(value)) for key, value in impact_dict.items()]))

# Afficher le DataFrame résultant
st.write(df_n)

# Choisir le fond de carte
options = list(leafmap.basemaps.keys())
index = options.index("SATELLITE")
with st.sidebar:
    basemap = st.selectbox("Sélectionnez un fond de carte :", options, index, key="selectbox_basemap")
# Créer la carte avec le fond choisi
# Créer la carte avec le fond choisi
# Créer la carte avec le fond choisi
df = df.merge(asteroids_count[['latitude', 'longitude', 'count']], on=['latitude', 'longitude'], how='left')
col1, col2 = st.columns([4, 1])
with col1:
    # Créer la carte avec le fond choisi
    m = leafmap.Map(locate_control=True, latlon_control=True, draw_export=True, minimap_control=True)
    m.add_basemap(basemap)

    # Ajouter les marqueurs pour chaque astéroïde dans le DataFrame df
for idx, row in df.iterrows():
    if pd.notnull(row['latitude']) and pd.notnull(row['longitude']):
        # Récupérer le lieu d'impact à partir du DataFrame df
        lieu_impact = row['lieu_impact']
        
        # Créer un tooltip avec le nom du lieu d'impact
        tooltip_text = lieu_impact

        # Calculer un rayon proportionnel au nombre d'astéroïdes
        radius = row['count'] * 2  # Le rayon augmente avec le nombre d'astéroïdes
        radius = max(radius, 10)  # Définir un rayon minimum pour les petits nombres (ici 10)

        # Ajouter un cercle avec un popup et un tooltip
        folium.CircleMarker(
            location=[row['latitude'], row['longitude']],
            radius=radius,  # Rayon proportionnel
            color='orange',
            fill=True,
            fill_color='orange',
            fill_opacity=0.7,  # Opacité uniforme pour le cercle
            tooltip=tooltip_text  # Afficher le nom du lieu d'impact au survol
        ).add_to(m)

        # Ajouter le nombre d'astéroïdes à l'intérieur du cercle avec une opacité ajustée
        folium.Marker(
            location=[row['latitude'], row['longitude']],
            icon=folium.DivIcon(
                html=f'<div style="font-size: 10pt; color: rgba(255, 255, 255, 0.7); text-align: center; font-weight: bold; width: {radius * 2}px; height: {radius * 2}px; position: absolute; left: -{radius -5}px; top: -{radius -35}px; opacity: 0.7;">{int(row["count"])}</div>'
            )
        ).add_to(m)

# Affichage de la carte dans Streamlit
map_data = st_folium(m, width=1100, height=530)
