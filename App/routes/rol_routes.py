from fastapi import APIRouter
from controllers.rol_controller import RolController
from models.rol_model import Rol

router = APIRouter()
rol_controller = RolController()

@router.post("/create_rol")
async def create_rol(rol: Rol):
    rpta = rol_controller.create_rol(rol)
    return rpta

@router.get("/get_roles")
async def get_roles():
    rpta = rol_controller.get_roles()
    return rpta

@router.get("/get_rol/{id_rol}")
async def get_rol_by_id(id_rol: int):
    rpta = rol_controller.get_rol_by_id(id_rol)
    return rpta

@router.get("/combo")
async def get_id_y_nombre_roles():
    rpta = rol_controller.get_id_y_nombre_roles()
    return rpta

@router.put("/desactivar/{id_rol}")
async def desactivar_rol(id_rol: int):
    rpta = rol_controller.desactivar_rol(id_rol)
    return rpta

@router.put("/activar/{id_rol}")
async def activar_rol(id_rol: int):
    rpta = rol_controller.activar_rol(id_rol)
    return rpta