from pydantic import BaseModel, Field
from datetime import date
from typing import Optional, List, Literal

class MatchParams(BaseModel):
    match_id: int

class MatchSummary(BaseModel):
    match_id: int
    narration_style : Optional[Literal['Padrão' ,'Formal', 'Humorístico', 'Técnico']] = 'Padrão'

class PlayerParams(BaseModel):
    match_id: int
    player_id: int