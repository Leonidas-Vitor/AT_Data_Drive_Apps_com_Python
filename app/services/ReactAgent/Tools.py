import streamlit as st
from langchain.tools import tool
from langchain_community.utilities import GoogleSerperAPIWrapper
from langchain_google_community import GoogleSearchRun
from langchain_google_community import GoogleSearchAPIWrapper
from langchain.agents import (AgentExecutor,
                              Tool,
                              create_self_ask_with_search_agent,
                              )
from langchain_experimental.agents import create_pandas_dataframe_agent
from langchain_core.language_models import BaseLanguageModel
from langchain_core.tools import BaseTool
from langchain import hub
from typing import Optional
from services import Statsbomb_Methods as sbm
import json
import pandas as pd

#-----------------Variáveis globais
llm = None
current_df = pd.DataFrame()
#-----------------ÚTEIS
@tool
def get_sb_list_of_events(action_input:str):
    '''
    Get the events of a specific match
    '''

    data = json.loads(action_input)
    match_id = data["match_id"]
    return sbm.get_sb_list_of_events(match_id)

@tool 
def get_sb_match_columns(action_input:str):
    '''
    Get the columns of a specific match
    '''

    data = json.loads(action_input)
    match_id = data["match_id"]
    return sbm.get_sb_match_columns(match_id)

@tool
def get_sb_events_type_count(action_input:str):
    '''
    Get the count events of a specific match
    '''

    data = json.loads(action_input)
    match_id = data["match_id"]
    event_type =  data["event_type"]
    return sbm.get_sb_events_filter_type(match_id, event_type).shape[0]

@tool
def get_sb_events_type_groupby_count(action_input:str):
    '''
    Get the count events of a specific match with groupby
    '''

    data = json.loads(action_input)
    match_id = data["match_id"]
    event_type =  data["event_type"]
    column_groupby = data["groupby_column"]
    return sbm.get_sb_events_filter_type(match_id, event_type).groupby(column_groupby).size()

#-- Método para buscar/filtrar o dataframe
#-- Métodos mais especializados]


@tool
def search_dataframe(query):
    '''
    Executa uma query no último dataframe obtido e retorna o resultado
    '''
    global current_df
    global llm

    #st.dataframe(current_df)

    agent = create_pandas_dataframe_agent(
        llm, 
        current_df, 
        allow_dangerous_code=True,
        return_intermediate_steps = True,
        max_iterations = 50,
        max_execution_time = 100,
        number_of_head_rows = 2000,
    )

    result = agent.invoke(query)
    #st.write(result)
    return result['output']

@tool
def get_sb_events_type(action_input:str):
    '''
    Get the events of a specific match
    '''
    data = json.loads(action_input)
    match_id = data["match_id"]
    event_type = data["event_type"]

    global current_df
    current_df = sbm.get_sb_events_filter_type(match_id, event_type)
    return current_df

@tool 
def get_players_from_match(action_input:str):
    '''
    Get the players of a specific match
    '''
    data = json.loads(action_input)
    match_id = data["match_id"]
    return sbm.get_sb_match_players(match_id)

@tool
def get_player_stats(action_input:str):
    '''
    Get the stats of a player
    '''
    data = json.loads(action_input)
    match_id = data["match_id"]
    player_id = data["player_id"]
    return sbm.get_sb_match_player_profile(match_id, player_id)

#-----------------INÚTEIS
@tool
def get_match_events(match_id):
    '''
    Get the events of a specific match
    '''
    return sbm.get_sb_events(match_id)

@tool
def count_events(action_input:str):
    '''
    Get the events of a specific match
    '''
    st.write(action_input)
    data = pd.DataFrame(json.loads(action_input))
    return data.shape[0]

@tool
def group_by(action_input:str):
    '''
    Agrupa um dataframe pela coluna especificada
    '''
    data = json.loads(action_input)
    df = pd.DataFrame(data['dataframe'])
    by = data['column']
    return df.groupby('column').size()



