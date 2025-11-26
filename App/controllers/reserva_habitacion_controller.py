import mysql.connector
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from config.db_config import get_db_connection
from utils.timezone_utils import get_fecha_actual
from models.reserva_habitacion_model import ReservaHabitacion

class ReservaHabitacionController:

    def create_reserva_habitacion(self, reserva_habitacion: ReservaHabitacion):
        conn = None
        cursor = None

        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            fecha_actual = get_fecha_actual()
            query = """
                INSERT INTO reserva_habitacion (
                    id_reserva,
                    id_habitacion,
                    estado,
                    date_created,
                    date_updated
                ) VALUES (%s, %s, %s, %s, %s)
            """
            values = (
                reserva_habitacion.id_reserva,
                reserva_habitacion.id_habitacion,
                reserva_habitacion.estado,
                fecha_actual,
                fecha_actual
            )
            cursor.execute(query, values)
            conn.commit()
            new_id = cursor.lastrowid

            return {
                "success": True,
                "message": "Reserva-Habitación creada correctamente.",
                "id_rxh": new_id
            }

        except mysql.connector.Error as err:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=f"Error al crear la relación reserva-habitación: {err}")

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def get_reservas_habitaciones(self):
        conn = None
        cursor = None

        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM reserva_habitacion")
            data = cursor.fetchall()

            if not data:
                raise HTTPException(status_code=404, detail="No hay relaciones reserva-habitación registradas.")

            return {
                "success": True,
                "data": jsonable_encoder(data)
            }

        except mysql.connector.Error as err:
            raise HTTPException(status_code=500, detail=f"Error al obtener las relaciones reserva-habitación: {err}")

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def get_reserva_habitacion_by_id(self, id_rxh: int):
        conn = None
        cursor = None

        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT * FROM reserva_habitacion
                WHERE id_rxh = %s
            """, (id_rxh,))
            data = cursor.fetchone()

            if not data:
                raise HTTPException(status_code=404, detail="Relación reserva-habitación no encontrada.")

            return {
                "success": True,
                "data": jsonable_encoder(data)
            }

        except mysql.connector.Error as err:
            raise HTTPException(status_code=500, detail=f"Error al obtener la relación reserva-habitación: {err}")

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def get_habitaciones_by_reserva(self, id_reserva: int):
        conn = None
        cursor = None

        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)

            query = """
                SELECT 
                    h.id_habitacion,
                    h.numero,
                    h.estado,
                    h.limpieza,
                    h.id_thabitacion,
                    t.capacidad_max
                FROM reserva_habitacion rxh
                INNER JOIN habitacion h ON rxh.id_habitacion = h.id_habitacion
                INNER JOIN tipo_habitacion t ON h.id_thabitacion = t.id_thabitacion
                WHERE rxh.id_reserva = %s
            """

            cursor.execute(query, (id_reserva,))
            data = cursor.fetchall()

            return {
                "success": True,
                "habitaciones": data
            }

        except mysql.connector.Error as err:
            raise HTTPException(
                status_code=500,
                detail=f"Error al obtener habitaciones: {err}"
            )

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()