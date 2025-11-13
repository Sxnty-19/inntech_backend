from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class TipoHabitacion(BaseModel):
    id_thabitacion: Optional[int] = None           
    nombre: str                                    
    descripcion: Optional[str] = None              
    capacidad_max: int      
    estado: Optional[int] = 1                       
    date_created: Optional[datetime] = None        
    date_updated: Optional[datetime] = None        