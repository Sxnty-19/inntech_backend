import mysql.connector
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from config.db_config import get_db_connection
from utils.timezone_utils import get_fecha_actual
from models.usuario_atributo_model import UsuarioAtributo

class UsuarioAtributoController:

    def create_usuario_atributo(self, usuario_atributo: UsuarioAtributo):
        conn = None
        cursor = None

        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            fecha_actual = get_fecha_actual()
            query = """
                INSERT INTO usuario_atributo (
                    id_usuario,
                    id_atributo,
                    valor,
                    estado,
                    date_created,
                    date_updated
                ) VALUES (%s, %s, %s, %s, %s, %s)
            """
            values = (
                usuario_atributo.id_usuario,
                usuario_atributo.id_atributo,
                usuario_atributo.valor,
                usuario_atributo.estado,
                fecha_actual,
                fecha_actual
            )
            cursor.execute(query, values)
            conn.commit()
            new_id = cursor.lastrowid

            return {
                "success": True,
                "message": "Atributo asignado al usuario correctamente.",
                "id_uxa": new_id
            }

        except mysql.connector.Error as err:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=f"Error al asignar atributo al usuario: {err}")

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def get_usuarios_atributos(self):
        conn = None
        cursor = None

        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM usuario_atributo")
            data = cursor.fetchall()

            if not data:
                raise HTTPException(status_code=404, detail="No hay relaciones usuario-atributo registradas.")

            return {
                "success": True,
                "data": jsonable_encoder(data)
            }

        except mysql.connector.Error as err:
            raise HTTPException(status_code=500, detail=f"Error al obtener relaciones usuario-atributo: {err}")

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def get_usuario_atributo_by_id(self, id_uxa: int):
        conn = None
        cursor = None

        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT * FROM usuario_atributo
                WHERE id_uxa = %s
            """, (id_uxa,))
            data = cursor.fetchone()

            if not data:
                raise HTTPException(status_code=404, detail="Relación usuario-atributo no encontrada.")

            return {
                "success": True,
                "data": jsonable_encoder(data)
            }

        except mysql.connector.Error as err:
            raise HTTPException(status_code=500, detail=f"Error al obtener relación usuario-atributo: {err}")

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()