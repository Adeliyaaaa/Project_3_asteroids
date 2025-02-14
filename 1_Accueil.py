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

# Sélection entre accueil et photos
st.set_page_config(page_title="Main page", layout="wide")
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
    background-image: url("https://cdn.sci.news/images/enlarge3/image_4498e-2016-WF9.jpg");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
}
</style>
"""
# Appliquer le CSS avec st.markdown
st.markdown(page_bg_img1, unsafe_allow_html=True)

col1, col2= st.columns(2)
with col1:
    st.title("Astéroïdes géocroiseurs")
    st.markdown(f"""
                <div style="background-color:rgba(5, 5, 8, 0.8); padding:5px; text-align:center;">
                <p class='custom-text'>La notion de planète mineure est la notion générique pour 
                parler des planètes naines, astéroïdes, centaures, objets transneptuniens, objets du nuage d'Oort, etc. 
                Elle entretient également des liens étroits avec celles de petit corps, de planétoïde ou encore de météoroïde.</p>""", unsafe_allow_html=True)

with col2: 
    st.markdown(f"""
                <div style="background-color:rgba(5, 5, 8, 0.8); padding:5px; text-align:center;">
                <p class='custom-text'>En astronomie, les astéroïdes géocroiseurs sont des astéroïdes évoluant à proximité 
                de la Terre. Pour les nommer on utilise souvent l'abréviation ECA (Earth-Crossing Asteroids, 
                astéroïdes croisant l'orbite de la Terre), astéroïdes dont l'orbite autour du Soleil croise celle de la Terre, 
                ayant une distance aphélique inférieure à celle de Mars, soit 1,381 UA (valeur d'1,300 UA fixée par les spécialistes 
                américains). Les NEA (Near-Earth Asteroids, astéroïdes proches de la Terre) sont aussi souvent, par abus et à tort, 
                appelés en français géocroiseurs même si certains ne croisent pas l'orbite de la Terre </p>""", unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)

current_date = date.today()
current_time = pd.Timestamp.now(tz='Europe/Paris').strftime('%H:%M')
current_year = current_date.year


df1 = get_data("""
            WITH cte_selection AS(
                SELECT 
                    DISTINCT(nom) AS nom_astéroïde, 
                    date_approche_complete,
                    (date_approche_complete AT TIME ZONE 'UTC') AT TIME ZONE 'Europe/Paris' AS heure_locale,
                    potentiellement_dangeureux,
                    sentry_surveillance_collisions AS surveillance_collisions
                    FROM asteroids1
                    where date_approche = CURRENT_DATE
                    )
                SELECT 
                    nom_astéroïde, 
                    TO_CHAR(date_approche_complete, 'YYYY-MM-DD   HH24 : MI : SS') AS date_utc,
                    TO_CHAR(heure_locale, 'HH24 : MI') AS heure_locale,
                    potentiellement_dangeureux,
                    surveillance_collisions
                FROM cte_selection
               ORDER BY heure_locale;
              """)

df1.rename(columns={'nom_astéroïde': "Nom de l'astéroïde", 'date_utc' : 'Date approche (UTC)', 'heure_locale' : 'Heure locale', 
                    'potentiellement_dangeureux' : 'Potentiellement dangereux', 'surveillance_collisions' : 'Surveillance collisions'}, inplace=True)

if not df1.empty:
    st.title("Dans le ciel d'aujourd'hui :")

    df2 = get_data("""
                with cte_nb_asteroids AS(
                    SELECT 
                        id,
                        COUNT(distinct nom) as nb_asteroids
                        FROM asteroids1
                        WHERE date_approche = CURRENT_DATE
                        group by id
                ),
                cte_nb_surveillance AS(
                    SELECT 
                        id,
                        COUNT(sentry_surveillance_collisions) as nb_surveillance
                        FROM asteroids1
                        WHERE sentry_surveillance_collisions = true and date_approche = CURRENT_DATE
                        group by id
                ),
                cte_nb_dangerous AS(
                    SELECT 
                        id,
                        COUNT(potentiellement_dangeureux) as nb_dangerous
                        FROM asteroids1
                        WHERE potentiellement_dangeureux = true and date_approche = CURRENT_DATE
                        group by id
                )
                SELECT 
                    SUM(nb_asteroids) as nb_asteroids, 
                    SUM(nb_surveillance) as nb_surveillance, 
                    SUM(nb_dangerous) as nb_dangerous
                FROM cte_nb_asteroids a 
                left join cte_nb_surveillance s on s.id = a.id 
                left join cte_nb_dangerous d on d.id = a.id;
                            """)
    # Informations Nombre d'astéroïdes Dans le ciel d'aujourd'hui : 

    col1, col2 = st.columns([0.65, 0.35])
    with col1: 
        styled_df = df1.style.set_properties(**{'background-color': '#050508', 'color': '#DDE2E7'})
        st.dataframe(styled_df, hide_index=True, use_container_width=True)

    with col2: 
        st.markdown(f"""
        <div style="background-color:#13151D; padding:5px; border-radius:5px; border: 1px solid #DDE2E7; text-align:center;">
            <h2 style="font-size:16px;"> Nombre d'astéroïdes </h2>
            <h1 style="font-size:16px;">{df2['nb_asteroids'].astype(int).sum()}</h1>
            </div> """, unsafe_allow_html=True)
        st.write("")
        st.markdown(f"""
            <div style="background-color:#13151D; padding:5px; border-radius:5px; border: 1px solid #DDE2E7; text-align:center;">
            <h2 style="font-size:16px;"> Potentiellement dangeureux : </h2>
            <h1 style="font-size:16px;">{int(df2['nb_dangerous'].sum())}</h1>
            </div> """, unsafe_allow_html=True)
        st.write("")
        st.markdown(f"""
            <div style="background-color:#13151D; padding:5px; border-radius:5px; border: 1px solid #DDE2E7; text-align:center;">
            <h2 style="font-size:16px;"> Astéroïdes surveillés: </h2>
            <h1 style="font-size:16px;">{int(df2['nb_surveillance'].sum())}</h1>
            </div> """, unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)
