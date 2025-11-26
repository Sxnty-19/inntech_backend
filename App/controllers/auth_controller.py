from fastapi import HTTPException, Depends
import mysql.connector
from config.db_config import get_db_connection
from utils.password_utils import hash_password, verify_password
from utils.jwt_utils import crear_token
from utils.timezone_utils import get_fecha_actual
from utils.mailer_utils import send_email

class AuthController:

    def register_user(self, usuario):
        conn = None
        cursor = None

        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)

            # Verificar correo único
            cursor.execute("SELECT id_usuario FROM usuario WHERE correo = %s", (usuario.correo,))
            if cursor.fetchone():
                raise HTTPException(status_code=400, detail="El correo ya está registrado")

            # Verificar username único
            cursor.execute("SELECT id_usuario FROM usuario WHERE username = %s", (usuario.username,))
            if cursor.fetchone():
                raise HTTPException(status_code=400, detail="El nombre de usuario ya está en uso")

            hashed_pw = hash_password(usuario.password)
            fecha_actual = get_fecha_actual()
            id_rol = 3  # Rol por defecto: Usuario
            cursor.execute(
                """
                INSERT INTO usuario (
                    id_rol, primer_nombre, segundo_nombre,
                    primer_apellido, segundo_apellido, telefono,
                    correo, username, password, estado,
                    date_created, date_updated
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    id_rol, usuario.primer_nombre, usuario.segundo_nombre,
                    usuario.primer_apellido, usuario.segundo_apellido, usuario.telefono,
                    usuario.correo, usuario.username, hashed_pw, usuario.estado, fecha_actual,
                    fecha_actual
                )
            )
            conn.commit()
            new_id = cursor.lastrowid

            html_mensaje = """
            <html>
            <body>
                <h1>Bienvenido a nuestra plataforma</h1>
                <p>Su cuenta ha sido creada exitosamente.</p>
                <p>¡Gracias por unirse a nosotros!</p>
            </body>
            </html>
            """

            send_email(destinatario = usuario.correo, asunto = "Bienvenido", mensaje = html_mensaje, html = True)

            return {
                "success": True, 
                "message": "Usuario registrado exitosamente",
                "id_usuario": new_id
            }

        except mysql.connector.Error as err:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=f"Error en la base de datos: {err}")

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def login(self, username: str, password: str):
        conn = None
        cursor = None

        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)

            # Buscar usuario por username
            cursor.execute(
                """
                SELECT u.*, r.nombre AS nombre_rol
                FROM usuario u
                INNER JOIN rol r ON u.id_rol = r.id_rol
                WHERE u.username = %s
                """,
                (username,)
            )
            user = cursor.fetchone()

            if not user:
                raise HTTPException(status_code=404, detail="Usuario no encontrado")

            if user.get("estado") != 1:
                raise HTTPException(status_code=403, detail="Cuenta suspendida o no encontrada; CONTACTE CON ADMINISTRACIÓN")

            if not verify_password(password, user["password"]):
                raise HTTPException(status_code=401, detail="Credenciales inválidas")

            # Crear payload para JWT
            payload = {
                "id_usuario": user["id_usuario"],
                "id_rol": user["id_rol"],
                "username": user["username"]
            }

            token = crear_token(payload)

            # Datos que no incluyen contraseña
            user_data = {
                "rol": user["nombre_rol"],
                "id_usuario": user["id_usuario"],
                "id_rol": user["id_rol"],
                "primer_nombre": user["primer_nombre"],
                "segundo_nombre": user["segundo_nombre"],
                "primer_apellido": user["primer_apellido"],
                "segundo_apellido": user["segundo_apellido"],
                "telefono": user["telefono"],
                "correo": user["correo"],
                "username": user["username"]
            }

            return {
                "success": True,
                "access_token": token,
                "token_type": "bearer",
                "user": user_data
            }

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()