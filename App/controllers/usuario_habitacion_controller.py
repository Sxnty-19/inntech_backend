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

    def check_capacidad(self, id_reserva: int, id_habitacion: int, capacidad_max: int):
        conn = None
        cursor = None

        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)

            # Contar usuarios asignados a la habitación en esa reserva
            query = """
                SELECT COUNT(*) AS ocupados
                FROM usuario_habitacion
                WHERE id_reserva = %s
                AND id_habitacion = %s
                AND estado = 1
            """

            cursor.execute(query, (id_reserva, id_habitacion))
            result = cursor.fetchone()

            ocupados = result["ocupados"] if result else 0

            disponible = ocupados < capacidad_max

            return {
                "success": True,
                "disponible": disponible,
                "ocupados": ocupados,
                "capacidad": capacidad_max,
                "message": "Habitación disponible" if disponible else "Habitación llena"
            }

        except mysql.connector.Error as err:
            raise HTTPException(
                status_code=500,
                detail=f"Error al validar capacidad: {err}"
            )

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def registrar_salida(self, id_reserva: int, id_usuario: int):
        conn = None
        cursor = None

        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            fecha_actual = get_fecha_actual()

            # Verificar si existe un registro activo (estado = 1)
            select_query = """
                SELECT id_uxh
                FROM usuario_habitacion
                WHERE id_reserva = %s
                AND id_usuario = %s
                AND estado = 1
                LIMIT 1
            """
            cursor.execute(select_query, (id_reserva, id_usuario))
            data = cursor.fetchone()

            if not data:
                raise HTTPException(
                    status_code=404,
                    detail="No se encontró un registro activo para este usuario en esta reserva."
                )

            id_uxh = data[0]

            # Actualizar estado y fecha de salida
            update_query = """
                UPDATE usuario_habitacion
                SET estado = 0,
                    date_check_out = %s,
                    date_updated = %s
                WHERE id_uxh = %s
            """
            cursor.execute(update_query, (fecha_actual, fecha_actual, id_uxh))
            conn.commit()

            return {
                "success": True,
                "message": "Salida registrada exitosamente.",
                "id_uxh": id_uxh
            }

        except mysql.connector.Error as err:
            if conn:
                conn.rollback()

            raise HTTPException(
                status_code=500,
                detail=f"Error al registrar salida: {err}"
            )

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()