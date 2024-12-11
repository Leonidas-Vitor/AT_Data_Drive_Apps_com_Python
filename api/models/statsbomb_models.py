from pydantic import BaseModel, Field
from datetime import date
from typing import Optional, List


class StockParams(BaseModel):
    ticker: str
    start : Optional[date] = None
    end : Optional[date] = date.today()
    period : Optional[str] = '5y'

    class Config:
        populate_by_name = True