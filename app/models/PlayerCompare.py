import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import time
from mplsoccer.pitch import Pitch
from mplsoccer import VerticalPitch, add_image, FontManager, Sbopen
from services import Statsbomb_Methods as at_g, DashboardComponents as at_i

from matplotlib.colors import LinearSegmentedColormap

@st.cache_data
def GetPlayerProfile(match_id, player_id):
    '''
    Função para obter o perfil do jogador
    '''
    profile = at_g.get_sb_match_player_profile(match_id, player_id)
    return profile

at_i.select_match()

st.title("AT - Desenvolvimento Front-End com Python")
st.subheader("Comparar jogadores", divider=True)

metricas = ['total_passes' ,'total_chutes', 'total_dribles','total_interceptacoes','total_faltas','total_cartoes_amarelos','total_cartoes_vermelhos','total_gols','total_assistencias','total_lesoes',
'tempo_jogado','evento_sob_pressao']#,'taxa_gols','taxa_assistencias','taxa_dribles','passes_por_minuto','chutes_por_minuto','dribles_por_minuto','interceptacoes_por_minuto','faltas_por_minuto',
#'total_recuperacoes','total_recebimentos','total_mal_comportamento']

#metricas = ['total_passes' ,'total_chutes', 'total_dribles','total_interceptacoes','total_faltas','total_cartoes_amarelos','total_cartoes_vermelhos','total_gols','total_assistencias','total_lesoes',
#'tempo_jogado','evento_sob_pressao','taxa_gols','taxa_assistencias','taxa_dribles','passes_por_minuto','chutes_por_minuto','dribles_por_minuto','interceptacoes_por_minuto','faltas_por_minuto',
#'total_recuperacoes','total_recebimentos','total_mal_comportamento']

taxas = ['taxa_gols','taxa_assistencias','taxa_dribles','passes_por_minuto']#,'chutes_por_minuto','dribles_por_minuto','interceptacoes_por_minuto','faltas_por_minuto']

metricas_selecionadas = st.multiselect('Selecione as métricas', metricas, default=metricas)


cols = st.columns(2)

with cols[0]:
    player_a_container = st.container(border = True)
with cols[1]:
    player_b_container = st.container(border = True)

def show_select_player(team):
    st.markdown(f'### {team}')
    jogadores = at_g.get_sb_lineups(match_id=st.session_state['partida_id'])[team][['player_name','player_id','player_nickname','jersey_number']]
    #usar nickname se tiver, senão usar nome
    jogadores['player'] = jogadores['player_nickname'].fillna(jogadores['player_name'])
    #Adicionar o número da camisa no nome
    jogadores['player_jersey'] = jogadores['player'] + ' - ' + jogadores['jersey_number'].astype(str)
    #st.write(jogadores)
    jogador = st.selectbox('Selecione o jogador', jogadores['player_jersey'],key=team)
    jogador_foto = at_i.obter_foto_jogador(jogadores[jogadores['player_jersey'] == jogador]['player'].values[0])

    player_profile = GetPlayerProfile(st.session_state['partida_id'], jogadores[jogadores['player_jersey'] == jogador]['player_id'].values[0])

    st.write('### Posição:', player_profile['posicao'])

    if jogador_foto:
        st.markdown(
            f"""
            <div style="display: flex; justify-content: center;">
                <img src="{jogador_foto}" style="height: {250}px;">
            </div>
            """, unsafe_allow_html=True
        )
        #st.image(jogador_foto)#, use_column_width=True, output_format='auto')
    else:
        st.markdown(
            f"""
            <div style="display: flex; justify-content: center;">
                <img src="{'https://upload.wikimedia.org/wikipedia/commons/0/0a/No-image-available.png'}" style="height: {250}px;">
            </div>
            """, unsafe_allow_html=True
        )
        #st.image('https://upload.wikimedia.org/wikipedia/commons/0/0a/No-image-available.png')#, use_column_width=True, output_format='auto')


    player_events = at_g.get_sb_events(match_id=st.session_state['partida_id'])
    player_events = player_events[player_events['player'] == jogadores[jogadores['player_jersey'] == jogador]['player_name'].values[0]]
    return jogador, player_profile, player_events

