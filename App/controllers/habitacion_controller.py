import mysql.connector
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from config.db_config import get_db_connection
from utils.timezone_utils import get_fecha_actual
from models.habitacion_model import Habitacion

class HabitacionController:

    def create_habitacion(self, habitacion: Habitacion):
        conn = None
        cursor = None

        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            fecha_actual = get_fecha_actual()
            query = """
                INSERT INTO habitacion (
                    id_thabitacion,
                    numero,
                    estado,
                    date_created,
                    date_updated
                ) VALUES (%s, %s, %s, %s, %s)
            """
            values = (
                habitacion.id_thabitacion,
                habitacion.numero,
                habitacion.estado,
                fecha_actual,
                fecha_actual
            )
            cursor.execute(query, values)
            conn.commit()
            new_id = cursor.lastrowid

            return {
                "success": True,
                "message": "Habitación creada correctamente.",
                "id_habitacion": new_id
            }

        except mysql.connector.Error as err:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=f"Error al crear habitación: {err}")

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def get_habitaciones(self):
        conn = None
        cursor = None

        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM habitacion")
            data = cursor.fetchall()

            if not data:
                raise HTTPException(status_code=404, detail="No hay habitaciones registradas.")

            return {
                "success": True,
                "data": jsonable_encoder(data)
            }

        except mysql.connector.Error as err:
            raise HTTPException(status_code=500, detail=f"Error al obtener habitaciones: {err}")

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def get_habitacion_by_id(self, id_habitacion: int):
        conn = None
        cursor = None

        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT * FROM habitacion 
                WHERE id_habitacion = %s
            """, (id_habitacion,))
            data = cursor.fetchone()

            if not data:
                raise HTTPException(status_code=404, detail="Habitación no encontrada.")

            return {
                "success": True,
                "data": jsonable_encoder(data)
            }

        except mysql.connector.Error as err:
            raise HTTPException(status_code=500, detail=f"Error al obtener habitación: {err}")

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def get_numeros_y_estados(self):
        conn = None
        cursor = None

        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)

            cursor.execute("SELECT numero, estado FROM habitacion ORDER BY numero")
            data = cursor.fetchall()

            if not data:
                raise HTTPException(status_code=404, detail="No hay habitaciones registradas.")

            return {
                "success": True,
                "data": jsonable_encoder(data)
            }

        except mysql.connector.Error as err:
            raise HTTPException(status_code=500, detail=f"Error al obtener habitaciones: {err}")

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def actualizar_estado_por_numero(self, numero: str, estado: int):
        conn = None
        cursor = None

        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            fecha_actual = get_fecha_actual()

            cursor.execute("SELECT id_habitacion FROM habitacion WHERE numero = %s", (numero,))
            habitacion = cursor.fetchone()

            if not habitacion:
                raise HTTPException(status_code=404, detail=f"Habitación con número {numero} no encontrada.")

            id_habitacion = habitacion["id_habitacion"]

            query = """
                UPDATE habitacion
                SET estado = %s,
                    date_updated = %s
                WHERE id_habitacion = %s
            """
            cursor.execute(query, (estado, fecha_actual, id_habitacion))
            conn.commit()

            return {
                "success": True,
                "message": f"Estado de la habitación {numero} actualizado correctamente a {estado}."
            }

        except mysql.connector.Error as err:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=f"Error al actualizar habitación: {err}")

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()