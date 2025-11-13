from fastapi import APIRouter
from controllers.usuario_atributo_controller import UsuarioAtributoController
from models.usuario_atributo_model import UsuarioAtributo

router = APIRouter()
usuario_atributo_controller = UsuarioAtributoController()

# Crear una relación usuario-atributo
@router.post("/create_usuario_atributo")
async def create_usuario_atributo(usuario_atributo: UsuarioAtributo):
    rpta = usuario_atributo_controller.create_usuario_atributo(usuario_atributo)
    return rpta

# Obtener todas las relaciones usuario-atributo
@router.get("/get_usuarios_atributos")
async def get_usuarios_atributos():
    rpta = usuario_atributo_controller.get_usuarios_atributos()
    return rpta

# Obtener una relación usuario-atributo por ID
@router.get("/get_usuario_atributo/{id_uxa}")
async def get_usuario_atributo_by_id(id_uxa: int):
    rpta = usuario_atributo_controller.get_usuario_atributo_by_id(id_uxa)
    return rpta