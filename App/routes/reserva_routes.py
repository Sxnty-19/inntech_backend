from fastapi import APIRouter
from controllers.reserva_controller import ReservaController
from models.reserva_model import Reserva
from models.ReservaWithRooms_model import ReservaWithRooms

router = APIRouter()
reserva_controller = ReservaController()

@router.post("/create_reserva")
async def create_reserva(reserva: Reserva):
    rpta = reserva_controller.create_reserva(reserva)
    return rpta

@router.get("/get_reservas")
async def get_reservas():
    rpta = reserva_controller.get_reservas()
    return rpta

@router.get("/get_reserva/{id_reserva}")
async def get_reserva_by_id(id_reserva: int):
    rpta = reserva_controller.get_reserva_by_id(id_reserva)
    return rpta

@router.get("/activas/{id_usuario}")
async def reservas_activas_usuario(id_usuario: int):
    rpta = reserva_controller.get_reservas_activas_por_usuario(id_usuario)
    return rpta

@router.put("/cancelar/{id_reserva}")
async def cancelar_reserva(id_reserva: int):
    rpta = reserva_controller.cancelar_reserva(id_reserva)
    return rpta

@router.get("/terminadas")
async def reservas_terminadas():
    rpta = reserva_controller.get_reservas_terminadas()
    return rpta

@router.get("/get_reserva_completa/{id_reserva}")
async def get_reserva_completa(id_reserva: int):
    rpta = reserva_controller.get_reserva_con_usuario(id_reserva)
    return rpta

@router.post("/create_with_rooms")
async def create_reserva_with_rooms(payload: ReservaWithRooms):
    rpta = reserva_controller.create_reserva_with_habitaciones(
        payload.id_usuario,
        payload.date_start,
        payload.date_end,
        payload.habitaciones
    )
    return rpta