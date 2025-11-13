import mysql.connector
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from config.db_config import get_db_connection
from utils.timezone_utils import get_fecha_actual
from models.tipo_habitacion_model import TipoHabitacion

class TipoHabitacionController:

    def create_tipo_habitacion(self, tipo_habitacion: TipoHabitacion):
        conn = None
        cursor = None

        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            fecha_actual = get_fecha_actual()
            query = """
                INSERT INTO tipo_habitacion (
                    nombre,
                    descripcion,
                    capacidad_max,
                    estado,
                    date_created,
                    date_updated
                ) VALUES (%s, %s, %s, %s, %s, %s)
            """
            values = (
                tipo_habitacion.nombre,
                tipo_habitacion.descripcion,
                tipo_habitacion.capacidad_max,
                tipo_habitacion.estado,
                fecha_actual,
                fecha_actual
            )
            cursor.execute(query, values)
            conn.commit()
            new_id = cursor.lastrowid

            return {
                "success": True,
                "message": "Tipo de habitación creado correctamente.",
                "id_thabitacion": new_id
            }

        except mysql.connector.Error as err:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=f"Error al crear tipo de habitación: {err}")

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def get_tipos_habitacion(self):
        conn = None
        cursor = None

        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM tipo_habitacion")
            data = cursor.fetchall()

            if not data:
                raise HTTPException(status_code=404, detail="No hay tipos de habitación registrados.")

            return {
                "success": True,
                "data": jsonable_encoder(data)
            }

        except mysql.connector.Error as err:
            raise HTTPException(status_code=500, detail=f"Error al obtener tipos de habitación: {err}")

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def get_tipo_habitacion_by_id(self, id_thabitacion: int):
        conn = None
        cursor = None

        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT * FROM tipo_habitacion
                WHERE id_thabitacion = %s
            """, (id_thabitacion,))
            data = cursor.fetchone()

            if not data:
                raise HTTPException(status_code=404, detail="Tipo de habitación no encontrado.")

            return {
                "success": True,
                "data": jsonable_encoder(data)
            }

        except mysql.connector.Error as err:
            raise HTTPException(status_code=500, detail=f"Error al obtener tipo de habitación: {err}")

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()