import streamlit as st
import yaml
import json
from streamlit_extras.app_logo import add_logo

intro_page = st.Page("models/Intro.py", title="Introdução", icon="🏡")#📑

#business_model_canvas = st.Page("model/BusinessModelCanvas.py", title="Business Model Canvas", icon="🗺️")
#project_charter = st.Page("model/ProjectCharter.py", title="Project Charter", icon="🛣️")
about = st.Page("models/About.py", title="Sobre", icon="✨")

aplication = st.Page("models/MatchStats.py", title="MatchStats", icon="⚽")
#update_db = st.Page("model/UpdateDB.py", title="Atualizar Banco de Dados", icon="🔄")
doc_api = st.Page("models/DocAPI.py", title="Doc API", icon="📡")

pages = {
        'Introdução': [intro_page],
        'Sobre': [about],
        'Aplicação': [aplication, doc_api, ]
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

pg.run()

