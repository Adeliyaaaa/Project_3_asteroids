# Importer les bibliothèques
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go 
import streamlit as st
from streamlit_option_menu import option_menu
from datetime import datetime
from database import get_data

# Page configuration
st.set_page_config(layout="wide")

st.markdown(f"""
    <div style="background-color:rgba(5, 5, 8, 0.4); padding:5px; border-radius:8px; text-align:center;">
    <h2 style="font-size:45px; font-weight: bold;"> Découvrez les astéroïdes </h2>
    </div> """, unsafe_allow_html=True)

st.session_state["page"] = "Découvrez les astéroïdes"

# CSS styling
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

# Background image
page_bg_img2 = """
<style>
.stApp {
    background-image: url("https://wallpaperaccess.com/full/138014.jpg");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
}
</style>
"""
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

# Charger le dataframe
df = get_data("""
              SELECT 
                *
              FROM asteroids1 
              """)

# Vérifier si on est sur la bonne page (optionnel)
if "page" not in st.session_state:
    st.session_state["page"] = "Découvrez les astéroïdes"  

# Sidebar
if st.session_state["page"] == "Découvrez les astéroïdes":
    st.sidebar.title("Filtres")
    # Filtre date
    date = df['date_approche'].dt.date.unique()
    selected_date = st.sidebar.multiselect("Choisissez une date :", date)

# Filtrer le DataFrame en fonction des sélections  
filtered_df = df[df['date_approche'].dt.date.isin(selected_date)]

# Vérifier si le filtered_df est vide  
if filtered_df.empty:  
    filtered_df = df  # Afficher df si filtered_df est vide 

# Création de colonnes pour les KPIs
col_1, col_2, col_3, col_4, col_5 = st.columns(5)