else : 
    st.title("Aujourd'hui il n'y a aucun astéroïde ...")


# Filtres de la page : 
if "page" not in st.session_state:
    st.session_state["page"] = "Accueil"  

if st.session_state["page"] == "Accueil":
    st.sidebar.write("Date : ")
    st.sidebar.markdown(f"""<p style="font-size:25px; color: #DDE2E7">{current_date} </p> 
                        </div> """, unsafe_allow_html=True)
    st.sidebar.write("Heure : ")
    st.sidebar.markdown(f"""<p style="font-size:25px; color: #DDE2E7">{current_time} </p> 
                        </div> """, unsafe_allow_html=True)
    
    st.sidebar.divider()  # Ajoute une séparation visuelle

    if not df1.empty:
        # Filtre sélectionne astéroïde : 
        st.sidebar.markdown(f"""<p style="font-size:25px; font-weight: 550; color: #DDE2E7">Filtre :</p> 
                            </div> """, unsafe_allow_html=True)
        asteroide = df1["Nom de l'astéroïde"].unique()
        asteroide_with_blank = ["Choisissez un astéroïde :"] + list(asteroide)
        selection = st.sidebar.selectbox(" ", asteroide_with_blank, key='selectbox_key')
        if selection != "Choisissez un astéroïde :" :

            df_ast = get_data("""
                            with cte_current_day as(
                                select
                                    distinct id,
                                    nom 
                                from asteroids1 a 
                                where date_approche = CURRENT_DATE
                            )
                            select 
                                d.nom,
                                TO_CHAR(a.date_approche, 'YYYY-MM-DD') as date_approche,
                                a.description,
                                a.magnitude_absolue, 
                                a.diametre_estime_min_m, 
                                a.diametre_estime_max_m, 
                                a.vitesse_relative_km_par_seconde,
                                a."type" 
                            from cte_current_day d
                            join asteroids1 a ON d.id = a.id
                            order by d.nom, a.date_approche
                            ;
                        """)
    # Information sur l'astéroïde sélectionné : 
            df_filtered = df_ast[df_ast['nom'] == selection]
            index = df_filtered[df_filtered['nom'] == selection].index[-1] # Prendre les données de l'année en cours
            
            col1, col2 = st.columns([0.26, 0.74])
            with col1: 
                st.markdown(
                    """
                    <style>
                        .reduce-space {
                            margin-bottom: 0px;
                            padding-bottom: 0px;
                            line-height: 1;
                        }
                    </style>
                    """,
                    unsafe_allow_html=True
                )
                st.markdown(f"""
                <div style="background-color:#050508; padding:5px; border-radius:5px; border: 1px solid #050508; text-align:center;">
                    <br>
                    <h2 style="font-size:25px;"> {selection} </h2>
                    <h1 style="font-size:17px; font-weight: normal;">{df_filtered.loc[index, 'description']}</h1>
                    <h1 style="font-size:15px; font-weight: normal;"> Magnitude absolue : {df_filtered.loc[index, 'magnitude_absolue']}</h1>
                    <h1 class="reduce-space" style="font-size:15px; font-weight: normal;"> Diamètre estimé : </h1>
                    <p class="reduce-space" style="font-size:15px; font-weight: normal;"> Min {round(df_filtered.loc[index, 'diametre_estime_min_m'],2)} m, Max {round(df_filtered.loc[index, 'diametre_estime_max_m'],2)} m </p>
                    <h1 style="font-size:15px; font-weight: normal;"> Vitesse relative en {current_year} : {round(df_filtered.loc[index, 'vitesse_relative_km_par_seconde'],2)} km/s </h1>
                    <h1 style="font-size:15px; font-weight: normal;"> Type : {df_filtered.loc[index, 'type']}</h1>
                    </div> """, unsafe_allow_html=True)
            with col2:
                df_filtered['date_approche'] = pd.to_datetime(df_filtered['date_approche'])

                fig = px.line(df_filtered, 
                                x='date_approche', 
                                y='vitesse_relative_km_par_seconde', 
                                title=f"Dates lorsque l'astéroïde {selection} passe près de la Terre ainsi que sa vitesse relative", labels={"date_approche": "Dates d'approche", "vitesse_relative_km_par_seconde":"Vitesse relative km/s"})
                # Option 2 : Afficher toutes les dates disponibles
                fig.update_xaxes(tickformat="%Y-%m-%d", tickvals=df_filtered['date_approche'], tickangle=-45)
                # Affichage du graphique dans Streamlit
                fig.update_layout(
                plot_bgcolor="#050508", 
                paper_bgcolor="#050508",
                font_color="#DDE2E7",  # Texte 
                title_x= 0.15)
                st.plotly_chart(fig, use_container_width=True)

