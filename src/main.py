import sys
import os

# Para que el archivo generado por pyuic5 encuentre los recursos correctamente le asignamos
# la clave exacta que espera el archivo generado (qtRecursosIconos_rc y qtRecursosLogos_rc)
import recursos.qtRecursosIconos_rc as recursos_iconos_rc
import recursos.qtRecursosLogos_rc as recursos_logos_rc

sys.modules["qtRecursosIconos_rc"] = recursos_iconos_rc
sys.modules["qtRecursosLogos_rc"] = recursos_logos_rc

from dotenv import load_dotenv

# Si la aplicación se ejecuta como un ejecutable de PyInstaller
if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    # La ruta del .env será el directorio temporal de PyInstaller
    dotenv_path = os.path.join(sys._MEIPASS, '.env.ejemplo')
else:
    # En modo de desarrollo, la ruta es la del script
    dotenv_path = os.path.join(os.path.dirname(__file__), "..", '.env')
    
# Cargar las variables de entorno
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path = dotenv_path)


from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTranslator, QLocale, QLibraryInfo

from vistas.vistas_python.VentanaPrincipal import VentanaPrincipal
from configuraciones.dependencias import contenedor_dependencias
from configuraciones.usuario_admin_init import inicializar_usuario_admin_bd


def main():
    app = QApplication(sys.argv)
    
    # Para cargar la traducción al español al texto de los botones de los elementos
    path = QLibraryInfo.location(QLibraryInfo.TranslationsPath)
    
    translator_base = QTranslator()
    if translator_base.load(QLocale.system(), "qtbase", "_", path):
        app.installTranslator(translator_base)
    
    try:
        inicializar_usuario_admin_bd()
    except Exception as e:
        print(f"Advertencia al inicializar base de datos: {e}")
    
    servicios = contenedor_dependencias.obtener_servicios()
    
    # Creo la instancia de la ventana principal que contiene todas las demaás
    ventana_principal = VentanaPrincipal(servicios)
    ventana_principal.show()
    
    app.exec_()


if __name__ == "__main__":
    main()