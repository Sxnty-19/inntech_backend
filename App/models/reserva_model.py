from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class Reserva(BaseModel):
    id_reserva: Optional[int] = None
    id_usuario: int
    date_start: datetime
    date_end: datetime
    estado: Optional[int] = 1
    date_created: Optional[datetime] = None
    date_updated: Optional[datetime] = None