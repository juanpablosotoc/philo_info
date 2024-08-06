from typing import List, Optional, Literal
from datetime import datetime
from pydantic import BaseModel

class CreateExampleInput(BaseModel):
    engine_id: str
    tag: str
    children: Optional[List] = None

class CreateEngineInput(BaseModel):
    engine_name: str
    creation_date: Optional[datetime] = datetime.now()

    def __init__(self, engine_name: str, creation_date: datetime = datetime.now()):
        super().__init__(engine_name=engine_name, creation_date=creation_date)
