import mysql.connector
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from datetime import datetime, timedelta
from config.db_config import get_db_connection
from utils.timezone_utils import get_fecha_actual
from models.reserva_model import Reserva

class ReservaController:

    def create_reserva(self, reserva: Reserva):
        conn = None
        cursor = None

        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            fecha_actual = get_fecha_actual()

            cursor.execute("""
                SELECT * FROM documento
                WHERE id_usuario = %s
            """, (reserva.id_usuario,))
            documento = cursor.fetchone()

            if not documento:
                raise HTTPException(status_code=400, detail="El usuario no tiene ningún documento registrado, no se puede crear la reserva.")

            query = """
                INSERT INTO reserva (
                    id_usuario,
                    date_start,
                    date_end,
                    estado,
                    date_created,
                    date_updated
                ) VALUES (%s, %s, %s, %s, %s, %s)
            """
            values = (
                reserva.id_usuario,
                reserva.date_start,
                reserva.date_end,
                reserva.estado,
                fecha_actual,
                fecha_actual
            )
            cursor.execute(query, values)
            conn.commit()
            new_id = cursor.lastrowid

            return {
                "success": True,
                "message": "Reserva creada correctamente.",
                "id_reserva": new_id
            }

        except mysql.connector.Error as err:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=f"Error al crear la reserva: {err}")

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def get_reservas(self):
        conn = None
        cursor = None

        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM reserva")
            data = cursor.fetchall()

            if not data:
                raise HTTPException(status_code=404, detail="No hay reservas registradas.")

            return {
                "success": True,
                "data": jsonable_encoder(data)
            }

        except mysql.connector.Error as err:
            raise HTTPException(status_code=500, detail=f"Error al obtener reservas: {err}")

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def get_reserva_by_id(self, id_reserva: int):
        conn = None
        cursor = None

        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT * FROM reserva
                WHERE id_reserva = %s
            """, (id_reserva,))
            data = cursor.fetchone()

            if not data:
                raise HTTPException(status_code=404, detail="Reserva no encontrada.")

            return {
                "success": True,
                "data": jsonable_encoder(data)
            }

        except mysql.connector.Error as err:
            raise HTTPException(status_code=500, detail=f"Error al obtener la reserva: {err}")

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def get_reservas_activas_por_usuario(self, id_usuario: int):
        conn = None
        cursor = None

        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            fecha_actual = get_fecha_actual()
            query = """
                SELECT *
                FROM reserva
                WHERE id_usuario = %s
                AND estado = 1
                AND (date_start > %s OR date_end > %s)
            """
            cursor.execute(query, (id_usuario, fecha_actual, fecha_actual))
            data = cursor.fetchall()

            if not data:
                raise HTTPException(status_code=404, detail="No hay reservas activas para este usuario.")

            return {
                "success": True,
                "data": jsonable_encoder(data)
            }

        except mysql.connector.Error as err:
            raise HTTPException(status_code=500, detail=f"Error al obtener reservas activas: {err}")

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def cancelar_reserva(self, id_reserva: int):
        conn = None
        cursor = None

        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            fecha_actual = get_fecha_actual().replace(tzinfo=None)

            # Obtener la reserva
            cursor.execute("SELECT * FROM reserva WHERE id_reserva = %s", (id_reserva,))
            reserva = cursor.fetchone()

            if not reserva:
                raise HTTPException(status_code=404, detail="Reserva no encontrada.")

            # Verificar si faltan más de 24 horas
            date_start = reserva["date_start"]

            if isinstance(date_start, str):
                # Manejo robusto del formato
                try:
                    date_start = datetime.strptime(date_start, "%Y-%m-%d %H:%M:%S")
                except ValueError:
                    try:
                        date_start = datetime.fromisoformat(date_start)
                    except Exception:
                        raise HTTPException(status_code=500, detail=f"Formato de fecha inválido: {date_start}")

            # Comparación correcta
            if date_start - fecha_actual < timedelta(hours=24):
                raise HTTPException(
                    status_code=400,
                    detail="No se puede cancelar la reserva, faltan menos de 24 horas para que comience."
                )

            # Cancelar reserva
            query = """
                UPDATE reserva
                SET estado = 0,
                    date_updated = %s
                WHERE id_reserva = %s
            """
            cursor.execute(query, (fecha_actual, id_reserva))
            conn.commit()

            return {
                "success": True,
                "message": f"Reserva con id {id_reserva} cancelada correctamente."
            }

        except mysql.connector.Error as err:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=f"Error al cancelar la reserva: {err}")

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def get_reservas_terminadas_usuario(self, id_usuario: int):
        conn = None
        cursor = None

        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)

            fecha_actual = get_fecha_actual()

            query = """
                SELECT *
                FROM reserva
                WHERE id_usuario = %s AND date_end < %s
                ORDER BY date_end DESC
            """

            cursor.execute(query, (id_usuario, fecha_actual))
            data = cursor.fetchall()

            if not data:
                return {
                    "success": True,
                    "data": [],
                    "message": "No hay reservas terminadas para este usuario."
                }

            return {
                "success": True,
                "data": jsonable_encoder(data)
            }

        except mysql.connector.Error as err:
            raise HTTPException(status_code=500, detail=f"Error al obtener reservas terminadas: {err}")

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def get_reserva_con_usuario(self, id_reserva: int):
        conn = None
        cursor = None

        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            query = """
                SELECT 
                    r.*,
                    CONCAT(u.primer_nombre, ' ', IFNULL(u.segundo_nombre, ''), ' ', u.primer_apellido, ' ', IFNULL(u.segundo_apellido, '')) AS nombre_completo
                FROM reserva r
                JOIN usuario u ON r.id_usuario = u.id_usuario
                WHERE r.id_reserva = %s
            """
            cursor.execute(query, (id_reserva,))
            data = cursor.fetchone()

            if not data:
                raise HTTPException(status_code=404, detail="Reserva no encontrada.")

            return {
                "success": True,
                "data": jsonable_encoder(data)
            }

        except mysql.connector.Error as err:
            raise HTTPException(status_code=500, detail=f"Error al obtener la reserva: {err}")

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def create_reserva_with_habitaciones(self, id_usuario: int, date_start: str, date_end: str, habitaciones: list, estado=1):
        conn = None
        cursor = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            fecha_actual = get_fecha_actual()

            # 1) validar que usuario tenga documento (tu lógica actual)
            cursor.execute("SELECT * FROM documento WHERE id_usuario = %s", (id_usuario,))
            documento = cursor.fetchone()
            if not documento:
                raise HTTPException(status_code=400, detail="El usuario no tiene ningún documento registrado, no se puede crear la reserva.")

            # 2) verificar disponibilidad previa para cada habitación (opcional pero recomendable)
            for id_h in habitaciones:
                cursor.execute("""
                    SELECT 1
                    FROM reserva_habitacion rh
                    JOIN reserva r ON rh.id_reserva = r.id_reserva
                    WHERE rh.id_habitacion = %s
                    AND r.estado != 0
                    AND (r.date_start < %s)
                    AND (r.date_end > %s)
                    LIMIT 1
                """, (id_h, date_end, date_start))
                clash = cursor.fetchone()
                if clash:
                    raise HTTPException(status_code=400, detail=f"Habitación {id_h} no disponible para las fechas solicitadas.")

            # 3) crear la reserva
            insert_reserva = """
                INSERT INTO reserva (id_usuario, date_start, date_end, estado, date_created, date_updated)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(insert_reserva, (id_usuario, date_start, date_end, estado, fecha_actual, fecha_actual))
            id_reserva = cursor.lastrowid

            # 4) insertar relaciones reserva_habitacion
            insert_rh = """
                INSERT INTO reserva_habitacion (id_reserva, id_habitacion, estado, date_created, date_updated)
                VALUES (%s, %s, %s, %s, %s)
            """
            for id_h in habitaciones:
                cursor.execute(insert_rh, (id_reserva, id_h, 1, fecha_actual, fecha_actual))

            conn.commit()
            return {"success": True, "message": "Reserva creada con habitaciones.", "id_reserva": id_reserva}

        except HTTPException:
            if conn:
                conn.rollback()
            raise
        except mysql.connector.Error as err:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=f"Error al crear reserva con habitaciones: {err}")
        finally:
            if cursor: cursor.close()
            if conn: conn.close()