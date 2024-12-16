import streamlit as st
from services import DashboardComponents as at_i, Statsbomb_Methods, StatsPlots as sp, gemini_services as gs

at_i.select_match()

@st.cache_data
def GetMainEvents(match_id):
    return Statsbomb_Methods.get_sb_match_main_events(match_id)

st.title("Stats de Partidas de Futebol")

st.subheader('Estatísticas da partida',divider=True)

with st.container(border=True):
    at_i.ShowMatchSelected()

with st.container(border=True):
    st.subheader("Principais eventos da partida", divider=True)
    st.dataframe(GetMainEvents(st.session_state['partida_id']), use_container_width = True)

st.subheader('Narração da partida',divider=True)
with st.container(border=True):
    narration_style = st.radio('Escolha o tipo de narração',['Padrão' ,'Formal', 'Humorístico', 'Técnico'])
    st.write(gs.GetMatchSummary(
        GetMainEvents(st.session_state['partida_id']),
        narration_style))

st.subheader('Gráficos da partida',divider=True)

with st.container(border=True):
    st.markdown("##### Passes")
    sp.plot_passes()

    st.markdown("##### Finalizações")
    sp.plot_chutes()

with st.container(border=True):
    at_i.ExploreMatchEvents()


