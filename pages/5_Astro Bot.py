import pandas as pd
import streamlit as st
import os
from dotenv import load_dotenv
load_dotenv()

import google.generativeai as genai
GOOGLE_API_KEY=os.getenv('google_api_key3')
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

st.session_state["page"] = "Astro Bot"

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

#Couleur de fond : 
page_bg_img2 = """
<style>
.stApp {
    background-image: url("https://cdn.sci.news/images/enlarge3/image_4498e-2016-WF9.jpg");
}
</style>
"""

# Appliquer le CSS avec st.markdown
st.markdown(page_bg_img2, unsafe_allow_html=True)

page_style2 = """
    <style>
    .custom-text {
        color: white;
        background_color : #13151D; /* Rich black */
        font-size: 10px;
    }
    </style>
"""
st.markdown(page_style2, unsafe_allow_html=True)

#st.sidebar.image('https://cdn.freebiesupply.com/logos/thumbs/1x/nvidia-logo.png', width=200)

#Chatbot
st.markdown(f"""
<div style="background-color:rgba(5, 5, 8, 0.8); padding:5px; text-align:center;">
    <h2 style="font-size:45px; font-weight: bold;"> Bonjour !</h2>
    <h2 style="font-size:30px; font-weight: bold;"> Je m'appelle Astro Bot et je suis passionné par les astéroïdes. </h2>
    <h2 style="font-size:30px; font-weight: bold;"> Si vous avez des questions, n'hésitez pas ! </h2>
    </div> """, unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

if "initialized" not in st.session_state:
    st.session_state.clear()  # Effacer tous les messages si nouvel accès
    st.session_state["initialized"] = True  # Marquer la session comme initialisée
    
# Initialisation des variables de session
if "gemini_model" not in st.session_state:
    st.session_state["gemini_model"] = "gemini-1.5-flash"

if "messages" not in st.session_state:
    st.session_state.messages = []

# Affichage de l'historique des messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Demande utilisateur
if prompt := st.chat_input("Pose-moi une question sur les astéroïdes ☄️"):
    with st.chat_message("user"):
        st.markdown(prompt)

    # Ajout du message utilisateur à l'historique
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Définition du contexte de Gemini
    system_prompt = """Tu es un Astrophysicien spécialisé dans les astéroïdes.
    Tu donnes des réponses précises et des données chiffrées. 
    Analyse bien la question pour comprendre si elle concerne l'astrophysique. 
    Par exemple, "comment créer une liste d'astéroïdes sur Python ?" une question du domaine de l'informatique. 
    Si la question sort du domaine de l'astrophysique, réponds : Je ne suis pas spécialisé dans ce domaine."""

    # Création d'une session de chat avec l'historique des messages
    chat = genai.GenerativeModel(st.session_state["gemini_model"]).start_chat(
        history=[{"role": "user", "parts": [system_prompt]}]
    )

    # Génération de la réponse
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        response = chat.send_message(prompt)  # Envoi du message à Gemini
        full_response = response.text  # Récupération de la réponse

        # Affichage progressif de la réponse
        message_placeholder.markdown(full_response)

    # Ajout de la réponse de Gemini à l'historique
    st.session_state.messages.append({"role": "assistant", "content": full_response})

