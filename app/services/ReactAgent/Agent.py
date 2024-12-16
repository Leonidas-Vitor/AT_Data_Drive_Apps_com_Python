#from langchain import hub
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import LLMChain
from langchain.agents import create_react_agent, AgentExecutor
from langchain.prompts import PromptTemplate

import streamlit as st
from services.ReactAgent import Tools

def load_agent(memory) -> LLMChain:
    """
    Carrega o agente de chat com o modelo GEMINI-1.5-FLASH como base
    """
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash", 
        temperature=0.2, 
        google_api_key=st.secrets["GEMINI_KEY"],
        max_tokens=5000,
        timeout=None,
        max_retries=10,
        max_output_tokens=2048,
        )

    #prompt = hub.pull("hwchase17/react-chat")
    base_prompt = """
    Você é um espescialista em futebol e está conversando com um usuário que deseja saber mais 
    sobre a partida {match_name} (Id da partida: {match_id}).
    Seu objetivo é utilizar as ferramentas disponíveis para coletar os dados necessários para 
    responder a pergunta do usuário.

    Você tem acesso as seguintes ferramentas: {tool_names}
    Descrição das ferramentas: {tools}

    ## Utilização das ferramentas:
    - Cada ferramenta pode ser utilizada apenas uma vez.
    - Você pode utilizar quantas ferramentas desejar.
    - Você pode utilizar as ferramentas em qualquer ordem.
    - Você pode utilizar as ferramentas para coletar informações sobre os eventos da partida.
    - Elabore um plano de utilização da ferramenta antes de começar a coletar informações, seguindo o padrão:
        Thought: [Seu pensamento antes de utilizar a ferramenta.]
        Action: [Nome_da_ferramenta]
        Action Input:  [O input necessário para a ferramenta em formato json.]
        Observation: [O output ou resultado da ferramenta.]
        Coerência: A informação coletada é coerente com o motivo? (Sim/Não) Possuo todas as informações necessárias para coletar a informação desejada?
    - NÃO use nenhum caractere especial ou acentos, apenas letras e números.
    
    ## Exemplo:
    Thought: Quero saber quantos passes foram realizados na partida.
    Action: Match Events
    Action: {{"match_id": "12345", "event_type": "Pass"}}
    Observation: [Lista de eventos de passes]
    Resultado da ferramenta: Na partida foram realizados 100 passes.

    ## Condição de parada:
    - Ao coletar todas as informações necessárias para responder a pergunta do usuário, responda a pergunta com base nas 
    informações coletadas da seguinte forma:
    
    Thought: I have completed the analysis. No further tools are required.
    Final Answer: [Sua resposta final ao usuário.]
    Ferramentas utilizadas: [Ferraentas utilizadas para coletar informações.]
    

    ## Tarefa atual
    {input}

    ## Agent's Workspace
    {agent_scratchpad}
    """

    prompt = PromptTemplate(
       input_variables=["match_id",
                        "match_name",
                        "input",
                        "agent_scratchpad",
                        "tool_names",
                        "tools"],
       template=base_prompt
    )

    tools = Tools.GetTools(llm=llm)
    
    agent = create_react_agent(llm=llm, prompt=prompt, tools=tools)
    
    return AgentExecutor(
        agent=agent,
        tools=tools,
        #memory=memory,
        handle_parsing_errors=True,
        verbose=True,
        max_iterations=3
        )