# KPI 1 : Nombre d'astéroides
with col_1:
    # Compter le nombre d'astéroïdes  
    total_asteroides = filtered_df.shape[0]  
    # Afficher le résultat
    st.markdown(f"""
    <div style="background-color:#050508; padding:5px; border-radius:5px; border: 1px solid #DDE2E7; text-align: center; width: 230px; height: 150px; overflow: hidden; display: flex; justify-content: center; align-items: center;">
        <div>
            <h2 style="font-size:18px; color: #DDE2E7; margin: 0;"> Nombre d'astéroïdes </h2>
            <h1 style="font-size:20px; color: #EAE0D5; margin: 0;">{total_asteroides}</h1>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.write("")

# KPI 2 : Nombre de collisions surveillées 
with col_2:
    total_collisions_surveillees = filtered_df['sentry_surveillance_collisions'].sum()
    # Afficher le résultat
    st.markdown(f"""
    <div style="background-color:#050508; padding:5px; border-radius:5px; border: 1px solid #DDE2E7; text-align: center; width: 230px; height: 150px; overflow: hidden; display: flex; justify-content: center; align-items: center;">
        <div>
            <h2 style="font-size:18px; color: #DDE2E7; margin: 0;"> Nombre de surveillances collisions </h2>
            <h1 style="font-size:20px; color: #EAE0D5; margin: 0;">{total_collisions_surveillees}</h1>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.write("")

# KPI 3 : Diamètre min - max
with col_3:
    diametre_min = filtered_df['diametre_estime_min_m'].min()
    diametre_max = filtered_df['diametre_estime_max_m'].max()
    # Afficher le résultat
    st.markdown(f"""
    <div style="background-color:#050508; padding:5px; border-radius:5px; border: 1px solid #DDE2E7; text-align: center; width: 230px; height: 150px; overflow: hidden; display: flex; justify-content: center; align-items: center;">
        <div>
            <h2 style="font-size:18px; color: #DDE2E7; margin: 0;"> Diamètre estimé (m) </h2>
            <h1 style="font-size:20px; color: #EAE0D5; margin: 0;"> Min: {diametre_min:.2f}</h1>
            <h1 style="font-size:20px; color: #EAE0D5; margin: 0;"> Max: {diametre_max:.2f}</h1>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.write("")

# KPI 4 : Vitesse min - max
with col_4:
    vitesse_min = filtered_df['vitesse_relative_km_par_seconde'].min()
    vitesse_max = filtered_df['vitesse_relative_km_par_seconde'].max()
    # Afficher le résultat
    st.markdown(f"""
    <div style="background-color:#050508; padding:5px; border-radius:5px; border: 1px solid #DDE2E7; text-align: center; width: 230px; height: 150px; overflow: hidden; display: flex; justify-content: center; align-items: center;">
        <div>
            <h2 style="font-size:18px; color: #DDE2E7; margin: 0;"> Vitesse relative (km/s) </h2>
            <h1 style="font-size:20px; color: #EAE0D5; margin: 0;"> Min: {vitesse_min:.2f}</h1>
            <h1 style="font-size:20px; color: #EAE0D5; margin: 0;"> Max: {vitesse_max:.2f}</h1>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.write("")

# KPI 5: Distance moyenne par rapport à la terre
with col_5:
    distance_moyenne = filtered_df["distance_de_la_terre"].mean()
    distance_moyenne = distance_moyenne/1000000
    # Afficher le résultat
    st.markdown(f"""
    <div style="background-color:#050508; padding:5px; border-radius:5px; border: 1px solid #DDE2E7; text-align: center; width: 230px; height: 150px; overflow: hidden; display: flex; justify-content: center; align-items: center;">
        <div>
            <h2 style="font-size:18px; color: #DDE2E7; margin: 0;"> Distance moyenne<br>Terre-Astéroïdes (km) </h2>
            <h1 style="font-size:20px; color: #EAE0D5; margin: 0;">{distance_moyenne:.2f}M </h1>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.write("")

st.markdown("<br>", unsafe_allow_html=True)

# Graphiques
col1, col2, col3 = st.columns([0.42, 0.38, 0.2])

# Types d'astéroïdes
with col1:
    type_counts = filtered_df['type'].value_counts().reset_index()
    type_counts.columns = ['Type', 'Nombre']
    type_counts = type_counts.sort_values(by='Nombre', ascending=True)

    fig1 = px.bar(
        type_counts,
        x='Nombre',
        y='Type',
        title="Répartition des types d'astéroïdes",
        text='Nombre',
        orientation='h'
    )
    # Modifier les noms des labels pour inclure des sauts de ligne
    tick_labels = {
        'Inconnu': 'Inconnu',  
        'Type S (silicatés)': 'S (Silicaté)',   
        'Type C (carbonés)': 'C (Carboné)',   
        'Type M (métalliques)': 'M (Métallique)',   
        'Type L (entre S (silicatés) et C (carbonés))': 'L (entre S & C)',   
        'Type B (sous-type de C)': 'B (sous-type C)',   
        'Type D': 'D',   
        'Type Q (Olivine, Pyroxène, Métaux (fer-nickel), Silicates non altérés)': 'Q (Olivine,<br>Pyroxène, Métaux,<br>Silicaté non altéré)'  
    }

    # Afficher sur Streamlit
    fig1.update_layout(
        height=355,
        plot_bgcolor='#050508', 
        paper_bgcolor='#050508',
        title_x=0.15, 
        title_font=dict(size=18, color='#DDE2E7'),
        yaxis=dict(  
            tickmode='array',  
            tickfont=dict(size=11),
            tickvals=list(tick_labels.keys()),  
            ticktext=list(tick_labels.values())
        ),
        xaxis_type="log",  # Échelle logarithmique
        xaxis_title="Nombre d'astéroïdes",
        yaxis_title="Type d'astéroïde"
    )
    fig1.update_traces(textangle=360, textfont=dict(size=14), marker_color='#0077B6')
    st.plotly_chart(fig1, use_container_width=True)

# Astéroïdes au fil du temps
with col2:
    df['année'] = df['date_decouverte'].dt.year
    asteroides_par_an = df['année'].value_counts().reset_index()
    asteroides_par_an.columns = ['année', 'nombre_asteroides']
    asteroides_par_an = asteroides_par_an.sort_values(by='année')  
    
    fig2 = px.line(asteroides_par_an,   
              x='année',   
              y="nombre_asteroides",   
              title='Astéroïdes découverts au fil du temps',  
              labels={'nombre_asteroides': 'Nombre d\'astéroïdes', 'année': 'Année'},  
              markers=True)
    # Afficher sur Streamlit
    fig2.update_traces(line=dict(color='#0077B6', width=2))
    fig2.update_layout(
        height=355,
        plot_bgcolor="#050508", 
        paper_bgcolor="#050508",
        font_color="#DDE2E7",
        title_x=0.15,
        title_font=dict(size=18, color='#DDE2E7')
    )
    st.plotly_chart(fig2, use_container_width=True)

# KPI : Nombre moyen d'astéroïdes par jour, nombre d'impacts par an
with col3:
    
    # Nombre moyen d'astéroïdes par jour
    asteroides_par_jour = df.groupby(filtered_df['date_approche'].dt.date)['id'].count()
    moyenne_asteroides_par_jour = asteroides_par_jour.mean()
    # Afficher le résultat
    st.markdown(f"""
    <div style="background-color:#050508; padding:5px; border-radius:5px; border: 1px solid #DDE2E7; text-align: center; width: 235px; height: 165px; overflow: hidden; display: flex; justify-content: center; align-items: center;">
        <div>
            <h2 style="font-size:18px; color: #DDE2E7; margin: 0;"> Nombre moyen d'astéroïdes par jour </h2>
            <h1 style="font-size:20px; color: #EAE0D5; margin: 0;">{round(moyenne_asteroides_par_jour)}</h1>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.write("")

    # Nombre total d'impacts terrestres:
    impacts = filtered_df['nom'][filtered_df['lieu_impact'].notna()].nunique() 
    # Afficher le résultat
    st.markdown(f"""
    <div style="background-color:#050508; padding:5px; border-radius:5px; border: 1px solid #DDE2E7; text-align: center; width: 235px; height: 165px; overflow: hidden; display: flex; justify-content: center; align-items: center;">
        <div>
            <h2 style="font-size:18px; color: #DDE2E7; margin: 0;"> Nombre d'impacts terrestres </h2>
            <h1 style="font-size:20px; color: #EAE0D5; margin: 0;">{impacts}</h1>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.write("")

st.markdown("<br>", unsafe_allow_html=True)

col1, col2, col3 = st.columns([0.27, 0.48, 0.35])

# Astéroïdes potentiellement dangeureux vs non dangereux
with col1:
    total_asteroides = len(filtered_df)
    dangerous_asteroids = filtered_df[filtered_df['potentiellement_dangeureux'] == True].shape[0]
    data = pd.DataFrame({
    "Type d'astéroïde": ["Non dangereux", "Potentiellement dangereux"],
    "Nombre": [total_asteroides - dangerous_asteroids, dangerous_asteroids]
    })

    fig1 = px.pie(data,
                names="Type d'astéroïde", 
                values="Nombre", 
                title="Proportion des astéroïdes",
                color_discrete_sequence=["#0077B6", "#CAF0F8"],
                hole=0.4)

    # Afficher sur Streamlit
    fig1.update_layout(  
        height=380,
        plot_bgcolor='#050508', 
        paper_bgcolor='#050508',
        title_x=0.15, 
        title_font=dict(size=18, color='#DDE2E7'),  
        legend=dict(title='Type d\'astéroïde', font=dict(size=14), orientation="h") 
    )     
    
    st.plotly_chart(fig1, use_container_width=True) 

# Statistiques des astéroïdes par année
with col2:
    df_stats_ast = get_data("""
    SELECT   
      a.annee,  
      COALESCE(a.nombre_asteroides, 0) AS nombre_asteroides,  
      COALESCE(b.nombre_impacts, 0) AS nombre_impacts,  
      COALESCE(c.entrees_atmosphere, 0) AS entrees_atmosphere  
    FROM   
        (SELECT   
          EXTRACT(YEAR FROM date_approche) AS annee,  
          COUNT(id) AS nombre_asteroides  
        FROM   
          asteroids1  
        GROUP BY   
          annee) AS a  
    JOIN   
        (SELECT   
            EXTRACT(YEAR FROM date_approche) AS annee,  
            COUNT (DISTINCT nom) AS nombre_impacts  
        FROM   
            asteroids1  
        WHERE   
            lieu_impact IS NOT NULL  
        GROUP BY   
            annee) AS b ON a.annee = b.annee  
    JOIN   
        (SELECT   
            EXTRACT(YEAR FROM date_approche) AS annee,  
            COUNT(*) AS entrees_atmosphere  
        FROM   
            asteroids1  
        WHERE   
            date_entree_athmospherique IS NOT NULL  
        GROUP BY   
            annee) AS c ON a.annee = c.annee OR b.annee = c.annee  
    ORDER BY   
        annee;
    """)

    # Créer le graphique à barres superposées
    fig = go.Figure()  
 
    fig.add_trace(go.Bar(  
    x=df_stats_ast['annee'],  
    y=df_stats_ast['nombre_impacts'],  
    name='Impacts terrestres',  
    marker_color='#CAF0F8',
    text=df_stats_ast['nombre_impacts'],
    textposition='inside',
    textangle=360,
    textfont=dict(size=14)
    ))  

    fig.add_trace(go.Bar(  
    x=df_stats_ast['annee'],  
    y=df_stats_ast['entrees_atmosphere'],  
    name='Entrées dans l\'atmosphère',  
    marker_color='#0077B6',
    text=df_stats_ast['entrees_atmosphere'],  
    textposition='inside',
    textangle=360,
    textfont=dict(size=14)
    ))  
    # Afficher le graphique avec Streamlit  
    fig.update_layout(
    height=380,
    plot_bgcolor='#050508', 
    paper_bgcolor='#050508',  
    legend=dict(
        font=dict(size=14), 
        orientation="h",
        x=0.05,
        y=-0.3, 
    ),    
    title='Statistiques des astéroïdes par année',
    title_x=0.15,
    title_font=dict(size=18, color='#DDE2E7'),
    xaxis_title='Année',  
    yaxis_title='Nombre',  
    barmode='stack'
    ) 
    st.plotly_chart(fig, use_container_width=True)  

# Répartition des tailles d'astéroïdes
with col3:
    def classifie_taille(description):  
        description = description.lower()  
        if 'petite' in description or 'petit' in description or 'modeste' in description:  
            return 'Petite'  
        elif 'moyenne' in description:  
            return 'Moyenne'  
        elif 'grande' in description:  
            return 'Grande'  
        else:  
            return 'Inconnue'

    filtered_df['taille'] = filtered_df['description'].apply(classifie_taille)
    taille_counts = filtered_df['taille'].value_counts().reset_index()
    taille_counts.columns = ['taille', 'nombre']

    fig = px.bar(
        taille_counts,
        x='taille',
        y='nombre',
        title="Répartition des tailles d'astéroïdes",
        text='nombre'
    )
    # Afficher sur Streamlit
    fig.update_layout(
        height=370,
        plot_bgcolor='#050508', 
        paper_bgcolor='#050508',
        title_x=0.15, 
        title_font=dict(size=18, color='#DDE2E7'),
        yaxis_type="log",  # Échelle logarithmique
        yaxis_title="Nombre d'astéroïdes",
        xaxis_title="Taille"
    )
    fig.update_traces(textangle=360, textfont=dict(size=14), marker_color='#0077B6')
    st.plotly_chart(fig, use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)

col1, col2 = st.columns([0.38, 0.62])

# Information sur l'astéroïde sélectionné   
with col1:
    # Filtre astéroïde
    asteroide = df['nom'].unique()
    selected_asteroide = st.sidebar.selectbox("Choisissez un astéroïde :", asteroide)   
    filtered_df_ast = df[df['nom'] == selected_asteroide]

    # Afficher les informations pour chaque astéroïde sélectionné  
    if selected_asteroide and not filtered_df_ast.empty:  
        latest_asteroid = filtered_df_ast.sort_values(by='date_approche', ascending=False).iloc[0]

        st.markdown(f"""  
            <div style="background-color:#050508; padding:5px; border-radius:5px; border: 1px solid #DDE2E7; height: 480px; overflow: hidden; text-align:center;">   
                <h2 style="font-size:20px;"> {latest_asteroid['nom']} </h2>  
                <h1 style="font-size:15px; font-weight: normal;">{latest_asteroid['description']}</h1> 
                <h1 style="font-size:15px; font-weight: normal;">Potentiellement dangereux : {latest_asteroid['potentiellement_dangeureux']}</h1>
                <h1 style="font-size:16px; font-weight: normal;">Surveillance collision : {latest_asteroid['sentry_surveillance_collisions']}</h1>
                <h1 style="font-size:15px; font-weight: normal;"> Magnitude absolue: {latest_asteroid['magnitude_absolue']}</h1>  
                <h1 style="font-size:15px; font-weight: normal;"> Diamètre estimé: Min {round(latest_asteroid['diametre_estime_min_m'], 2)} (m), Max {round(latest_asteroid['diametre_estime_max_m'], 2)} (m)</h1>  
                <h1 style="font-size:15px; font-weight: normal;"> Vitesse relative en {latest_asteroid['date_approche'].year}: {round(latest_asteroid['vitesse_relative_km_par_seconde'], 2)} (km/s) </h1>  
                <h1 style="font-size:15px; font-weight: normal;"> Type: {latest_asteroid['type']}</h1>  
            </div> """, unsafe_allow_html=True)

with col2:
    # Filtre astéroïde   
    filtered_df_ast = df[df['nom'] == selected_asteroide]
    filtered_df_ast['date_approche'] = pd.to_datetime(filtered_df_ast['date_approche'])

    if selected_asteroide and not filtered_df_ast.empty:
        fig = px.line(filtered_df_ast, 
                  x='date_approche', 
                  y='vitesse_relative_km_par_seconde',
                  title=f"Dates quand l'astéroïde {latest_asteroid['nom']} passe près de la Terre et sa vitesse", 
                  labels={"date_approche": "Dates d'approche", "vitesse_relative_km_par_seconde":"Vitesse relative (km/s)"},
                  markers=True)
        
        fig.update_xaxes(tickformat="%Y-%m-%d", tickvals=filtered_df_ast['date_approche'], tickangle=-45)
        # Affichage du graphique dans Streamlit
        fig.update_traces(line=dict(color='#0077B6', width=2))
        fig.update_layout(
        height=480,
        plot_bgcolor="#050508", 
        paper_bgcolor="#050508",
        font_color="#DDE2E7", 
        title_x= 0.07,
        title_font=dict(size=18, color='#DDE2E7'))
        st.plotly_chart(fig, use_container_width=True)
    
    