from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class Habitacion(BaseModel):
    id_habitacion: Optional[int] = None
    id_thabitacion: int
    numero: str
    estado: Optional[int] = 1
    date_created: Optional[datetime] = None
    date_updated: Optional[datetime] = None