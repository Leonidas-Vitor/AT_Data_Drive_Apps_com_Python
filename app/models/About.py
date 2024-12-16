import streamlit as st
from services import DashboardComponents as at_i

at_i.select_match()

st.title("Sobre")

st.write(
    """
    Olá, essa aplicação tem por objetivo entregar estatísticas de partidas de futebol e, principalmente, oferecer um chatbot para interação com o usuário utilizando diversas ferramentas para potencializar a experiência do usuário.
    """
)

st.subheader("Primeiros passos", divider=True)
st.write(
    '''
    No menu ao lado, você pode selecionar uma partida e as cores dos times que serão exibidos.
    ''')

st.subheader("Recursos disponíveis", divider=True)
st.write(
    f"""
    - **Chatbot**: Você pode conversar com o chatbot para obter informações sobre uma partida.
    - **Estatísticas**: Você pode visualizar estatísticas das partidas.
    - **Comparar jogadores**: Você poder comparar jogadores de uma partida.
    - **Documentação API**: Você pode acessar a documentação da API que está disponível na url {st.secrets['API_URL']}/docs.
    """
)

st.subheader("Outras informações", divider=True)
st.write(
    '''
    No github do projeto você pode encontrar encontrar um notebook em tests/API_Tests.ipynb com exemplos de como consumir a API e verificar os valores retornados.
    '''
)