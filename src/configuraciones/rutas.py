import os
import sys
import shutil
import platform
import subprocess
from userpaths import get_my_documents
from utilidades.tipos_reporte import TiposReporte


def obtener_ruta_base():
    if getattr(sys, "frozen", False):
        return sys._MEIPASS
    else:
        carpeta_configuraciones = os.path.abspath(os.path.dirname(__file__))
        raiz_proyecto = os.path.abspath(os.path.join(carpeta_configuraciones, ".."))
        return raiz_proyecto

RUTA_BASE = obtener_ruta_base()

def obtener_ruta_sesion_json() -> str:
    ruta_absoluta_sesion_json = os.path.join(
        "sesion_usuario.json"
    )
    
    ruta_final_sesion_json = os.path.join(RUTA_BASE, ruta_absoluta_sesion_json)
    return ruta_final_sesion_json

def obtener_ruta_reportes(indice_opcion_tipo_reporte: str) -> str:
    ruta_documentos = get_my_documents()
    ruta_reportes = os.path.join(ruta_documentos, "REPORTES_SERVICIOS")
    
    opcion_tipo_reporte = TiposReporte[f"{indice_opcion_tipo_reporte}"]
    ruta_tipo_reporte = os.path.join(ruta_reportes, opcion_tipo_reporte.value)
    
    try:
        os.makedirs(ruta_reportes, exist_ok = True)
        os.makedirs(ruta_tipo_reporte, exist_ok = True)
        return ruta_tipo_reporte
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

def obtener_ruta_manual_usuario() -> str:
    nombre_manual = "MANUAL_USUARIO_SISTEMA_DGTIC.pdf"
    
    ruta_original_manual_usuario = os.path.normpath(
        os.path.join(RUTA_BASE, "recursos", "manual_usuario", nombre_manual)
    )
    
    # Verificación de existencia con mensaje claro si falla
    if not os.path.exists(ruta_original_manual_usuario):
        raise FileNotFoundError(
            f"No se encontró el manual en: {ruta_original_manual_usuario}"
        )
    
    ruta_documentos = get_my_documents()
    ruta_carpeta_manual_usuario = os.path.join(ruta_documentos, "MANUAL_USUARIO")
    ruta_destino_manual_usuario = os.path.join(ruta_carpeta_manual_usuario, nombre_manual)
    
    try:
        os.makedirs(ruta_carpeta_manual_usuario, exist_ok = True)
        shutil.copy2(ruta_original_manual_usuario, ruta_destino_manual_usuario)
        
        if (platform.system() == "Windows"):
            os.startfile(ruta_destino_manual_usuario)
        elif (platform.system() == "Darwin"):
            subprocess.call(("open", ruta_destino_manual_usuario))
        else:
            subprocess.call(("xdg-open", ruta_destino_manual_usuario))
        
        return ruta_destino_manual_usuario
    except Exception as error:
        raise error


if __name__ == "__main__":
    try:
        obtener_ruta_manual_usuario()
    except OSError as error:
        print(f"ERROR AL CREAR LA CARPETA: {error}")
    except Exception as error:
        print(error)