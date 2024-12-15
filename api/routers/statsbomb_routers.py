import pandas as pd
from fastapi import APIRouter, HTTPException, Depends
from typing import List
from api.models.statsbomb_models import StockParams
from api.services import statsbomb_services as sb_services
from api.services import gemini_services as ge_services
from api.models import InputModels as in_models, OutputModels as out_models
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

@router.get("/match")
def GetMatch(params: in_models.MatchParams = Depends()):
    '''
    Retorna as informações de uma partida específica
    '''
    df = sb_services.get_sb_events(params.match_id)
    df.fillna('N/A', inplace=True)

    return sb_services.get_sb_events(params.match_id).to_dict(orient='records')

@router.get("/match_main_events")
def GetMatchMainEvents(params: in_models.MatchParams = Depends()):
    '''
    Retorna os principais eventos de uma partida específica
    '''
    return sb_services.get_sb_match_main_events(params.match_id).to_dict(orient='records')

@router.get('/match_players')
def GetMatchPlayers(params: in_models.MatchParams = Depends()):
    '''
    Retorna os jogadores de uma partida específica
    '''
    return sb_services.get_sb_match_players(params.match_id).to_dict(orient='records')

#-----------------------MAIN ENDPOINTS-----------------------

@router.get('/match_summary', response_model=out_models.MatchSummary)
def GetMatchSummary(params: in_models.MatchSummary = Depends()):
    '''
    Retorna um resumo de uma partida específica
    '''
    print(params)
    mainEvents = GetMatchMainEvents(in_models.MatchParams(match_id=params.match_id))
     
    matchSummary = out_models.MatchSummary(match_summary=ge_services.GetMatchSummary(mainEvents, params.narration_style))
    return matchSummary

@router.get("/player_profile", response_model=out_models.PlayerProfile)
def GetPlayerProfile(params: in_models.PlayerParams = Depends()):
    '''
    Retorna o perfil de um jogador em uma partida específica
    '''
    try:
        player_profile = sb_services.get_sb_match_player_profile(match_id=params.match_id, player_id=params.player_id)
        player_profile = out_models.PlayerProfile(**player_profile)
        return player_profile
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

#3895302 -> Match id