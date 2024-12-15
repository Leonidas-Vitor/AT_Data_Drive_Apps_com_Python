import streamlit as st
from api.services import statsbomb_services as at_g

def ShowMatchSelector():
    if (st.session_state['competicao_nome'] and st.session_state['temporada_nome'] 
        and st.session_state['partida_nome']):
        match_events = at_g.get_sb_events(match_id=st.session_state['partida_id'])
        st.success("Partida selecionada com sucesso!")
        cols = st.columns([0.3,0.2,0.2,0.2,0.2])
        with cols[0]:
            with st.expander("Informações da partida selecionada", expanded=True):
                st.write("Competição: " + st.session_state['competicao_nome'])
                st.write("Temporada: " + st.session_state['temporada_nome'])
                st.write("Partida: " + st.session_state['partida_nome'])
        with cols[1]:
            df_comp = at_g.get_sb_competitions()
            st.metric("Placar", at_g.get_sb_matches(competition_id=st.session_state['competicao_id'], 
                season_id=st.session_state['temporada_id'])[(at_g.get_sb_matches(competition_id=st.session_state['competicao_id'], 
                season_id=st.session_state['temporada_id'])['match_id'] == st.session_state['partida_id'])][['home_score','away_score']].values[0][0].astype(str) + 
                ' x ' + at_g.get_sb_matches(competition_id=st.session_state['competicao_id'], 
                season_id=st.session_state['temporada_id'])[(at_g.get_sb_matches(competition_id=st.session_state['competicao_id'], 
                season_id=st.session_state['temporada_id'])['match_id'] == st.session_state['partida_id'])][['home_score','away_score']].values[0][1].astype(str))
                
            st.metric("Total de dribles", match_events[match_events['type'] == 'Dribble'].shape[0])
        with cols[2]:
            st.metric("Total de interceptações", match_events[match_events['type'] == 'Interception'].shape[0])
            st.metric("Total de passes", match_events[match_events['type'] == 'Pass'].shape[0])
        with cols[3]:
            st.metric("Total de faltas", match_events[match_events['type'] == 'Foul Committed'].shape[0])
            st.metric("Total de substituições", match_events[match_events['type'] == 'Substitution'].shape[0])
        with cols[4]:
            st.metric("Total de chutes", match_events[match_events['type'] == 'Shot'].shape[0])
            st.metric("Total de paralisações", match_events[match_events['type'] == 'Injury Stoppage'].shape[0])

        events = at_g.get_sb_events_types(st.session_state['partida_id'])
        keys = list(events.keys())
        event_type = st.selectbox('Selecione o tipo de evento para visualizá-los', keys)
        st.dataframe(events[event_type], use_container_width = True)
    else :
        st.error("Selecione uma partida")
    #st.dataframe(match_events[match_events['type'] == 'Injury Stoppage'])

    st.subheader("Visualizações", divider=True)