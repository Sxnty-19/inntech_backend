import mysql.connector
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from config.db_config import get_db_connection
from utils.timezone_utils import get_fecha_actual
from models.usuario_model import Usuario

class UsuarioController:

    def create_usuario(self, usuario: Usuario):
        conn = None
        cursor = None

        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            fecha_actual = get_fecha_actual()
            query = """
                INSERT INTO usuario (
                    id_rol,
                    primer_nombre,
                    segundo_nombre,
                    primer_apellido,
                    segundo_apellido,
                    telefono,
                    correo,
                    username,
                    password,
                    estado,
                    date_created,
                    date_updated
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            values = (
                usuario.id_rol,
                usuario.primer_nombre,
                usuario.segundo_nombre,
                usuario.primer_apellido,
                usuario.segundo_apellido,
                usuario.telefono,
                usuario.correo,
                usuario.username,
                usuario.password,
                usuario.estado,
                fecha_actual,
                fecha_actual
            )
            cursor.execute(query, values)
            conn.commit()
            new_id = cursor.lastrowid

            return {
                "success": True,
                "message": "Usuario creado correctamente.",
                "id_usuario": new_id
            }

        except mysql.connector.Error as err:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=f"Error al crear usuario: {err}")

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def get_usuarios(self):
        conn = None
        cursor = None

        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT 
                    u.*, 
                    r.nombre AS nombre_rol
                FROM usuario u
                JOIN rol r ON u.id_rol = r.id_rol
            """)
            data = cursor.fetchall()

            if not data:
                raise HTTPException(status_code=404, detail="No hay usuarios registrados.")

            return {
                "success": True,
                "data": jsonable_encoder(data)
            }

        except mysql.connector.Error as err:
            raise HTTPException(status_code=500, detail=f"Error al obtener usuarios: {err}")

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def get_usuario_by_id(self, id_usuario: int):
        conn = None
        cursor = None

        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT 
                    u.*, 
                    r.nombre AS nombre_rol
                FROM usuario u
                JOIN rol r ON u.id_rol = r.id_rol
                WHERE u.id_usuario = %s
            """, (id_usuario,))
            data = cursor.fetchone()

            if not data:
                raise HTTPException(status_code=404, detail="Usuario no encontrado.")

            return {
                "success": True,
                "data": jsonable_encoder(data)
            }

        except mysql.connector.Error as err:
            raise HTTPException(status_code=500, detail=f"Error al obtener usuario: {err}")

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def update_usuario(self, id_usuario: int, usuario: Usuario):
        conn = None
        cursor = None

        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            fecha_actual = get_fecha_actual()

            # Solo actualizamos los campos permitidos
            query = """
                UPDATE usuario
                SET
                    primer_nombre = %s,
                    segundo_nombre = %s,
                    primer_apellido = %s,
                    segundo_apellido = %s,
                    telefono = %s,
                    date_updated = %s
                WHERE id_usuario = %s
            """
            values = (
                usuario.primer_nombre,
                usuario.segundo_nombre,
                usuario.primer_apellido,
                usuario.segundo_apellido,
                usuario.telefono,
                fecha_actual,
                id_usuario
            )

            cursor.execute(query, values)
            conn.commit()

            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Usuario no encontrado para actualizar.")

            return {
                "success": True,
                "message": "Usuario actualizado correctamente."
            }

        except mysql.connector.Error as err:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=f"Error al actualizar usuario: {err}")

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def desactivar_usuario(self, id_usuario: int):
        conn = None
        cursor = None

        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            fecha_actual = get_fecha_actual()

            query = """
                UPDATE usuario
                SET estado = 0,
                    date_updated = %s
                WHERE id_usuario = %s
            """
            cursor.execute(query, (fecha_actual, id_usuario))
            conn.commit()

            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Usuario no encontrado para desactivar.")

            return {
                "success": True,
                "message": f"Usuario con id {id_usuario} desactivado correctamente."
            }

        except mysql.connector.Error as err:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=f"Error al desactivar usuario: {err}")

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def activar_usuario(self, id_usuario: int):
        conn = None
        cursor = None

        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            fecha_actual = get_fecha_actual()
            query = """
                UPDATE usuario
                SET estado = 1,
                    date_updated = %s
                WHERE id_usuario = %s
            """
            cursor.execute(query, (fecha_actual, id_usuario))
            conn.commit()

            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Usuario no encontrado para activar.")

            return {
                "success": True,
                "message": f"Usuario con id {id_usuario} activado correctamente."
            }

        except mysql.connector.Error as err:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=f"Error al activar usuario: {err}")

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def cambiar_rol_usuario(self, id_usuario: int, id_rol: int):
        conn = None
        cursor = None

        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            fecha_actual = get_fecha_actual()

            query = """
                UPDATE usuario
                SET id_rol = %s,
                    date_updated = %s
                WHERE id_usuario = %s
            """
            values = (id_rol, fecha_actual, id_usuario)
            cursor.execute(query, values)
            conn.commit()

            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Usuario no encontrado para cambiar de rol.")

            return {
                "success": True,
                "message": f"Rol del usuario con id {id_usuario} actualizado correctamente."
            }

        except mysql.connector.Error as err:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=f"Error al cambiar el rol del usuario: {err}")

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()