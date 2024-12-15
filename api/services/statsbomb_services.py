import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import plotly.express as px
import json
import time
from statsbombpy import sb
from mplsoccer.pitch import Pitch
from SPARQLWrapper import SPARQLWrapper, JSON


#@st.cache_data
def get_sb_competitions():
    '''
    Retorna as competições disponíveis no StatsBomb
    '''
    try:
        return sb.competitions().fillna('N/A')
    except:
        return None

#@st.cache_data
def get_sb_matches(competition_id, season_id):
    '''
    Retorna as partidas de uma competição e temporada específicas
    '''
    try:
        return sb.matches(competition_id=competition_id, season_id=season_id).fillna('N/A')
    except:
        return None

#@st.cache_data
def get_sb_events(match_id):
    '''
    Retorna os eventos de uma partida específica
    '''
    try:
        return sb.events(match_id=match_id).fillna('N/A')
    except:
        return None

#@st.cache_data
def get_sb_events_types(match_id):
    '''
    Retorna os eventos de uma partida específica separados por tipo (ex: passes, chutes, etc.)
    '''
    try:
        return sb.events(match_id=match_id, split=True, flatten_attrs=False)
    except:
        return None

#@st.cache_data
def get_sb_events_type(match_id, event_type):
    '''
    Retorna os eventos de uma partida específica de um tipo específico (ex: passes, chutes, etc.)
    '''
    try:
        return sb.events(match_id=match_id, split=True, flatten_attrs=False)[event_type]
    except:
        return None

#@st.cache_data
def get_sb_match_main_events(match_id):
    '''
    Retorna os principais eventos de uma partida específica
    '''
    try:
        events = get_sb_events(match_id)
        main_events = events[(events['type'].isin(['Pass', 'Shot', 'Dribble', 'Interception', 
                                                   'Foul Committed', 'Substitution', 
                                                   'Injury Stoppage', 'Bad Behaviour']))]
        
        main_events = main_events[['type', 'minute', 'team', 'player', 'position', 'location',
         'bad_behaviour_card','dribble_outcome','interception_outcome','pass_goal_assist','shot_outcome','substitution_outcome','substitution_replacement','foul_committed_card']]

        main_events = main_events[(main_events['pass_goal_assist'] == True) | (main_events['type'] != 'Pass')]
                
        return main_events
    except:
        return None
    
def get_sb_match_players(match_id):
    '''
    Retorna os jogadores de uma partida específica
    '''
    try:
        events = get_sb_events(match_id)
        players = events[['player_id', 'player', 'team']].drop_duplicates()
        return players
    except:
        return None
    
def get_sb_match_player_profile(match_id, player_id):
    '''
    Retorna o perfil de um jogador em uma partida específica
    '''
    #try:
    events = get_sb_events(match_id)
    player_events = events[events['player_id'] == player_id]
    player_events = player_events[(player_events['type'].isin(['Pass', 'Shot', 'Dribble', 'Interception', 
                                                'Foul Committed', 'Substitution', 
                                                'Injury Stoppage', 'Bad Behaviour', 
                                                'Ball Recovery', 'Ball Receipt*']))]
    
    #player_events = player_events[['type', 'minute', 'team', 'player', 'position', 'location',
    # 'bad_behaviour_card','dribble_outcome','interception_outcome','pass_goal_assist','shot_outcome','substitution_outcome','substitution_replacement','foul_committed_card']]
    
    profile = {}
    profile['jogador'] = player_events['player'].values[0]
    profile['posicao'] = player_events['position'].values[0]

    profile['total_passes'] = player_events[player_events['type'] == 'Pass'].shape[0]
    profile['total_chutes'] = player_events[player_events['type'] == 'Shot'].shape[0]
    profile['total_dribles'] = player_events[player_events['type'] == 'Dribble'].shape[0]
    profile['total_interceptacoes'] = player_events[player_events['type'] == 'Interception'].shape[0]
    profile['total_faltas'] = player_events[player_events['type'] == 'Foul Committed'].shape[0]
    profile['total_cartoes_amarelos'] = player_events[player_events['bad_behaviour_card'] == 'yellow card'].shape[0] + player_events[player_events['foul_committed_card'] == 'yellow card'].shape[0]
    profile['total_cartoes_vermelhos'] = player_events[player_events['bad_behaviour_card'] == 'red card'].shape[0] + player_events[player_events['foul_committed_card'] == 'red card'].shape[0]
    profile['total_gols'] = player_events[player_events['type'] == 'Shot'][player_events['shot_outcome'] == 'Goal'].shape[0]
    profile['total_assistencias'] = player_events[player_events['pass_goal_assist'] == True].shape[0]
    profile['total_lesoes'] = player_events[player_events['type'] == 'Injury Stoppage'].shape[0]
    profile['tempo_jogado'] = player_events['minute'].max() - player_events['minute'].min()
    profile['evento_sob_pressao'] = player_events[player_events['under_pressure'] == True].shape[0]

    profile['taxa_gols'] = round(profile['total_gols'] / profile['total_chutes'], 2)
    profile['taxa_assistencias'] = round(profile['total_assistencias'] / profile['total_passes'], 2)
    profile['taxa_dribles'] = round(player_events[(player_events['type'] == 'Dribble') & (player_events['dribble_outcome'] == 'Complete')].shape[0] / profile['total_dribles'], 2)
    profile['passes_por_minuto'] = round(profile['total_passes'] / profile['tempo_jogado'], 2)
    profile['chutes_por_minuto'] = round(profile['total_chutes'] / profile['tempo_jogado'], 2)
    profile['dribles_por_minuto'] = round(profile['total_dribles'] / profile['tempo_jogado'], 2)
    profile['interceptacoes_por_minuto'] = round(profile['total_interceptacoes'] / profile['tempo_jogado'], 2)
    profile['faltas_por_minuto'] = round(profile['total_faltas'] / profile['tempo_jogado'], 2)

    profile['total_recuperacoes'] = player_events[player_events['type'] == 'Ball Recovery'].shape[0]
    profile['total_recebimentos'] = player_events[player_events['type'] == 'Ball Receipt*'].shape[0]
    profile['total_mal_comportamento'] = player_events[player_events['type'] == 'Bad Behaviour'].shape[0]

    return profile#pd.DataFrame(profile, index=[0]).fillna('N/A').to_dict(orient='records')
    
    #except:
    #    return None

