import pandas as pd
import streamlit as st
import os
from dotenv import load_dotenv
load_dotenv()

import google.generativeai as genai
GOOGLE_API_KEY=os.getenv('google_api_key3')
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

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
st.title("Je suis un Astro Bot passionné par des astéroïdes, posez-moi vos questions")

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
    Tu donnes des réponses précises et des données chiffrées. Si la question sort du domaine de l'astrophysique, réponds : Je ne suis pas spécialisé dans ce domaine."""

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

