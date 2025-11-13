from fastapi import APIRouter, Form
from controllers.habitacion_controller import HabitacionController
from models.habitacion_model import Habitacion

router = APIRouter()
habitacion_controller = HabitacionController()

@router.post("/create_habitacion")
async def create_habitacion(habitacion: Habitacion):
    rpta = habitacion_controller.create_habitacion(habitacion)
    return rpta

@router.get("/get_habitaciones")
async def get_habitaciones():
    rpta = habitacion_controller.get_habitaciones()
    return rpta

@router.get("/get_habitacion/{id_habitacion}")
async def get_habitacion_by_id(id_habitacion: int):
    rpta = habitacion_controller.get_habitacion_by_id(id_habitacion)
    return rpta

@router.get("/numeros_estados")
async def numeros_estados():
    rpta = habitacion_controller.get_numeros_y_estados()
    return rpta

@router.put("/actualizar_estado")
async def actualizar_estado_habitacion( numero: str = Form(...), estado: int = Form(...)):
    rpta = habitacion_controller.actualizar_estado_por_numero(numero, estado)
    return rpta