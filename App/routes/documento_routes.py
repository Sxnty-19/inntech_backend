from fastapi import APIRouter
from controllers.documento_controller import DocumentoController
from models.documento_model import Documento

router = APIRouter()
documento_controller = DocumentoController()

@router.post("/create_documento")
async def create_documento(documento: Documento):
    rpta = documento_controller.create_documento(documento)
    return rpta

@router.get("/get_documentos")
async def get_documentos():
    rpta = documento_controller.get_documentos()
    return rpta

@router.get("/get_documento/{id_documento}")
async def get_documento_by_id(id_documento: int):
    rpta = documento_controller.get_documento_by_id(id_documento)
    return rpta

@router.get("/get_documentos_completo")
async def get_documentos_con_usuario_y_tipo():
    rpta = documento_controller.get_documentos_con_usuario_y_tipo()
    return rpta

@router.get("/buscar_usuario_por_documento/{numero_documento}")
async def buscar_usuario_por_documento(numero_documento: str):
    rpta = documento_controller.buscar_usuario_por_documento(numero_documento)
    return rpta