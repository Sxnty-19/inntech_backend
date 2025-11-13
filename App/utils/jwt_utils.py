from fastapi import HTTPException, Request, Depends
from fastapi.security import OAuth2PasswordBearer
from config.db_config import get_db_connection
import jwt
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def crear_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire, "iat": datetime.utcnow()})
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return token

def verificar_token(token: str = Depends(oauth2_scheme)) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expirado. Inicia sesión nuevamente.")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token inválido.")


def verificar_acceso_modulo_auto(payload: dict = Depends(verificar_token), request: Request = None):
    id_rol = payload.get("id_rol")
    ruta_actual = request.url.path

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id_modulo FROM modulo WHERE ruta = %s", (ruta_actual,))
    modulo = cursor.fetchone()

    if not modulo:
        raise HTTPException(status_code=404, detail=f"No existe módulo para la ruta {ruta_actual}")

    id_modulo = modulo["id_modulo"]

    # Validar permisos
    cursor.execute(
        "SELECT * FROM modulo_rol WHERE id_rol = %s AND id_modulo = %s",
        (id_rol, id_modulo)
    )
    permiso = cursor.fetchone()

    if not permiso:
        raise HTTPException(status_code=403, detail="No tienes permiso para acceder a este módulo.")

    cursor.close()
    conn.close()

    return payload