with cols[0]:
    with player_a_container:
        try:
            jogador_a, player_a_profile, player_a_events = show_select_player(st.session_state["team_a"])
        except:
            st.error('Jogador não encontrado')
with cols[1]:
    with player_b_container:
        try:
            jogador_b, player_b_profile, player_b_events = show_select_player(st.session_state["team_b"])
        except:
            st.error('Jogador não encontrado')


def show_player_stats(team, player_profile, player_profile_compare):
    cols = st.columns(3)
    for i, m in enumerate(metricas_selecionadas):
        metric = player_profile[m]
        delta = float(player_profile[m] - player_profile_compare[m])
        if i % 3 == 0:
            with cols[0]:
                st.metric(m, metric, delta)
        elif i % 3 == 1:
            with cols[1]:
                st.metric(m, metric, delta)
        else:
            with cols[2]:
                st.metric(m, metric, delta)
        


def show_kde(player_events, color):
    st.write('### Mapa de calor')
    
    x = player_events['location'].apply(lambda x: x[0] if isinstance(x, (tuple, list)) else np.nan)
    y = player_events['location'].apply(lambda x: x[1] if isinstance(x, (tuple, list)) else np.nan)

    flamingo_cmap = LinearSegmentedColormap.from_list("Flamingo - 100 colors",
                                                ['#101010', color], N=100)
    pitch = VerticalPitch(line_color='#404040', line_zorder=2)
    fig, ax = pitch.draw(figsize=(4.4, 6.4))
    kde = pitch.kdeplot(x, y, ax=ax,
                        fill=True, levels=100,
                        thresh=0,
                        cut=4,
                        cmap=flamingo_cmap)
    fig.set_facecolor('none')
    ax.set_facecolor('none')
    st.pyplot(fig)

#taxa_selecionada = st.selectbox('Selecione a taxa', taxas)

# def BarChart(player_profile, color):
#     st.write('### Gráfico de barras')
#     df = pd.DataFrame([player_profile])
#     fig = px.bar(df, x='jogador', y=taxa_selecionada, color_discrete_sequence=[color])
#     st.plotly_chart(fig)

def SpiderChart(player_profile, player_color):
    '''
    Cria um gráfico de radar para comparar as taxas de um jogador com outro
    '''
    df = pd.DataFrame([player_profile])
    df = df[taxas]
    df = df.T.reset_index()
    df.columns = ['taxa', 'valor']
    df['jogador'] = player_profile['jogador']
    df['cor'] = player_color
    fig = px.line_polar(df, r='valor', theta='taxa', line_close=True, color='jogador', color_discrete_sequence=[player_color], template='plotly_dark')
    fig.update_layout(
    polar=dict(
        radialaxis=dict(range=[0, 1], showticklabels=True, ticks=""),  # Define o intervalo fixo
    ))
    st.plotly_chart(fig, use_container_width=True)

with player_a_container:
    st.divider()
    show_player_stats(st.session_state["team_a"], player_a_profile, player_b_profile)
    st.divider()
    show_kde(player_a_events, st.session_state['team_a_color'])
    st.divider()
    #BarChart(player_a_profile, st.session_state['team_a_color'])
    SpiderChart(player_a_profile, st.session_state['team_a_color'])
    

with player_b_container:
    st.divider()
    show_player_stats(st.session_state["team_b"], player_b_profile, player_a_profile)
    st.divider()
    show_kde(player_b_events, st.session_state['team_b_color'])
    st.divider()
    SpiderChart(player_b_profile, st.session_state['team_b_color'])



#Mapa de passes
#Mapa de chutes
#Mapa de dribles
#Mapa de interceptações


#Download

if st.button('Download dados selecionados', key='download'):
    with st.spinner('Preparando dados...'):
        df = pd.DataFrame([player_a_profile, player_b_profile])
        st.success('Download pronto para ser realizado!')
        st.download_button('Clique aqui para baixar o dataset filtrado', df.to_csv(), file_name='data.csv', mime='text/csv')
