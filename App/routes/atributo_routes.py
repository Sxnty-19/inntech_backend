from fastapi import APIRouter
from controllers.atributo_controller import AtributoController
from models.atributo_model import Atributo

router = APIRouter()
atributo_controller = AtributoController()

# Crear un nuevo atributo
@router.post("/create_atributo")
async def create_atributo(atributo: Atributo):
    rpta = atributo_controller.create_atributo(atributo)
    return rpta

# Obtener todos los atributos
@router.get("/get_atributos")
async def get_atributos():
    rpta = atributo_controller.get_atributos()
    return rpta

# Obtener atributo por ID
@router.get("/get_atributo/{id_atributo}")
async def get_atributo_by_id(id_atributo: int):
    rpta = atributo_controller.get_atributo_by_id(id_atributo)
    return rpta