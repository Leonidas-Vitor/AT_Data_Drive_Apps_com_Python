from langchain.tools import tool
import json

@tool
def get_last_material_facts(ticker : str) -> str:
    '''
    Get the last material facts of a company
    '''
    return ''


