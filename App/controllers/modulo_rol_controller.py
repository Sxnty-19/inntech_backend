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

    def get_modulos_by_rol(self, id_rol: int):
        conn = None
        cursor = None

        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)

            query = """
                SELECT m.id_modulo, m.nombre, m.ruta
                FROM modulo_rol mr
                INNER JOIN modulo m ON mr.id_modulo = m.id_modulo
                WHERE mr.id_rol = %s AND mr.estado = 1
            """

            cursor.execute(query, (id_rol,))
            data = cursor.fetchall()

            # SOLUCIÓN: devolver lista vacía, NO ERROR
            return {
                "success": True,
                "data": jsonable_encoder(data)
            }

        except mysql.connector.Error as err:
            raise HTTPException(500, f"Error al obtener módulos del rol: {err}")

        finally:
            if cursor: cursor.close()
            if conn: conn.close()


    def get_modulos_by_rol(self, id_rol: int):
        conn = None
        cursor = None

        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)

            query = """
                SELECT m.id_modulo, m.nombre, m.ruta
                FROM modulo_rol mr
                INNER JOIN modulo m ON mr.id_modulo = m.id_modulo
                WHERE mr.id_rol = %s AND mr.estado = 1
            """

            cursor.execute(query, (id_rol,))
            data = cursor.fetchall()

            if not data:
                raise HTTPException(404, "Este rol no tiene módulos asignados.")

            return {
                "success": True,
                "data": jsonable_encoder(data)
            }

        except mysql.connector.Error as err:
            raise HTTPException(500, f"Error al obtener módulos del rol: {err}")

        finally:
            if cursor: cursor.close()
            if conn: conn.close()