from fastapi import APIRouter, Form, Depends
from models.usuario_model import Usuario
from controllers.auth_controller import AuthController
from utils.jwt_utils import verificar_token

router = APIRouter() #prefix="/auth", tags=["Auth"]
auth_controller = AuthController()

# Registro
@router.post("/register")
async def register(usuario: Usuario):
    rpta = auth_controller.register_user(usuario)
    return rpta

# Login
@router.post("/login")
async def login(username: str = Form(...), password: str = Form(...)):
    rpta =  auth_controller.login(username, password)
    return rpta