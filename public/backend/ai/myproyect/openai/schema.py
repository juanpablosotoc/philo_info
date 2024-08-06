from pydantic import BaseModel
from typing import List, Optional

class ProcessedInfoInput(BaseModel):
    file_ids: Optional[List[str]] = []
    text: Optional[str] = None
