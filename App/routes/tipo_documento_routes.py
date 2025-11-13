from fastapi import APIRouter
from controllers.tipo_documento_controller import TipoDocumentoController
from models.tipo_documento_model import TipoDocumento

router = APIRouter()
tipo_doc_controller = TipoDocumentoController()

@router.post("/create_tipo_documento")
async def create_tipo_documento(tipo_documento: TipoDocumento):
    rpta = tipo_doc_controller.create_tipo_documento(tipo_documento)
    return rpta

@router.get("/get_tipos_documento")
async def get_tipos_documento():
    rpta = tipo_doc_controller.get_tipos_documento()
    return rpta

@router.get("/get_tipo_documento/{id_tdocumento}")
async def get_tipo_documento_by_id(id_tdocumento: int):
    rpta = tipo_doc_controller.get_tipo_documento_by_id(id_tdocumento)
    return rpta

@router.get("/combo")
async def tipos_documento_combo():
    rpta = tipo_doc_controller.get_tipos_documento_combo()
    return rpta