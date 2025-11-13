import mysql.connector
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from config.db_config import get_db_connection
from utils.timezone_utils import get_fecha_actual
from models.usuario_habitacion_model import UsuarioHabitacion

class UsuarioHabitacionController:

    def create_usuario_habitacion(self, usuario_habitacion: UsuarioHabitacion):
        conn = None
        cursor = None

        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            fecha_actual = get_fecha_actual()
            query = """
                INSERT INTO usuario_habitacion (
                    id_usuario,
                    id_habitacion,
                    id_reserva,
                    date_check_in,
                    date_check_out,
                    estado,
                    date_created,
                    date_updated
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            values = (
                usuario_habitacion.id_usuario,
                usuario_habitacion.id_habitacion,
                usuario_habitacion.id_reserva,
                usuario_habitacion.date_check_in,
                usuario_habitacion.date_check_out,
                usuario_habitacion.estado,
                fecha_actual,
                fecha_actual
            )
            cursor.execute(query, values)
            conn.commit()
            new_id = cursor.lastrowid

            return {
                "success": True,
                "message": "Usuario-Habitación creada correctamente.",
                "id_uxh": new_id
            }

        except mysql.connector.Error as err:
            if conn:
                conn.rollback()
            raise HTTPException(
                status_code=500,
                detail=f"Error al crear Usuario-Habitación: {err}"
            )

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def get_usuarios_habitacion(self):
        conn = None
        cursor = None

        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            query = """
                SELECT 
                    uh.*, 
                    u.primer_nombre, 
                    u.primer_apellido, 
                    h.numero AS numero_habitacion
                FROM usuario_habitacion uh
                JOIN usuario u ON uh.id_usuario = u.id_usuario
                JOIN habitacion h ON uh.id_habitacion = h.id_habitacion
            """
            cursor.execute(query)
            data = cursor.fetchall()

            if not data:
                raise HTTPException(status_code=404, detail="No hay asignaciones registradas.")

            return {
                "success": True,
                "data": jsonable_encoder(data)
            }

        except mysql.connector.Error as err:
            raise HTTPException(status_code=500, detail=f"Error al obtener Usuario-Habitación: {err}")

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def get_usuario_habitacion_by_id(self, id_uxh: int):
        conn = None
        cursor = None

        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            query = """
                SELECT 
                    uh.*, 
                    u.primer_nombre, 
                    u.primer_apellido, 
                    h.numero AS numero_habitacion
                FROM usuario_habitacion uh
                JOIN usuario u ON uh.id_usuario = u.id_usuario
                JOIN habitacion h ON uh.id_habitacion = h.id_habitacion
                WHERE uh.id_uxh = %s
            """
            cursor.execute(query, (id_uxh,))
            data = cursor.fetchone()

            if not data:
                raise HTTPException(status_code=404, detail="Registro no encontrado.")

            return {
                "success": True,
                "data": jsonable_encoder(data)
            }

        except mysql.connector.Error as err:
            raise HTTPException(status_code=500, detail=f"Error al obtener Usuario-Habitación: {err}")

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()