import requests
import threading
from dotenv import load_dotenv
import os

load_dotenv()

def _send_email_task(payload):
    try:
        requests.post(
            os.getenv("MAILER_SERVICE_URL"),
            json=payload,
            timeout=5
        )
    except Exception as e:
        print(f"[AVISO] No se pudo enviar correo: {e}")

def send_email(destinatario, asunto, mensaje, html=False):
    payload = {
        "remitente": os.getenv("MAILER_SENDER_ADDRESS"),
        "destinatario": destinatario,
        "asunto": asunto,
        "mensaje": mensaje,
        "es_html": html
    }
    
    print(f"[INFO] Enviando correo a {destinatario} en segundo plano...")
    threading.Thread(target=_send_email_task, args=(payload,), daemon=True).start()
    return True

""" from utils.mailer_utils import send_email - send_email("cliente@example.com", "Asunto de prueba", "Mensaje de prueba") """