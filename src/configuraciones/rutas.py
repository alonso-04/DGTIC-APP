import os
import sys
from userpaths import get_my_documents


def obtener_ruta_base():
    if getattr(sys, "frozen", False):
        return sys._MEIPASS
    else:
        return os.path.abspath(os.path.dirname(__file__))

RUTA_BASE = obtener_ruta_base()

def obtener_ruta_sesion_json() -> str:
    ruta_absoluta_sesion_json = os.path.join(
        "sesion_usuario.json"
    )
    
    ruta_final_sesion_json = os.path.join(RUTA_BASE, ruta_absoluta_sesion_json)
    return ruta_final_sesion_json

def obtener_ruta_reportes() -> str:
    ruta_documentos = get_my_documents()
    ruta_reportes = os.path.join(ruta_documentos, "REPORTES_SERVICIOS")
    
    try:
        os.makedirs(ruta_reportes, exist_ok = True)
        return ruta_reportes
    except OSError:
        return None

def obtener_ruta_respaldos_bd() -> str:
    ruta_documentos = get_my_documents()
    ruta_respaldos = os.path.join(ruta_documentos, "RESPALDOS_BD")
    
    try:
        os.makedirs(ruta_respaldos, exist_ok = True)
        return ruta_respaldos
    except OSError:
        return None


if __name__ == "__main__":
    try:
        directorio_reportes = obtener_ruta_reportes()
        directorio_respaldos = obtener_ruta_respaldos_bd()
        
        if (directorio_reportes):
            print(f"El directorio se creó correctamente. La ruta es: {directorio_reportes}")
        
        if (directorio_respaldos):
            print(f"El directorio se creó correctamente para los respaldos en: {directorio_respaldos}")
    except OSError as error:
        print(f"ERROR AL CREAR LA CARPETA: {error}")
    except Exception as error:
        print(error)