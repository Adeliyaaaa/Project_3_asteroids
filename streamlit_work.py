import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu


# Sélection entre accueil et photos
with st.sidebar:
    st.write("Bienvenue !")

    selection = option_menu(menu_title=None, 
                    options= ["Planètes mineures ou astéroïdes", "Découvrez les astéroïdes"])
    
    # if selection == "Planètes mineures ou astéroïdes":
    #     st.write("Bienvenue sur la page d'accueil !")
    # elif selection == "Découvrez les astéroïdes":
    #     st.write("Bienvenue ")

# le contenu de la page accueil et de la page photo   
if selection == "Planètes mineures ou astéroïdes":
# Les titres de la page
    st.markdown("<h1 style='text-align: center; color: black;'> Astéroïdes géocroiseurs</h1>", unsafe_allow_html=True)
    
    st.write("""La notion de planète mineure est la notion générique pour parler des planètes naines, astéroïdes, centaures, objets transneptuniens, objets du nuage d'Oort, etc. 
             Elle entretient également des liens étroits avec celles de petit corps, de planétoïde ou encore de météoroïde. """)
    st.write("""En astronomie, les astéroïdes géocroiseurs sont des astéroïdes évoluant à proximité de la Terre.
             Pour les nommer on utilise souvent l'abréviation ECA (de l'anglais Earth-Crossing Asteroids, astéroïdes croisant l'orbite de la Terre), astéroïdes dont l'orbite autour du Soleil croise celle de la Terre, ayant une distance aphélique inférieure à celle de Mars, soit 1,381 UA (valeur d'1,300 UA fixée par les spécialistes américains). 
             Les NEA (Near-Earth Asteroids, astéroïdes proches de la Terre) sont aussi souvent, par abus et à tort, appelés en français géocroiseurs même si certains ne croisent pas l'orbite de la Terre""")

elif selection == "Découvrez les astéroïdes":
# le titre de la page
    st.markdown("<h1 style='text-align: center; color: black;'> Les données sur les astéroïdes </h1>", unsafe_allow_html=True)

    st.write("Les programmes d'observation détectent chaque année plus de 2 000 nouveaux objets géocroiseurs")
    st.write("On appelle « astéroïdes potentiellement dangereux » (APD ; potentially hazardous asteroids, PHA, en anglais) les astéroïdes de magnitude absolue H < 22 (mesurant donc typiquement plus de 140 mètres de diamètre moyen) et qui peuvent passer à moins de 0,05 unité astronomique de la Terre.")
