from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import Qt
from ui.ventanas.ventanas_pyuic.VentanaImportacionBdPyuic import Ui_VentanaCargaImportacion


class VentanaImportacionBd(QDialog, Ui_VentanaCargaImportacion):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.barraProgresoImportacionBd.setRange(0, 0)
    
    def closeEvent(self, evento):
        evento.ignore()