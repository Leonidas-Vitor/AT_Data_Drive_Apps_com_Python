from langchain import hub

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import LLMChain
from langchain.agents import create_react_agent, AgentExecutor
from langchain.memory import ConversationBufferMemory
#from langgraph.checkpoint.memory import MemorySaver

#from langchain_experimental.plan_and_execute.planners.chat_planner import load_chat_planner
#from langchain_experimental.plan_and_execute.executors.agent_executor import load_agent_executor
#from langchain_experimental.plan_and_execute import PlanAndExecute
from typing import Literal

import streamlit as st
from services import Tools as tl

ReasoningStrategy = Literal["zero_shot_react", "plan_and_solve", "CONVERSATIONAL_REACT_DESCRIPTION"]

def load_agent(memory, strategy: ReasoningStrategy = "CONVERSATIONAL_REACT_DESCRIPTION",) -> LLMChain:
    """
    """
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash", 
        temperature=0.0, 
        google_api_key=st.secrets["GEMINI_KEY"],
        max_tokens=5000,
        timeout=None,
        max_retries=10,
        max_output_tokens=2048,
        )
    #llm.with_retry(retry_if_exception_type=[ResourceExhausted])
    tools = tl.GetTools(llm=llm)

    #if strategy == "plan_and_solve":
    #    planner = load_chat_planner(llm, output_format="Thought and Action")
    #    executor = load_agent_executor(
    #        llm,
    #        tools,
    #        output_format="Thought and Action",
    #        handle_parsing_errors=True,
    #        verbose=True
    #    )
    #    return PlanAndExecute(planner=planner, executor=executor, verbose=True)
    
    prompt = hub.pull("hwchase17/react-chat")
    #agent = langchain.agents.initialize_agent(tools, llm, agent=langchain.agents.AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION, memory=memory, verbose=True)

    agent = create_react_agent(llm=llm, prompt=prompt, tools=tools)
    
    return AgentExecutor(agent=agent,
                         tools=tools,
                         memory=memory,
                         #checkpointer=memory,
                         handle_parsing_errors=True,
                         verbose=True)