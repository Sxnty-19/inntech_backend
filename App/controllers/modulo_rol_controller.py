import mysql.connector
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from config.db_config import get_db_connection
from utils.timezone_utils import get_fecha_actual
from models.modulo_rol_model import ModuloRol

class ModuloRolController:

    def create_modulorol(self, modulorol: ModuloRol):
        conn = None
        cursor = None

        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            fecha_actual = get_fecha_actual()
            query = """
                INSERT INTO modulo_rol (
                    id_modulo,
                    id_rol,
                    estado,
                    date_created,
                    date_updated
                ) VALUES (%s, %s, %s, %s, %s)
            """
            values = (
                modulorol.id_modulo,
                modulorol.id_rol,
                modulorol.estado,
                fecha_actual,
                fecha_actual
            )
            cursor.execute(query, values)
            conn.commit()
            new_id = cursor.lastrowid

            return {
                "success": True,
                "message": "Módulo-Rol creado correctamente.",
                "id_mxr": new_id
            }

        except mysql.connector.Error as err:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=f"Error al crear módulo-rol: {err}")

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def get_modulos_roles(self):
        conn = None
        cursor = None

        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM modulo_rol")
            data = cursor.fetchall()

            if not data:
                raise HTTPException(status_code=404, detail="No hay módulos-roles registrados.")

            return {
                "success": True,
                "data": jsonable_encoder(data)
            }

        except mysql.connector.Error as err:
            raise HTTPException(status_code=500, detail=f"Error al obtener módulos-roles: {err}")

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def get_modulorol_by_id(self, id_mxr: int):
        conn = None
        cursor = None

        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT * FROM modulo_rol 
                WHERE id_mxr = %s
            """, (id_mxr,))
            data = cursor.fetchone()

            if not data:
                raise HTTPException(status_code=404, detail="Módulo-Rol no encontrado.")

            return {
                "success": True,
                "data": jsonable_encoder(data)
            }

        except mysql.connector.Error as err:
            raise HTTPException(status_code=500, detail=f"Error al obtener módulo-rol: {err}")

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()