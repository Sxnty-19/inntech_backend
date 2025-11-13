from fastapi import APIRouter
from controllers.modulo_controller import ModuloController
from models.modulo_model import Modulo

router = APIRouter()
modulo_controller = ModuloController()

# Crear un nuevo módulo
@router.post("/create_modulo")
async def create_modulo(modulo: Modulo):
    rpta = modulo_controller.create_modulo(modulo)
    return rpta

# Obtener todos los módulos
@router.get("/get_modulos")
async def get_modulos():
    rpta = modulo_controller.get_modulos()
    return rpta

# Obtener módulo por ID
@router.get("/get_modulo/{id_modulo}")
async def get_modulo_by_id(id_modulo: int):
    rpta = modulo_controller.get_modulo_by_id(id_modulo)
    return rpta