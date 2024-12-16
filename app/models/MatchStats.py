import streamlit as st
from services import DashboardComponents as at_i, StatsPlots as sp

at_i.select_match()

st.title("Stats de Partidas de Futebol")

st.subheader('Estatísticas da partida',divider=True)

with st.container(border=True):
    at_i.ShowMatchSelected()

st.subheader('Narração da partida',divider=True)
with st.container(border=True):
    st.write('Em breve...')

st.subheader('Gráficos da partida',divider=True)

with st.container(border=True):
    st.markdown("##### Passes")
    sp.plot_passes()

    st.markdown("##### Finalizações")
    sp.plot_chutes()


