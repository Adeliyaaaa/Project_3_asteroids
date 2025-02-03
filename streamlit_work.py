import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu


# Sélection entre accueil et photos
with st.sidebar:
    st.write("Bienvenue !")
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
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown("""
        <style>
            /* Modifier la couleur de l'élément sélectionné */
            [data-testid="stSidebarNav"] a {
                color: white; /* Couleur du texte des liens */
            }

            [data-testid="stSidebarNav"] a:hover {
                color: #FFD700; /* Couleur du texte au survol */
            }

            [data-testid="stSidebarNav"] a[aria-current="page"] {
                background-color: #FF4B4B !important; /* Rouge */
                color: white !important; /* Texte en blanc */
                border-radius: 10px; /* Arrondir les bords */
                padding: 5px 10px; /* Ajoute un peu d'espace */
            }
        </style>
    """, unsafe_allow_html=True)

    st.sidebar.title("Navigation")
    # st.sidebar.page_link("Page 1", label="🌍 Planètes mineures ou astéroïdes")
    # st.sidebar.page_link("Page 2", label="🔭 Découvrez les astéroïdes")

    selection = option_menu(menu_title=None, 
                    options= ["Planètes mineures ou astéroïdes", "Découvrez les astéroïdes"])

    

# le contenu de la page accueil et de la page photo   
if selection == "Planètes mineures ou astéroïdes":
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
            font-weight: bold;
            text-align: center;
        }
        </style>
    """
    st.markdown(page_style1, unsafe_allow_html=True)

    # Les titres de la 1ère page
    st.markdown("<h1 style='text-align: center; color: #DDE2E7;'> Astéroïdes géocroiseurs</h1>", unsafe_allow_html=True)
    st.markdown("<p class='custom-text'>La notion de planète mineure est la notion générique pour parler des planètes naines, astéroïdes, centaures, objets transneptuniens, objets du nuage d'Oort, etc. Elle entretient également des liens étroits avec celles de petit corps, de planétoïde ou encore de météoroïde.</p>", unsafe_allow_html=True)
    st.markdown("<p class='custom-text'>En astronomie, les astéroïdes géocroiseurs sont des astéroïdes évoluant à proximité de la Terre. Pour les nommer on utilise souvent l'abréviation ECA (de l'anglais Earth-Crossing Asteroids, astéroïdes croisant l'orbite de la Terre), astéroïdes dont l'orbite autour du Soleil croise celle de la Terre, ayant une distance aphélique inférieure à celle de Mars, soit 1,381 UA (valeur d'1,300 UA fixée par les spécialistes américains). Les NEA (Near-Earth Asteroids, astéroïdes proches de la Terre) sont aussi souvent, par abus et à tort, appelés en français géocroiseurs même si certains ne croisent pas l'orbite de la Terre</p>", unsafe_allow_html=True)

elif selection == "Découvrez les astéroïdes":
    #Couleur de fond : 
    page_bg_img2 = """
    <style>
    .stApp {
        background-color: #050508; /* Black */
    }
    </style>
    """
    # Appliquer le CSS avec st.markdown
    st.markdown(page_bg_img2, unsafe_allow_html=True)

    page_style2 = """
        <style>
        .custom-text {
            color: white;
            font-size: 20px;
        }
        </style>
    """
    st.markdown(page_style2, unsafe_allow_html=True)

# le titre de la page
    st.markdown("<h1 style='text-align: center; color: white;'> Les données sur les astéroïdes </h1>", unsafe_allow_html=True)
    st.markdown("<p class='custom-text'>Les programmes d'observation détectent chaque année plus de 2 000 nouveaux objets géocroiseurs.</p>", unsafe_allow_html=True)


    # avec l'affichage d'un graphique
    #st.markdown("<p class='custom-text'>On appelle « astéroïdes potentiellement dangereux » (APD ; potentially hazardous asteroids, PHA, en anglais) les astéroïdes de magnitude absolue H < 22 (mesurant donc typiquement plus de 140 mètres de diamètre moyen) et qui peuvent passer à moins de 0,05 unité astronomique de la Terre.</p>", unsafe_allow_html=True)
    