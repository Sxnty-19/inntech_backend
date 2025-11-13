from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class TipoDocumento(BaseModel):
    id_tdocumento: Optional[int] = None
    nombre: str
    descripcion: Optional[str] = None
    estado: Optional[int] = 1
    date_created: Optional[datetime] = None
    date_updated: Optional[datetime] = None