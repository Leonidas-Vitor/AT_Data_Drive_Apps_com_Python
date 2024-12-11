import streamlit as st
from langchain_community.utilities import GoogleSerperAPIWrapper, GoogleFinanceAPIWrapper, GoogleTrendsAPIWrapper, DuckDuckGoSearchAPIWrapper
#from langchain.utilities import FinancialDatasetsAPIWrapper 
#from langchain.utilities import AskNewsAPIWrapper
from langchain_community.tools.ddg_search import DuckDuckGoSearchRun

from langchain_google_community import GoogleSearchRun
from langchain_google_community import GoogleSearchAPIWrapper

from langchain.agents import (AgentExecutor,
                              Tool,
                              create_self_ask_with_search_agent)

from langchain_core.language_models import BaseLanguageModel
from langchain_core.tools import BaseTool
from langchain import hub
from typing import Optional



def GetTools(llm: Optional[BaseLanguageModel] = None) -> list[BaseTool]:
  
    prompt = hub.pull("hwchase17/self-ask-with-search")

    search_wrapper = GoogleSearchRun(api_wrapper=GoogleSearchAPIWrapper(google_cse_id=st.secrets["GOOGLE_CSE_ID"], google_api_key=st.secrets["GOOGLE_API_KEY"]))
    search_tool = Tool(
        name="Intermediate Answer",
        func=search_wrapper.invoke,#DuckDuckGoSearchRun(api_wrapper=DuckDuckGoSearchAPIWrapper()),#DuckDuckGoSearchAPIWrapper().run,
        description="Search"
    )

    self_ask_agent = AgentExecutor(
        agent=create_self_ask_with_search_agent(llm, [search_tool], prompt),
        tools = [search_tool],
        handle_parsing_errors=True,
        verbose=True,
    )

#================================================================================================

    available_tools = {
        "google_search": Tool(
            name="Google Search",
            func=GoogleSerperAPIWrapper(serper_api_key=st.secrets["SERPER_KEY"]).run,
            description="Search Google for information. Input should be a search query.",
        ),

        "google_finance": Tool(
            name="Google Finance",
            func=GoogleFinanceAPIWrapper(serp_api_key=st.secrets["SERP_KEY"]).run,
            description="Search Google Finance for information. Input should be a search query.",
        ),

        "google_trends": Tool(
            name="Google Trends",
            func=GoogleTrendsAPIWrapper(serp_api_key=st.secrets["SERP_KEY"]).run,
            description="Search Google Trends for information. Input should be a search query.",
        ),

        "critical_search": Tool.from_function(
           func=self_ask_agent.invoke,
           name="Self-ask agent",
           description='''
           A tool to answer complicated questions. Useful for when you need to answer questions about current events. Input should be a question.
           Always use the format [{"input": "question"}].
           ''',
        ),
    }

    return [available_tools[tool] for tool in available_tools.keys()]