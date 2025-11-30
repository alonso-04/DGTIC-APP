import sys

# Para que el archivo generado por pyuic5 encuentre los recursos correctamente le asignamos
# la clave exacta que espera el archivo generado (qtRecursosIconos_rc y qtRecursosLogos_rc)
import recursos.qtRecursosIconos_rc as recursos_iconos_rc
import recursos.qtRecursosLogos_rc as recursos_logos_rc

sys.modules["qtRecursosIconos_rc"] = recursos_iconos_rc
sys.modules["qtRecursosLogos_rc"] = recursos_logos_rc

from dotenv import load_dotenv

load_dotenv()

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTranslator, QLocale, QLibraryInfo
from ui.ventanas.ventanas_python.ventanas_principales.VentanaPrincipal import VentanaPrincipal
from ui.ventanas.ventanas_python.ventanas_principales.VentanaApp import VentanaApp
from ui.ventanas.ventanas_python.ventanas_principales.VentanaUsuarios import VentanaUsuarios
from ui.ventanas.ventanas_python.ventanas_principales.VentanaDepartamentos import VentanaDepartamentos
from ui.ventanas.ventanas_python.ventanas_principales.VentanaTipoServicio import VentanaTipoServicio
from infraestructura.dependencias import contenedor_dependencias
from infraestructura.usuario_admin_init import inicializar_usuario_admin_bd

USUARIO_CONTROLADOR = contenedor_dependencias.obtener_usuario_controlador()
SERVICIO_CONTROLADOR = contenedor_dependencias.obtener_servicio_controlador()

def main():
    app = QApplication(sys.argv)
    
    # Para cargar la traducción al español al texto de los botones de los elementos
    path = QLibraryInfo.location(QLibraryInfo.TranslationsPath)
    
    translator_base = QTranslator()
    if translator_base.load(QLocale.system(), "qtbase", "_", path):
        app.installTranslator(translator_base)
    
    # Creo la instancia de la ventana principal que contiene todas las demaás
    ventana_principal = VentanaPrincipal(
        usuario_controlador = USUARIO_CONTROLADOR,
        servicio_controlador = SERVICIO_CONTROLADOR
    )
    
    # Creo la instancia de cada ventana por separado pasandole por inyección de dependencias la ventana_principal
    ventana_app = VentanaApp(ventana_principal)
    ventana_usuarios = VentanaUsuarios(ventana_principal)
    ventana_departamentos = VentanaDepartamentos(ventana_principal)
    ventana_tipo_servicio = VentanaTipoServicio(ventana_principal)
    
    ventana_principal.show()
    
    app.exec_()


if __name__ == "__main__":
    inicializar_usuario_admin_bd()
    main()