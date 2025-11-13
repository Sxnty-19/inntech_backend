from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class Modulo(BaseModel):
    id_modulo: Optional[int] = None
    nombre: str
    ruta: str
    descripcion: Optional[str] = None
    estado: Optional[int] = 1
    date_created: Optional[datetime] = None
    date_updated: Optional[datetime] = None