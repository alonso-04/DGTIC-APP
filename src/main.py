import sys
import os

# Para que el archivo generado por pyuic5 encuentre los recursos correctamente le asignamos
# la clave exacta que espera el archivo generado (recursos_rc)
import recursos.recursos_rc as recursos_rcs
sys.modules["recursos_rc"] = recursos_rcs

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
    
    # Para cargar la traducción al español al texto de los botones de los elementos
    path = QLibraryInfo.location(QLibraryInfo.TranslationsPath)
    
    translator_base = QTranslator()
    if translator_base.load(QLocale.system(), "qtbase", "_", path):
        app.installTranslator(translator_base)
    
    hilo_inicializar_usuario_admin = HiloInicializarUsuarioAdmin()
    hilo_inicializar_usuario_admin.terminado.connect(lambda: print("Admin listo."))
    hilo_inicializar_usuario_admin.error.connect(lambda error: print(f"Error al inicializar usuario admin: {error}"))
    hilo_inicializar_usuario_admin.start()
    
    servicios = contenedor_dependencias.obtener_servicios()
    
    # Creo la instancia de la ventana principal que contiene todas las demaás
    ventana_principal = VentanaPrincipal(servicios, "VentanaPrincipal.ui", "estilos_globales.qss")
    ventana_principal.abrir()
    
    app.exec_()


if __name__ == "__main__":
    main()