available_tools = {
        "google_search": Tool(
            name="Google Search",
            func=GoogleSerperAPIWrapper(serper_api_key=st.secrets["SERPER_KEY"]).run,
            description='''Busca no Google por informações. O input deve ser uma query de busca e só 
            deve ser em último caso.''',
        ),

        "get_events": Tool.from_function(
            func=get_sb_list_of_events,
            name="Match Events Types",
            description='''Retorna os tipos de eventos de uma partida específica, útil saber como filtrar eventos específicos. 
            O input deve ser o match_id.''',
        ),

        "get_columns": Tool.from_function(
            func=get_sb_match_columns,
            name="Match Columns",
            description='''Retorna as colunas de uma partida específica, útil para saber quais informações estão disponíveis.
            O input deve ser o match_id.''',
        ),

        "get_sb_events_type_groupby_count": Tool.from_function(
            func=get_sb_events_type_groupby_count,
            name="Match Events Count Groupby",
            description='''Conta o número de eventos de um tipo específico de uma partida específica com groupby,
            útil para saber quantos eventos de um tipo ocorreram em uma partida agrupados por uma coluna específica.
            O input deve ser o match_id, o event_type desejado e a groupby_column para agrupar. 
            O event_type pode ser obtido pela ferramenta get_events e a groupby_column pode ser obtida pela 
            ferramenta get_columns.''',
        ),

        #"match_events": Tool.from_function(
        #    func=get_match_events,
        #    name="Match Events",
        #    description='''Get the events of a specific match, useful to get pass, shots and 
        #    another events of a match. The input must be the match_id.''',
        #),
        
        "match_events": Tool.from_function(
            func=get_sb_events_type,
            name="Match Events",
            description='''Retorna um tipo específico de evento de uma partida específica, 
            útil para obter passes, chutes e outros eventos de uma partida. O input 
            deve ser o match_id e o event_type que PRECISA ser obtido 
            pela ferramenta get_events.''',
        ),

        "dataframe_search" : Tool.from_function(
            name="search_dataframe",
            func=search_dataframe,
            sample_size = 10000000,
            description='''Busca informações em um DataFrame. O input deve ser a pergunta a 
            ser respondida, o dataframe utilizado é o último que foi obtido. Não é necessário 
            informar o dataframe. A pergunta deve ser em feita em inglês. E deixe claro na pergunta que 
            a resposta não deve ser um código e sim um resultado.
            ''',
        ),

        "get_player_stats": Tool.from_function(
            func=get_player_stats,
            name="Player Stats",
            description='''Retorna as estatísticas de um jogador em uma partida específica, 
            útil para saber quantos passes, chutes e outros eventos um jogador realizou em uma partida. 
            O input deve ser o match_id e o player_id que pode ser obtido pela ferramenta get_players_from_match.''',
        ),

        "get_players_from_match": Tool.from_function(
            func=get_players_from_match,
            name="Players from Match",
            description='''Retorna os jogadores de uma partida específica, útil para saber quais jogadores
            participaram de uma partida. O input deve ser o match_id.''',
        ),


        # "match_events_count": Tool.from_function(
        #     func=get_sb_events_type_count,
        #     name="Match Events Count",
        #     description='''Conta o número de eventos de um tipo específico de uma partida específica, 
        #     útil para saber quantos eventos de um tipo ocorreram em uma partida. O input deve ser o 
        #     match_id e o event_type desejado. O event_type pode ser obtido pela ferramenta get_events.''',
        # ),
    
        # "group_by": Tool.from_function(
        #     func=group_by,
        #     name="Group By",
        #     description='''Agrupa um dataframe pela coluna especificada e retorna a quantidade de elementos agrupados. 
        #     O input deve ser um json com a coluna  e o dataframe a ser agrupado.
        #     Formato do input: {"column": "column_name", "dataframe": dataframe}''',
        # ),
}

def GetToolsNames_and_Descriptions() -> tuple[list[str], list[str]]:
    return [available_tools[tool].name for tool in available_tools.keys()], [available_tools[tool].description for tool in available_tools.keys()]

def SetLanguageModel(model: BaseLanguageModel):
    global llm
    llm = model

def GetTools() -> list[BaseTool]:
    global llm
    prompt = hub.pull("hwchase17/self-ask-with-search")

    search_wrapper = GoogleSearchRun(api_wrapper=
                                     GoogleSearchAPIWrapper(google_cse_id=st.secrets["GOOGLE_CSE_ID"], 
                                                            google_api_key=st.secrets["GOOGLE_API_KEY"]))
    search_tool = Tool(
        name="Intermediate Answer",
        func=search_wrapper.invoke,#DuckDuckGoSearchRun(api_wrapper=DuckDuckGoSearchAPIWrapper()),#DuckDuckGoSearchAPIWrapper().run,
        description="Search"
    )

    self_ask_agent = AgentExecutor(
        agent=create_self_ask_with_search_agent(
            llm, 
            [search_tool], 
            prompt
            ),
        tools = [search_tool],
        handle_parsing_errors=True,
        verbose=True,
    )

#================================================================================================

    tools = available_tools
    tools["critical_search"] = Tool.from_function(
           func=self_ask_agent.invoke,
           name="Self-ask agent",
           description='''
           A tool to answer complicated questions. Useful for when you need to answer questions about current events. Input should be a question.
           Example: "What is the capital of Brazil?".
           ''',
        )

    return [tools[tool] for tool in available_tools.keys()]


