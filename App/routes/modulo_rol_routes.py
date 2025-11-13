from fastapi import APIRouter
from controllers.modulo_rol_controller import ModuloRolController
from models.modulo_rol_model import ModuloRol

router = APIRouter()
modulorol_controller = ModuloRolController()

# Crear un nuevo módulo-rol
@router.post("/create_modulorol")
async def create_modulorol(modulorol: ModuloRol):
    rpta = modulorol_controller.create_modulorol(modulorol)
    return rpta

# Obtener todos los módulos-roles
@router.get("/get_modulos_roles")
async def get_modulos_roles():
    rpta = modulorol_controller.get_modulos_roles()
    return rpta

# Obtener módulo-rol por ID
@router.get("/get_modulorol/{id_mxr}")
async def get_modulorol_by_id(id_mxr: int):
    rpta = modulorol_controller.get_modulorol_by_id(id_mxr)
    return rpta