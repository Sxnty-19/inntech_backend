import mysql.connector
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from config.db_config import get_db_connection
from utils.timezone_utils import get_fecha_actual
from models.rol_model import Rol

class RolController:

    def create_rol(self, rol: Rol):
        conn = None
        cursor = None

        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            fecha_actual = get_fecha_actual()
            query = """
                INSERT INTO rol (
                    nombre,
                    descripcion,
                    estado,
                    date_created,
                    date_updated
                ) VALUES (%s, %s, %s, %s, %s)
            """
            values = (
                rol.nombre,
                rol.descripcion,
                rol.estado,
                fecha_actual,
                fecha_actual
            )
            cursor.execute(query, values)
            conn.commit()
            new_id = cursor.lastrowid

            return {
                "success": True,
                "message": "Rol creado correctamente.",
                "id_rol": new_id
            }

        except mysql.connector.Error as err:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=f"Error al crear el rol: {err}")

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def get_roles(self):
        conn = None
        cursor = None

        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM rol")
            data = cursor.fetchall()

            if not data:
                raise HTTPException(status_code=404, detail="No hay roles registrados.")

            return {
                "success": True,
                "data": jsonable_encoder(data)
            }

        except mysql.connector.Error as err:
            raise HTTPException(status_code=500, detail=f"Error al obtener roles: {err}")

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def get_rol_by_id(self, id_rol: int):
        conn = None
        cursor = None

        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT * FROM rol
                WHERE id_rol = %s
            """, (id_rol,))
            data = cursor.fetchone()

            if not data:
                raise HTTPException(status_code=404, detail="Rol no encontrado.")

            return {
                "success": True,
                "data": jsonable_encoder(data)
            }

        except mysql.connector.Error as err:
            raise HTTPException(status_code=500, detail=f"Error al obtener el rol: {err}")

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def get_id_y_nombre_roles(self):
        conn = None
        cursor = None

        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)

            # Seleccionamos solo id_rol y nombre
            cursor.execute("SELECT id_rol, nombre FROM rol WHERE estado = 1 ORDER BY nombre")
            data = cursor.fetchall()

            if not data:
                raise HTTPException(status_code=404, detail="No hay roles activos.")

            return {
                "success": True,
                "data": jsonable_encoder(data)
            }

        except mysql.connector.Error as err:
            raise HTTPException(status_code=500, detail=f"Error al obtener roles: {err}")

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def desactivar_rol(self, id_rol: int):
        conn = None
        cursor = None

        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            fecha_actual = get_fecha_actual()
            query = """
                UPDATE rol
                SET estado = 0,
                    date_updated = %s
                WHERE id_rol = %s
            """
            cursor.execute(query, (fecha_actual, id_rol))
            conn.commit()

            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Rol no encontrado para desactivar.")

            return {
                "success": True,
                "message": f"Rol con id {id_rol} desactivado correctamente."
            }

        except mysql.connector.Error as err:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=f"Error al desactivar el rol: {err}")

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def activar_rol(self, id_rol: int):
        conn = None
        cursor = None

        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            fecha_actual = get_fecha_actual()
            query = """
                UPDATE rol
                SET estado = 1,
                    date_updated = %s
                WHERE id_rol = %s
            """
            cursor.execute(query, (fecha_actual, id_rol))
            conn.commit()

            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Rol no encontrado para activar.")

            return {
                "success": True,
                "message": f"Rol con id {id_rol} activado correctamente."
            }

        except mysql.connector.Error as err:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=f"Error al activar el rol: {err}")

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()