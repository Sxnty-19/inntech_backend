import mysql.connector
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from config.db_config import get_db_connection
from utils.timezone_utils import get_fecha_actual
from models.documento_model import Documento

class DocumentoController:

    def create_documento(self, documento: Documento):
        conn = None
        cursor = None

        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            fecha_actual = get_fecha_actual()
            query = """
                INSERT INTO documento (
                    id_tdocumento, 
                    id_usuario, 
                    numero_documento, 
                    lugar_expedicion, 
                    estado, 
                    date_created, 
                    date_updated
                ) VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            values = (
                documento.id_tdocumento,
                documento.id_usuario,
                documento.numero_documento,
                documento.lugar_expedicion,
                documento.estado,
                fecha_actual,
                fecha_actual
            )
            cursor.execute(query, values)
            conn.commit()
            new_id = cursor.lastrowid

            return {
                "success": True,
                "message": "Documento creado correctamente.",
                "id_documento": new_id
            }

        except mysql.connector.Error as err:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=f"Error al crear documento: {err}")

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def get_documentos(self):
        conn = None
        cursor = None

        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM documento")
            data = cursor.fetchall()

            if not data:
                raise HTTPException(status_code=404, detail="No hay documentos registrados.")

            return {
                "success": True,
                "data": jsonable_encoder(data)
            }

        except mysql.connector.Error as err:
            raise HTTPException(status_code=500, detail=f"Error al obtener documentos: {err}")

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def get_documento_by_id(self, id_documento: int):
        conn = None
        cursor = None

        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT * FROM documento 
                WHERE id_documento = %s
            """, (id_documento,))
            data = cursor.fetchone()

            if not data:
                raise HTTPException(status_code=404, detail="Documento no encontrado.")

            return {
                "success": True,
                "data": jsonable_encoder(data)
            }

        except mysql.connector.Error as err:
            raise HTTPException(status_code=500, detail=f"Error al obtener documento: {err}")

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def get_documentos_con_usuario_y_tipo(self):
        conn = None
        cursor = None

        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)

            query = """
                SELECT 
                    d.id_documento,
                    d.id_tdocumento,
                    td.nombre AS tipo_documento,
                    d.numero_documento,
                    d.lugar_expedicion,
                    d.estado,
                    d.date_created,
                    d.date_updated,
                    u.id_usuario,
                    CONCAT(u.primer_nombre, ' ',
                        IFNULL(u.segundo_nombre, ''), ' ',
                        u.primer_apellido, ' ',
                        IFNULL(u.segundo_apellido, '')) AS nombre_completo
                FROM documento d
                JOIN usuario u ON d.id_usuario = u.id_usuario
                JOIN tipo_documento td ON d.id_tdocumento = td.id_tdocumento
            """
            cursor.execute(query)
            data = cursor.fetchall()

            if not data:
                raise HTTPException(status_code=404, detail="No hay documentos registrados.")

            return {
                "success": True,
                "data": jsonable_encoder(data)
            }

        except mysql.connector.Error as err:
            raise HTTPException(status_code=500, detail=f"Error al obtener documentos: {err}")

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def buscar_usuario_por_documento(self, numero_documento: str):
        conn = None
        cursor = None

        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)

            query = """
                SELECT 
                    d.id_documento,
                    d.numero_documento,
                    u.id_usuario,
                    CONCAT(
                        u.primer_nombre, ' ',
                        IFNULL(u.segundo_nombre, ''), ' ',
                        u.primer_apellido, ' ',
                        IFNULL(u.segundo_apellido, '')
                    ) AS nombre_completo
                FROM documento d
                INNER JOIN usuario u ON d.id_usuario = u.id_usuario
                WHERE d.numero_documento = %s
                LIMIT 1
            """

            cursor.execute(query, (numero_documento,))
            data = cursor.fetchone()

            if not data:
                raise HTTPException(
                    status_code=404,
                    detail="No se encontró ningún usuario con ese número de documento."
                )

            return {
                "success": True,
                "message": "Usuario encontrado.",
                "data": jsonable_encoder(data)
            }

        except mysql.connector.Error as err:
            raise HTTPException(status_code=500, detail=f"Error al buscar usuario: {err}")

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()