import streamlit as st
import yaml
import json
from streamlit_extras.app_logo import add_logo

intro_page = st.Page("models/Intro.py", title="Introdução", icon="🏡")#📑

about = st.Page("models/About.py", title="Sobre", icon="✨")

matchStats = st.Page("models/MatchStats.py", title="MatchStats", icon="⚽")
playerCompare = st.Page("models/PlayerCompare.py", title="Comparar Jogadores", icon="🔍")
chatbot = st.Page("models/Chatbot.py", title="Chatbot", icon="💬")
doc_api = st.Page("models/DocAPI.py", title="Doc API", icon="📡")

pages = {
        'Introdução': [intro_page],
        'Sobre': [about],
        'Aplicação': [matchStats, playerCompare, chatbot, doc_api, ]
}


pg = st.navigation(pages)

st.set_page_config(
        page_title="Intro",
        page_icon="images/Infnet_logo.png",
        layout="wide",
        initial_sidebar_state = "expanded")


#Carregar configurações
@st.cache_data
def load_configs():
        with open('configs/gemini_config.yaml', 'r') as arquivo:
                st.session_state['gemini_config'] = yaml.safe_load(arquivo)

add_logo("images/infnet-30-horizontal-branco.png", height=156)


#at_i.ShowMatchSelector()

pg.run()

