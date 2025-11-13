from fastapi import APIRouter
from controllers.usuario_controller import UsuarioController
from models.usuario_model import Usuario

router = APIRouter()
usuario_controller = UsuarioController()

@router.post("/create_usuario")
async def create_usuario(usuario: Usuario):
    rpta = usuario_controller.create_usuario(usuario)
    return rpta

@router.get("/get_usuarios")
async def get_usuarios():
    rpta = usuario_controller.get_usuarios()
    return rpta

@router.get("/get_usuario/{id_usuario}")
async def get_usuario_by_id(id_usuario: int):
    rpta = usuario_controller.get_usuario_by_id(id_usuario)
    return rpta

@router.put("/update_usuario/{id_usuario}")
async def actualizar_usuario(id_usuario: int, usuario: Usuario):
    rpta =  usuario_controller.update_usuario(id_usuario, usuario)
    return rpta

@router.put("/desactivar/{id_usuario}")
async def desactivar_usuario(id_usuario: int):
    rpta = usuario_controller.desactivar_usuario(id_usuario)
    return rpta

@router.put("/activar/{id_usuario}")
async def activar_usuario(id_usuario: int):
    rpta = usuario_controller.activar_usuario(id_usuario)
    return rpta

@router.put("/cambiar-rol/{id_usuario}/{id_rol}")
async def cambiar_rol(id_usuario: int, id_rol: int):
    rpta = usuario_controller.cambiar_rol_usuario(id_usuario, id_rol)
    return rpta