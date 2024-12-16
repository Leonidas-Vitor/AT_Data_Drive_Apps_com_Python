import streamlit as st
from services import Statsbomb_Methods as at_g, ColorMethods as cm
from SPARQLWrapper import SPARQLWrapper, JSON
from mplsoccer.pitch import Pitch
from mplsoccer import VerticalPitch, add_image, FontManager, Sbopen
from matplotlib.colors import LinearSegmentedColormap
import pandas as pd
import time

def select_match():
    '''
    Função para selecionar a partida no sidebar do Streamlit e armazenar as informações da competição, temporada e partida selecionadas em st.session_state para uso posterior na aplicação
    '''
    df_comp = at_g.get_sb_competitions()
    competicoes = df_comp[['competition_name','competition_id']].drop_duplicates()
    competicoes.reset_index(drop=True, inplace=True)
    #cols = st.columns(4)
    with st.sidebar:
        try:
            competicao_selecionada = st.selectbox('Selecione a competição', competicoes['competition_name'], index=int(competicoes['competition_name'].loc[competicoes['competition_name'] == st.session_state['competicao_nome']].index[0]))
        except:
            competicao_selecionada = st.selectbox('Selecione a competição', competicoes['competition_name'])
        competicao_id = competicoes[competicoes['competition_name'] == competicao_selecionada]['competition_id'].values[0]
    #with cols[1]:
        if competicao_selecionada:
            temporadas = df_comp[df_comp['competition_name'] == competicao_selecionada][['season_name', 'season_id']].drop_duplicates().reset_index(drop=True)
            try:
                temporada_selecionada = st.selectbox('Selecione a temporada', temporadas['season_name'], index=int(temporadas[temporadas['season_name'] == st.session_state['temporada_nome']].index[0]))
            except:
                temporada_selecionada = st.selectbox('Selecione a temporada', temporadas['season_name'])
            temporada_id = temporadas[temporadas['season_name'] == temporada_selecionada]['season_id'].values[0]
    #with cols[2]:
        if competicao_id and temporada_id:
            partidas = at_g.get_sb_matches(competition_id=competicao_id, season_id=temporada_id)
            partidas['partida'] = partidas['home_team'] + ' x ' + partidas['away_team'] + ' - ' + partidas['match_date']

            try:
                partida_selecionada = st.selectbox('Selecione a partida', partidas['partida'], index=int(partidas[partidas['partida'] == st.session_state['partida_nome']].index[0]))
            except:
                partida_selecionada = st.selectbox('Selecione a partida', partidas['partida'])
            partida_id = partidas[partidas['partida'] == partida_selecionada]['match_id'].values[0]
    #with cols[3]:
        if partida_id:
            cols = st.columns([0.5,0.5])
            team_a = partidas[partidas['match_id'] == partida_id]['home_team'].values[0]
            team_b = partidas[partidas['match_id'] == partida_id]['away_team'].values[0]
            with cols[0]:
                if 'team_a_color' in st.session_state:
                    st.session_state['team_a_color'] = st.color_picker(f'Cor do time: {team_a}', st.session_state['team_a_color'])
                else:
                    st.session_state['team_a_color'] = st.color_picker(f'Cor do time: {team_a}', value=cm.gerar_cor_hex())
            with cols[1]:
                if 'team_b_color' in st.session_state:
                    st.session_state['team_b_color'] = st.color_picker(f'Cor do time: {team_b}', st.session_state['team_b_color'])
                else:
                    st.session_state['team_b_color'] = st.color_picker(f'Cor do time: {team_b}', value=cm.gerar_cor_hex())

        st.session_state['competicao_nome'] = competicao_selecionada
        st.session_state['competicao_id'] = competicao_id
        st.session_state['temporada_nome'] = temporada_selecionada
        st.session_state['temporada_id'] = temporada_id
        st.session_state['partida_nome'] = partida_selecionada
        st.session_state['partida_id'] = partida_id
        st.session_state['team_a'] = team_a
        st.session_state['team_b'] = team_b

#Adicionar mais informações sobre a partida, ao menos igual as da API
def ShowMatchSelected():
    if (st.session_state['competicao_nome'] and st.session_state['temporada_nome'] 
        and st.session_state['partida_nome']):
        match_events = at_g.get_sb_events(match_id=st.session_state['partida_id'])
        st.success("Partida selecionada com sucesso!")
        cols = st.columns([0.2,0.2,0.2,0.2])
        with cols[0]:
            competicao = at_g.get_sb_matches(competition_id=st.session_state['competicao_id'], season_id=st.session_state['temporada_id'])
            st.metric("Placar", competicao[(competicao['match_id'] == st.session_state['partida_id'])][['home_score','away_score']].values[0][0].astype(str) + 
                ' x ' + competicao[(competicao['match_id'] == st.session_state['partida_id'])][['home_score','away_score']].values[0][1].astype(str))
            
            st.metric("Total de dribles", match_events[match_events['type'] == 'Dribble'].shape[0])
        with cols[1]:
            st.metric("Total de interceptações", match_events[match_events['type'] == 'Interception'].shape[0])
            st.metric("Total de passes", match_events[match_events['type'] == 'Pass'].shape[0])
        with cols[2]:
            st.metric("Total de faltas", match_events[match_events['type'] == 'Foul Committed'].shape[0])
            st.metric("Total de substituições", match_events[match_events['type'] == 'Substitution'].shape[0])
        with cols[3]:
            st.metric("Total de chutes", match_events[match_events['type'] == 'Shot'].shape[0])
            st.metric("Total de paralisações", match_events[match_events['type'] == 'Injury Stoppage'].shape[0])

        st.subheader("Principais eventos da partida", divider=True)
        main_events = at_g.get_sb_match_main_events(match_id=st.session_state['partida_id'])
        st.dataframe(main_events, use_container_width = True)
    else :
        st.error("Selecione uma partida")

def ExploreMatchEvents():
    events = at_g.get_sb_events_types(st.session_state['partida_id'])
    keys = list(events.keys())
    event_type = st.selectbox('Selecione o tipo de evento para visualizá-los', keys)
    st.dataframe(events[event_type], use_container_width = True)

def obter_foto_jogador(nome_jogador):
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    query = f"""
    SELECT ?thumbnail WHERE {{
        ?player a dbo:SoccerPlayer ;
                foaf:name "{nome_jogador}"@en ;
                dbo:thumbnail ?thumbnail .
    }}
    """
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    if results["results"]["bindings"]:
        foto_url = results["results"]["bindings"][0]["thumbnail"]["value"]
        return foto_url
    else:
        return None
    

#-------------------------------------------------CHATBOT-------------------------------------------------#

def WriteHistory(MEMORY, messages):
    '''
    Escreve o histórico de mensagens
    '''
    try:
        avatars = {
            "human": "user",
            "ai": "assistant"
        }
        #for history in st.session_state[memoryKey]:
            #role = 'Usuário' if 'Usuário' in history else 'Assistente'
            #icon = 'user' if 'Usuário' in history else 'assistant'
            #icon = entities[history['Role']]
            #messages.chat_message(icon).write(history['Msg'])
        for msg in MEMORY.chat_memory.messages:
            messages.chat_message(avatars[msg.type]).write(msg.content)
    except Exception as e:
        st.error(e)
        st.error('Erro ao escrever histórico')
        pass

def HistorySize(MEMORY):
    '''
    Retorna o tamanho do histórico
    '''
    user_count = 0
    for msg in MEMORY.chat_memory.messages:
        if msg.type == 'human':
            user_count += 1
    return user_count