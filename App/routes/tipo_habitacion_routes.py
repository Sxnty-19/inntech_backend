from fastapi import APIRouter
from controllers.tipo_habitacion_controller import TipoHabitacionController
from models.tipo_habitacion_model import TipoHabitacion

router = APIRouter()
tipo_habitacion_controller = TipoHabitacionController()

@router.post("/create_tipo_habitacion")
async def create_tipo_habitacion(tipo_habitacion: TipoHabitacion):
    rpta = tipo_habitacion_controller.create_tipo_habitacion(tipo_habitacion)
    return rpta

@router.get("/get_tipos_habitacion")
async def get_tipos_habitacion():
    rpta = tipo_habitacion_controller.get_tipos_habitacion()
    return rpta

@router.get("/get_tipo_habitacion/{id_thabitacion}")
async def get_tipo_habitacion_by_id(id_thabitacion: int):
    rpta = tipo_habitacion_controller.get_tipo_habitacion_by_id(id_thabitacion)
    return rpta