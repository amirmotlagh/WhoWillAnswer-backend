from typing import Any, Optional
from pydantic import BaseModel

class IncomingWSMessage(BaseModel):
    type: str
    data: Optional[Any] = None
    receiver_id: Optional[int] = None