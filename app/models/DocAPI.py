import streamlit as st
import requests

st.title("Documentação da API (Swagger UI)")

# URL do Swagger
swagger_url = st.session_state['config']['API_URL'] + "docs"  # ou "http://127.0.0.1:8000/docs"

# Incluir estilo customizado com fundo branco
st.markdown(
    """
    <style>
    iframe {
        background-color: white;
        border: none;
        border-radius: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Exibir o iframe com Swagger
st.components.v1.iframe(swagger_url, height=600, scrolling=True)
