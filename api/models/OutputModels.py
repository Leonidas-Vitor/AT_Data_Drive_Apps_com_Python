from pydantic import BaseModel, Field
from datetime import date
from typing import Optional, List, Literal

class MatchSummary(BaseModel):
    match_summary: str

class PlayerProfile(BaseModel):
    jogador : str
    posicao : str
    total_passes : int
    total_chutes : int
    total_dribles : int
    total_interceptacoes : int
    total_faltas : int
    total_cartoes_amarelos : int
    total_cartoes_vermelhos : int
    total_gols : int
    total_assistencias : int
    total_lesoes : int
    tempo_jogado : int
    evento_sob_pressao : int
    taxa_gols : float
    taxa_assistencias : float
    taxa_dribles : float
    passes_por_minuto : float
    chutes_por_minuto : float
    dribles_por_minuto : float
    interceptacoes_por_minuto : float
    faltas_por_minuto : float
    total_recuperacoes : int
    total_recebimentos : int
    total_mal_comportamento : int