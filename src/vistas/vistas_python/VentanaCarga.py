from PyQt5.QtCore import Qt

from utilidades.gui import UiBase


class VentanaCarga(UiBase):
    def __init__(self, nombre_archivo_ui: str, nombre_archivo_estilos: str):
        super().__init__(nombre_archivo_ui, nombre_archivo_estilos)
        
        self.ui.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.ui.barra_carga.setRange(0, 0)
    
    def closeEvent(self, evento):
        evento.ignore()