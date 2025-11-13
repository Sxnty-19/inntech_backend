from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class UsuarioHabitacion(BaseModel):
    id_uxh: Optional[int] = None
    id_usuario: int
    id_habitacion: int
    id_reserva: int
    date_check_in: Optional[datetime] = None
    date_check_out: Optional[datetime] = None
    estado: Optional[int] = 1
    date_created: Optional[datetime] = None
    date_updated: Optional[datetime] = None