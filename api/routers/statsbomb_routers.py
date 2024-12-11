import pandas as pd
from fastapi import APIRouter, HTTPException, Depends
from typing import List
from api.models.statsbomb_models import StockParams
from api.services import statsbomb_services as sb_services
#from services import calendar_services


router = APIRouter(
    prefix="/sb",
)

@router.get("/")
def Status():
    '''
    Retorna código 202 se o serviço estiver disponível
    '''
    return True

@router.get("/match/{match_id}")
def GetMatch(match_id: int):
    '''
    Retorna as informações de uma partida específica
    '''
    df = sb_services.get_sb_events(match_id)
    df.fillna('N/A', inplace=True)

    return sb_services.get_sb_events(match_id).to_dict(orient='records')

#3895302 -> Match id