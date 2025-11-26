from fastapi import APIRouter
from controllers.reserva_habitacion_controller import ReservaHabitacionController
from models.reserva_habitacion_model import ReservaHabitacion

router = APIRouter()
reserva_habitacion_controller = ReservaHabitacionController()

@router.post("/create_reserva_habitacion")
async def create_reserva_habitacion(reserva_habitacion: ReservaHabitacion):
    rpta = reserva_habitacion_controller.create_reserva_habitacion(reserva_habitacion)
    return rpta

@router.get("/get_reservas_habitaciones")
async def get_reservas_habitaciones():
    rpta = reserva_habitacion_controller.get_reservas_habitaciones()
    return rpta

@router.get("/get_reserva_habitacion/{id_rxh}")
async def get_reserva_habitacion_by_id(id_rxh: int):
    rpta = reserva_habitacion_controller.get_reserva_habitacion_by_id(id_rxh)
    return rpta

@router.get("/get_habitaciones_by_reserva/{id_reserva}")
async def get_habitaciones_by_reserva(id_reserva: int):
    rpta = reserva_habitacion_controller.get_habitaciones_by_reserva(id_reserva)
    return rpta