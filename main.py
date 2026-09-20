import sys
import os
import io
from cryptography.fernet import Fernet
from pathlib import Path

# Añadimos la carpeta src como el primer sitio del sys.path a buscar en las importaciones
ruta_src = Path(__file__).resolve().parent / "src"
sys.path.insert(0, str(ruta_src))


from dotenv import load_dotenv

# Esta clave generada en src/utilidadess/seguridad.py en la función cifrar_env
# es con motivos demostrativos, cada vez que quieran usarla en desarrollo o empaquetar lo que tienen que hacer es generar una nueva
# y pegarla en esta constante
CLAVE_CIFRADO_ENV_DEMO = b'IlQQ3BAdBoOSghoclsDUsB7L0tvzr4pm449suQa4u3I='

# Si la aplicación se ejecuta como un ejecutable de PyInstaller
if getattr(sys, 'frozen', False):
    # La ruta del .env será el directorio del ejecutable que genera PyInstaller
    dotenv_path = os.path.join(os.path.dirname(sys.executable), "_internal", '.env.enc')
else:
    # En modo de desarrollo, la ruta es la del script
    dotenv_path = os.path.join(os.path.dirname(__file__), '.env.enc')
    
# Cargar las variables de entorno
if os.path.exists(dotenv_path):
    try:
        # 1. Leer el contenido cifrado del archivo
        with open(dotenv_path, "rb") as f:
            datos_cifrados = f.read()

        # 2. Descifrar los datos con Fernet
        fernet = Fernet(CLAVE_CIFRADO_ENV_DEMO)
        datos_descifrados = fernet.decrypt(datos_cifrados)
        
        texto_descifrado = datos_descifrados.decode("utf-8").replace("\r", "")
        
        # Filtramos líneas vacías o corruptas
        lineas_limpias = [linea.strip() for linea in texto_descifrado.split("\n") if linea.strip()]
        texto_final = "\n".join(lineas_limpias)

        # 3. Cargar en el memory buffer totalmente limpio
        buffer = io.StringIO(texto_final)
        load_dotenv(stream=buffer)
    except Exception as e:
        print(f"Error al descifrar o cargar el archivo .env.enc: {e}")

import recursos.recursos_rc as recursos_rc
sys.modules["recursos_rc"] = recursos_rc

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTranslator, QLocale, QLibraryInfo, QThread, pyqtSignal

from vistas.vistas_python.VentanaPrincipal import VentanaPrincipal
from configuraciones.dependencias import contenedor_dependencias
from configuraciones.usuario_admin_init import inicializar_usuario_admin_bd


class HiloInicializarUsuarioAdmin(QThread):
    terminado = pyqtSignal()
    error = pyqtSignal(str)
    
    def run(self):
        try:
            inicializar_usuario_admin_bd()
            self.terminado.emit()
        except Exception as error:
            self.error.emit(str(error))


def main():
    app = QApplication(sys.argv)
    
    from configuraciones.conexion import bd
    
    try:
        bd.inicializar_conexion()
    except Exception as error:
        print(f"Error crítico al preparar la base de datos y tablas: {error}")
    
    # Para cargar la traducción al español al texto de los botones de los elementos
    path = QLibraryInfo.location(QLibraryInfo.TranslationsPath)
    
    translator_base = QTranslator()
    if translator_base.load(QLocale.system(), "qtbase", "_", path):
        app.installTranslator(translator_base)
    
    hilo_inicializar_usuario_admin = HiloInicializarUsuarioAdmin()
    hilo_inicializar_usuario_admin.terminado.connect(lambda: print("Admin principal listo."))
    hilo_inicializar_usuario_admin.error.connect(lambda error: print(f"Error al inicializar usuario admin principal: {error}"))
    hilo_inicializar_usuario_admin.start()
    
    servicios = contenedor_dependencias.obtener_servicios()
    
    # Creo la instancia de la ventana principal que contiene todas las demaás
    ventana_principal = VentanaPrincipal(servicios, "VentanaPrincipal.ui", "estilos_globales.qss")
    ventana_principal.abrir()
    
    app.exec_()


if __name__ == "__main__":
    main()