import mysql.connector
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from config.db_config import get_db_connection
from utils.timezone_utils import get_fecha_actual
from models.tipo_documento_model import TipoDocumento

class TipoDocumentoController:

    def create_tipo_documento(self, tipo_documento: TipoDocumento):
        conn = None
        cursor = None

        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            fecha_actual = get_fecha_actual()
            query = """
                INSERT INTO tipo_documento (
                    nombre,
                    descripcion,
                    estado,
                    date_created,
                    date_updated
                ) VALUES (%s, %s, %s, %s, %s)
            """
            values = (
                tipo_documento.nombre,
                tipo_documento.descripcion,
                tipo_documento.estado,
                fecha_actual,
                fecha_actual
            )
            cursor.execute(query, values)
            conn.commit()
            new_id = cursor.lastrowid

            return {
                "success": True,
                "message": "Tipo de documento creado correctamente.",
                "id_tdocumento": new_id
            }

        except mysql.connector.Error as err:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=f"Error al crear tipo de documento: {err}")

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def get_tipos_documento(self):
        conn = None
        cursor = None

        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM tipo_documento")
            data = cursor.fetchall()

            if not data:
                raise HTTPException(status_code=404, detail="No hay tipos de documento registrados.")

            return {
                "success": True,
                "data": jsonable_encoder(data)
            }

        except mysql.connector.Error as err:
            raise HTTPException(status_code=500, detail=f"Error al obtener tipos de documento: {err}")

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def get_tipo_documento_by_id(self, id_tdocumento: int):
        conn = None
        cursor = None

        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT * FROM tipo_documento
                WHERE id_tdocumento = %s
            """, (id_tdocumento,))
            data = cursor.fetchone()

            if not data:
                raise HTTPException(status_code=404, detail="Tipo de documento no encontrado.")

            return {
                "success": True,
                "data": jsonable_encoder(data)
            }

        except mysql.connector.Error as err:
            raise HTTPException(status_code=500, detail=f"Error al obtener tipo de documento: {err}")

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def get_tipos_documento_combo(self):
        conn = None
        cursor = None

        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT id_tdocumento, nombre FROM tipo_documento WHERE estado = 1")
            data = cursor.fetchall()
            
            if not data:
                raise HTTPException(status_code=404, detail="No hay tipos de documento activos.")

            return {
                "success": True,
                "data": jsonable_encoder(data)
            }

        except mysql.connector.Error as err:
            raise HTTPException(status_code=500, detail=f"Error al obtener tipos de documento: {err}")

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()