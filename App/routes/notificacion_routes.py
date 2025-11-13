from fastapi import APIRouter, Form
from controllers.notificacion_controller import NotificacionController
from models.notificacion_model import Notificacion

router = APIRouter()
notificacion_controller = NotificacionController()

@router.post("/create_notificacion")
async def create_notificacion(notificacion: Notificacion):
    rpta = notificacion_controller.create_notificacion(notificacion)
    return rpta

@router.get("/get_notificaciones")
async def get_notificaciones():
    rpta = notificacion_controller.get_notificaciones()
    return rpta

@router.get("/get_notificacion/{id_notificacion}")
async def get_notificacion_by_id(id_notificacion: int):
    rpta = notificacion_controller.get_notificacion_by_id(id_notificacion)
    return rpta

@router.get("/usuario/{id_usuario}")
async def notificaciones_usuario(id_usuario: int):
    rpta = notificacion_controller.get_notificaciones_por_usuario(id_usuario)
    return rpta

@router.post("/crear_por_numero")
async def crear_notificacion_por_numero(id_usuario: int = Form(...), numero_habitacion: str = Form(...), descripcion: str = Form(...), estado: int = Form(1)):
    rpta = notificacion_controller.create_notificacion_por_numero(id_usuario, numero_habitacion, descripcion, estado)
    return rpta