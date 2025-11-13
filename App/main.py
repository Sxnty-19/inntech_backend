from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Importación de rutas
from routes.auth_routes import router as auth_router

from routes.atributo_routes import router as atributo_router
from routes.documento_routes import router as documento_router
from routes.habitacion_routes import router as habitacion_router
from routes.modulo_rol_routes import router as modulo_rol_router
from routes.modulo_routes import router as modulo_router
from routes.notificacion_routes import router as notificacion_router
from routes.reserva_habitacion_routes import router as reserva_habitacion_router
from routes.reserva_routes import router as reserva_router
from routes.rol_routes import router as rol_router
from routes.tipo_documento_routes import router as tipo_documento_router
from routes.tipo_habitacion_routes import router as tipo_habitacion_router
from routes.usuario_atributo_routes import router as usuario_atributo_router
from routes.usuario_habitacion_routes import router as usuario_habitacion_router
from routes.usuario_routes import router as usuario_router

app = FastAPI(
    title="InnTech API",
    description="Backend desarrollado con FastAPI.",
    version="1.0.0"
)

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registro de rutas (módulos)
app.include_router(auth_router, prefix="/auth", tags=["Auth"])

app.include_router(atributo_router, prefix="/atributos", tags=["Atributos"])
app.include_router(documento_router, prefix="/documentos", tags=["Documentos"])
app.include_router(habitacion_router, prefix="/habitaciones", tags=["Habitaciones"])
app.include_router(modulo_rol_router, prefix="/modulos_roles", tags=["Módulos-Roles"])
app.include_router(modulo_router, prefix="/modulos", tags=["Módulos"])
app.include_router(notificacion_router, prefix="/notificaciones", tags=["Notificaciones"])
app.include_router(reserva_habitacion_router, prefix="/reservas_habitaciones", tags=["Reservas-Habitaciones"])
app.include_router(reserva_router, prefix="/reservas", tags=["Reservas"])
app.include_router(rol_router, prefix="/roles", tags=["Roles"])
app.include_router(tipo_documento_router, prefix="/tipos_documento", tags=["Tipos de Documento"])
app.include_router(tipo_habitacion_router, prefix="/tipos_habitacion", tags=["Tipos de Habitación"])
app.include_router(usuario_atributo_router, prefix="/usuarios_atributos", tags=["Usuarios-Atributos"])
app.include_router(usuario_habitacion_router, prefix="/usuarios_habitaciones", tags=["Usuarios-Habitaciones"])
app.include_router(usuario_router, prefix="/usuarios", tags=["Usuarios"])

# Endpoint raíz opcional
@app.get("/", tags=["Sistema"])
async def root():
    return {"message": "API en funcionamiento..."}