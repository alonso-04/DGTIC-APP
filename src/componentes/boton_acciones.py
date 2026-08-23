import os
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import QSize, Qt


DIRECTORIO_ACTUAL = os.path.dirname(__file__)


class BotonAcciones(QPushButton):
    def __init__(self, texto, variante: str, ruta_estilos_boton: str, padre = None):
        super().__init__(texto, padre)
        
        # DEFINIR LA PROPIEDAD DINÁMICA DE QT "variante"
        self.setProperty("variante", variante)
        
        # CONFIGURAR EL TAMAÑO POR DEFECTO
        self.setMinimumSize(QSize(120, 38))
        
        # CAMBIAR EL CURSOR A POINTER
        self.setCursor(Qt.PointingHandCursor)
        
        self._cargar_estilos(ruta_estilos_boton)
    
    def _cargar_estilos(self, ruta_estilos_boton):
        ruta_estilos = os.path.abspath(os.path.join(DIRECTORIO_ACTUAL, "..", ruta_estilos_boton))
            
        if os.path.exists(ruta_estilos):
            with open(ruta_estilos, "r", encoding="utf-8") as archivo:
                self.setStyleSheet(archivo.read())