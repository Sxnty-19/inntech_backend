from pydantic import BaseModel
from typing import List

class ReservaWithRooms(BaseModel):
    id_usuario: int
    date_start: str
    date_end: str
    habitaciones: List[int]