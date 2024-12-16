import streamlit as st
from services.ReactAgent import Agent, Tools 
from services.ReactAgent.Memory import MEMORY
from services.DashboardComponents import WriteHistory, HistorySize
from langchain_community.callbacks.streamlit import (
    StreamlitCallbackHandler,
)
from services import Statsbomb_Methods as at_g, DashboardComponents as at_i

at_i.select_match()

with st.spinner('Carregando aplicação...'):
    agent_chain = Agent.load_agent(MEMORY)
    tools = Tools.GetToolsNames_and_Descriptions()
    tools_names = tools[0]
    tools_description = tools[1]


st.header('Chat com o especialidade em futebol')


with st.container():  

    cols = st.columns([0.8,0.2])
    with cols[0]:
        messages = st.container(height=450)
        WriteHistory(MEMORY, messages)
        if HistorySize(MEMORY) < 3:
            if user_input := st.chat_input("Converse com o especialista de futebol", key='chat_input'):
                messages.chat_message("user").write(user_input)
                st.subheader('Pensamento do especialista',divider=True)
                with st.chat_message("assistant"):
                    st_callback = StreamlitCallbackHandler(st.container())
                    try:

                        input_data = {
                            "match_id": st.session_state["partida_id"],
                            "match_name": st.session_state["partida_nome"],
                            #"": st.session_state['competicao_nome'],
                            #"": st.session_state['competicao_id'],
                            #"": st.session_state['temporada_nome'],
                            #"": st.session_state['temporada_id'],
                            "tool_names": tools_names,
                            "tools": tools_description,
                            "input": user_input,
                            "agent_scratchpad": "",
                        }

                        st.write(f"Input to agent: {input_data}")
                        response = agent_chain.invoke(
                            input_data,
                            callbacks = [st_callback]
                        )
                        messages.chat_message("assistant").write(f"Assistente: {response['output']}")
                    except Exception as e:
                        st.error(f"Erro: {e}")
        else:
            st.write('Limite atingido, reinicia o chat para continuar')
    with cols[1]:
        st.write('Esse chat tem o limite de 3 interações, ao atingir o limite, reinicie o chat para continuar')
        st.write(f'Interações: {HistorySize(MEMORY)}/3')

        if st.button('Reiniciar'):
            #st.session_state[memoryKey].clear()
            MEMORY.clear()
            st.rerun()

        if HistorySize(MEMORY) == 3:
            st.warning('Limite atingido, reinicia o chat para continuar')
st.subheader('Memória', divider=True)
st.write(MEMORY.chat_memory.messages)
#st.write(MEMORY.list(config = {"configurable": {"thread_id": "abc123"}}))