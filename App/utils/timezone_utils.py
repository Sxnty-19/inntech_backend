from datetime import datetime
from dotenv import load_dotenv
import pytz
import os

load_dotenv()

def get_fecha_actual():
    timezone_name = os.getenv("TIMEZONE", "UTC")
    zona_horaria = pytz.timezone(timezone_name)
    return datetime.now(zona_horaria)

# Prueba...
if __name__ == "__main__":
    print("=== PRUEBA ===\n")

    print("\nCon TIMEZONE = America/Bogota:")
    print(get_fecha_actual())

    if "TIMEZONE" in os.environ:
        del os.environ["TIMEZONE"]
    print("\nSin TIMEZONE definida:")
    print(get_fecha_actual())

    fecha = get_fecha_actual()
    if isinstance(fecha, datetime):
        print("\nLa función retorna un objeto datetime correctamente.")
    else:
        print("\nLa función NO retorna un objeto datetime.")