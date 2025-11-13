import mysql.connector
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from config.db_config import get_db_connection
from utils.timezone_utils import get_fecha_actual
from models.notificacion_model import Notificacion

class NotificacionController:

    def create_notificacion(self, notificacion: Notificacion):
        conn = None
        cursor = None

        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            fecha_actual = get_fecha_actual()
            query = """
                INSERT INTO notificacion (
                    id_usuario,
                    id_habitacion,
                    descripcion,
                    estado,
                    date_created,
                    date_updated
                ) VALUES (%s, %s, %s, %s, %s, %s)
            """
            values = (
                notificacion.id_usuario,
                notificacion.id_habitacion,
                notificacion.descripcion,
                notificacion.estado,
                fecha_actual,
                fecha_actual
            )
            cursor.execute(query, values)
            conn.commit()
            new_id = cursor.lastrowid

            return {
                "success": True,
                "message": "Notificación creada correctamente.",
                "id_notificacion": new_id
            }

        except mysql.connector.Error as err:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=f"Error al crear notificación: {err}")

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def get_notificaciones(self):
        conn = None
        cursor = None

        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM notificacion")
            data = cursor.fetchall()

            if not data:
                raise HTTPException(status_code=404, detail="No hay notificaciones registradas.")

            return {
                "success": True,
                "data": jsonable_encoder(data)
            }

        except mysql.connector.Error as err:
            raise HTTPException(status_code=500, detail=f"Error al obtener notificaciones: {err}")

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def get_notificacion_by_id(self, id_notificacion: int):
        conn = None
        cursor = None

        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT * FROM notificacion 
                WHERE id_notificacion = %s
            """, (id_notificacion,))
            data = cursor.fetchone()

            if not data:
                raise HTTPException(status_code=404, detail="Notificación no encontrada.")

            return {
                "success": True,
                "data": jsonable_encoder(data)
            }

        except mysql.connector.Error as err:
            raise HTTPException(status_code=500, detail=f"Error al obtener notificación: {err}")

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def get_notificaciones_por_usuario(self, id_usuario: int):
        conn = None
        cursor = None

        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            query = """
                SELECT *
                FROM notificacion
                WHERE id_usuario = %s
                ORDER BY date_created DESC
            """
            cursor.execute(query, (id_usuario,))
            data = cursor.fetchall()

            if not data:
                raise HTTPException(status_code=404, detail="No hay notificaciones para este usuario.")

            return {
                "success": True,
                "data": jsonable_encoder(data)
            }

        except mysql.connector.Error as err:
            raise HTTPException(status_code=500, detail=f"Error al obtener notificaciones: {err}")

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def create_notificacion_por_numero(self, id_usuario: int, numero_habitacion: str, descripcion: str, estado: int = 1):
        conn = None
        cursor = None

        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            fecha_actual = get_fecha_actual()

            cursor.execute("SELECT id_habitacion FROM habitacion WHERE numero = %s", (numero_habitacion,))
            habitacion = cursor.fetchone()

            if not habitacion:
                raise HTTPException(status_code=404, detail=f"Habitación con número {numero_habitacion} no encontrada.")

            id_habitacion = habitacion["id_habitacion"]

            query = """
                INSERT INTO notificacion (
                    id_usuario,
                    id_habitacion,
                    descripcion,
                    estado,
                    date_created,
                    date_updated
                ) VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (id_usuario, id_habitacion, descripcion, estado, fecha_actual, fecha_actual))
            conn.commit()
            new_id = cursor.lastrowid

            return {
                "success": True,
                "message": "Notificación creada correctamente.",
                "id_notificacion": new_id
            }

        except mysql.connector.Error as err:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=f"Error al crear notificación: {err}")

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
