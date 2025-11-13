from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ModuloRol(BaseModel):
    id_mxr: Optional[int] = None
    id_modulo: int
    id_rol: int
    estado: Optional[int] = 1
    date_created: Optional[datetime] = None
    date_updated: Optional[datetime] = None