#----------------EXCLUSIVO STREAMLIT----------------
def select_match():
    '''
    Função para selecionar a partida no sidebar do Streamlit e armazenar as informações da competição, temporada e partida selecionadas em st.session_state para uso posterior na aplicação
    '''
    df_comp = get_sb_competitions()
    competicoes = df_comp[['competition_name','competition_id']].drop_duplicates()
    competicoes.reset_index(drop=True, inplace=True)
    with st.sidebar:
        st.markdown("## Selecionar partida")
        try:
            competicao_selecionada = st.selectbox('Selecione a competição', competicoes['competition_name'], index=int(competicoes['competition_name'].loc[competicoes['competition_name'] == st.session_state['competicao_nome']].index[0]))
        except:
            competicao_selecionada = st.selectbox('Selecione a competição', competicoes['competition_name'])
        competicao_id = competicoes[competicoes['competition_name'] == competicao_selecionada]['competition_id'].values[0]

        if competicao_selecionada:
            temporadas = df_comp[df_comp['competition_name'] == competicao_selecionada][['season_name', 'season_id']].drop_duplicates().reset_index(drop=True)
            try:
                temporada_selecionada = st.selectbox('Selecione a temporada', temporadas['season_name'], index=int(temporadas[temporadas['season_name'] == st.session_state['temporada_nome']].index[0]))
            except:
                temporada_selecionada = st.selectbox('Selecione a temporada', temporadas['season_name'])
            temporada_id = temporadas[temporadas['season_name'] == temporada_selecionada]['season_id'].values[0]

        if competicao_id and temporada_id:
            partidas = get_sb_matches(competition_id=competicao_id, season_id=temporada_id)
            partidas['partida'] = partidas['home_team'] + ' x ' + partidas['away_team'] + ' - ' + partidas['match_date']

            try:
                partida_selecionada = st.selectbox('Selecione a partida', partidas['partida'], index=int(partidas[partidas['partida'] == st.session_state['partida_nome']].index[0]))
            except:
                partida_selecionada = st.selectbox('Selecione a partida', partidas['partida'])
            partida_id = partidas[partidas['partida'] == partida_selecionada]['match_id'].values[0]

        if partida_id:
            cols = st.columns([0.5,0.5])
            team_a = partidas[partidas['match_id'] == partida_id]['home_team'].values[0]
            team_b = partidas[partidas['match_id'] == partida_id]['away_team'].values[0]
            with cols[0]:
                try:
                    st.session_state['team_a_color'] = st.color_picker(f'Cor do time: {team_a}', st.session_state['team_a_color'])
                except:
                    st.session_state['team_a_color'] = st.color_picker(f'Cor do time: {team_a}', '#111111')
            with cols[1]:
                try:
                    st.session_state['team_b_color'] = st.color_picker(f'Cor do time: {team_b}', st.session_state['team_b_color'])
                except:
                    st.session_state['team_b_color'] = st.color_picker(f'Cor do time: {team_b}', '#000000')

        st.session_state['competicao_nome'] = competicao_selecionada
        st.session_state['competicao_id'] = competicao_id
        st.session_state['temporada_nome'] = temporada_selecionada
        st.session_state['temporada_id'] = temporada_id
        st.session_state['partida_nome'] = partida_selecionada
        st.session_state['partida_id'] = partida_id
        st.session_state['team_a'] = team_a
        st.session_state['team_b'] = team_b

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
