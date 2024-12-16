import streamlit as st
from langchain.tools import tool
from langchain_community.utilities import GoogleSerperAPIWrapper
from langchain_google_community import GoogleSearchRun
from langchain_google_community import GoogleSearchAPIWrapper
from langchain.agents import (AgentExecutor,
                              Tool,
                              create_self_ask_with_search_agent)
from langchain_core.language_models import BaseLanguageModel
from langchain_core.tools import BaseTool
from langchain import hub
from typing import Optional
from services import Statsbomb_Methods as sbm
import json
import pandas as pd

@tool
def get_match_events(match_id):
    '''
    Get the events of a specific match
    '''
    return sbm.get_sb_events(match_id)

@tool
def get_sb_list_of_events(action_input:str):
    '''
    Get the events of a specific match
    '''

    data = json.loads(action_input)
    match_id = data["match_id"]
    return sbm.get_sb_list_of_events(match_id)

@tool
def get_sb_events_type(action_input:str):
    '''
    Get the events of a specific match
    '''

    data = json.loads(action_input)
    match_id = data["match_id"]
    event_type =  data["event_type"]
    return sbm.get_sb_events_filter_type(match_id, event_type)

@tool
def get_sb_events_type_count(action_input:str):
    '''
    Get the events of a specific match
    '''

    data = json.loads(action_input)
    match_id = data["match_id"]
    event_type =  data["event_type"]
    return sbm.get_sb_events_filter_type(match_id, event_type).shape[0]

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
            deve ser o match_id e o event_type desejado. O event_type pode ser obtido 
            pela ferramenta get_events.''',
        ),

        "match_events_count": Tool.from_function(
            func=get_sb_events_type_count,
            name="Match Events Count",
            description='''Conta o número de eventos de um tipo específico de uma partida específica, 
            útil para saber quantos eventos de um tipo ocorreram em uma partida. O input deve ser o 
            match_id e o event_type desejado. O event_type pode ser obtido pela ferramenta get_events.''',
        ),

        "group_by": Tool.from_function(
            func=group_by,
            name="Group By",
            description='''Agrupa um dataframe pela coluna especificada e retorna a quantidade de elementos agrupados. 
            O input deve ser um json com a coluna  e o dataframe a ser agrupado.
            Formato do input: {"column": "column_name", "dataframe": dataframe}''',
        ),
}

def GetToolsNames_and_Descriptions() -> tuple[list[str], list[str]]:
    return [available_tools[tool].name for tool in available_tools.keys()], [available_tools[tool].description for tool in available_tools.keys()]

def GetTools(llm: Optional[BaseLanguageModel] = None) -> list[BaseTool]:
  
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
           Always use the format [{"input": "question"}].
           ''',
        )

    return [tools[tool] for tool in available_tools.keys()]


