import mysql.connector
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from config.db_config import get_db_connection
from utils.timezone_utils import get_fecha_actual
from models.atributo_model import Atributo

class AtributoController:

    def create_atributo(self, atributo: Atributo):
        conn = None
        cursor = None

        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            fecha_actual = get_fecha_actual()
            query = """
                INSERT INTO atributo (
                    nombre, 
                    descripcion, 
                    estado, 
                    date_created, 
                    date_updated
                ) VALUES (%s, %s, %s, %s, %s)
            """
            values = (
                atributo.nombre,
                atributo.descripcion,
                atributo.estado,
                fecha_actual,
                fecha_actual
            )
            cursor.execute(query, values)
            conn.commit()
            new_id = cursor.lastrowid

            return {
                "success": True,
                "message": "Atributo creado correctamente.",
                "id_atributo": new_id
            }
        
        except mysql.connector.Error as err:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=f"Error al crear atributo: {err}")
        
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def get_atributos(self):
        conn = None
        cursor = None

        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM atributo")
            data = cursor.fetchall()

            if not data:
                raise HTTPException(status_code=404, detail="No hay atributos registrados.")
            
            return {
                "success": True, 
                "data": jsonable_encoder(data)
            }

        except mysql.connector.Error as err:
            raise HTTPException(status_code=500, detail=f"Error al obtener atributos: {err}")
        
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def get_atributo_by_id(self, id_atributo: int):
        conn = None
        cursor = None

        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT * FROM atributo 
                WHERE id_atributo = %s
            """, (id_atributo,))
            data = cursor.fetchone()

            if not data:
                raise HTTPException(status_code=404, detail="Atributo no encontrado.")

            return {
                "success": True, 
                "data": jsonable_encoder(data)
            }

        except mysql.connector.Error as err:
            raise HTTPException(status_code=500, detail=f"Error al obtener atributo: {err}")

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()