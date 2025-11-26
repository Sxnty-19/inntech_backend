from fastapi import APIRouter
from controllers.usuario_habitacion_controller import UsuarioHabitacionController
from models.usuario_habitacion_model import UsuarioHabitacion

router = APIRouter()
usuario_habitacion_controller = UsuarioHabitacionController()

# Crear una relación usuario-habitación
@router.post("/create_usuario_habitacion")
async def create_usuario_habitacion(usuario_habitacion: UsuarioHabitacion):
    rpta = usuario_habitacion_controller.create_usuario_habitacion(usuario_habitacion)
    return rpta

# Obtener todas las relaciones usuario-habitación
@router.get("/get_usuarios_habitacion")
async def get_usuarios_habitacion():
    rpta = usuario_habitacion_controller.get_usuarios_habitacion()
    return rpta

# Obtener una relación usuario-habitación por ID
@router.get("/get_usuario_habitacion/{id_uxh}")
async def get_usuario_habitacion_by_id(id_uxh: int):
    rpta = usuario_habitacion_controller.get_usuario_habitacion_by_id(id_uxh)
    return rpta

@router.post("/check_capacidad")
async def check_capacidad(payload: dict):
    id_reserva = payload.get("id_reserva")
    id_habitacion = payload.get("id_habitacion")
    capacidad_max = payload.get("capacidad_max")

    rpta = usuario_habitacion_controller.check_capacidad(id_reserva, id_habitacion, capacidad_max)
    return rpta

@router.post("/registrar_salida")
async def registrar_salida(payload: dict):
    id_reserva = payload.get("id_reserva")
    id_usuario = payload.get("id_usuario")

    if not id_reserva or not id_usuario:
        raise HTTPException(status_code=400, detail="Faltan parámetros requeridos.")

    rpta = usuario_habitacion_controller.registrar_salida(id_reserva, id_usuario)
    return rpta