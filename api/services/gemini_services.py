import google.generativeai as genai
import streamlit as st
import pandas as pd
import yaml
import json
import os

def GetGeminiConfigs(config_type : str):
    with open('configs/gemini_configs.yaml') as file:
        configs = yaml.load(file, Loader=yaml.FullLoader)
    return configs[config_type]


def GetGeminiModel(config : dict):
    genai.configure(api_key=os.environ["GEMINI_KEY"])
    if 'system_instruction' not in config:
        config['system_instruction'] = None
    if 'safety_settings' not in config:
        config['safety_settings'] = None
    if 'generation_config' not in config:
        config['generation_config'] = None
    model = genai.GenerativeModel(config['model']
                              ,system_instruction = config['system_instruction']
                              ,safety_settings = config['safety_settings']
                              ,generation_config = config['generation_config'])
    return model


def GetGeminiResponse(config : dict, prompt : str):
    model = GetGeminiModel(config)
    response = model.generate_content(prompt)
    return response

def GetMatchSummary(mainEvents : pd.DataFrame, narration_style : str):
    '''
    Retorna um resumo de uma partida específica
    '''
    config = GetGeminiConfigs('MATCH_NARRATIVE')
    model = GetGeminiModel(config)
    style = 'Estilo de narração: ' + narration_style + '\n'
    match_data = 'Dados da partida: \n' + json.dumps(pd.DataFrame(mainEvents).to_dict(orient='records'))
    response = model.generate_content(style + match_data)
    return response.text
