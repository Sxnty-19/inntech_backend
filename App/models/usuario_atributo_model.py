from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class UsuarioAtributo(BaseModel):
    id_uxa: Optional[int] = None
    id_usuario: int
    id_atributo: int
    valor: Optional[str] = None
    estado: Optional[int] = 1
    date_created: Optional[datetime] = None
    date_updated: Optional[datetime] = None