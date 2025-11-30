from PyQt5.QtWidgets import QDialog, QMessageBox, QCompleter
from PyQt5.QtCore import Qt
from ui.ventanas.ventanas_pyuic.VentanaInfoTipoServicioPyuic import Ui_VentanaInfoTipoServicio
from dominio.excepciones import TipoServicioValidacionError
from typing import Dict


class VentanaInfoTipoServicio(QDialog, Ui_VentanaInfoTipoServicio):
    def __init__(self, tipo_servicio_data: Dict, servicio_controlador, ventana_principal):
        super().__init__()
        self.setupUi(self)
        
        self.setWindowFlags(
            Qt.WindowSystemMenuHint |
            Qt.WindowTitleHint |
            Qt.WindowCloseButtonHint
        )
        
        self.tipo_servicio_data = tipo_servicio_data
        self.servicio_controlador = servicio_controlador
        self.ventana_principal = ventana_principal
        
        self.cargar_completer_tipos_servicio = self.ventana_principal.cargar_completer_tipos_servicio
        
        self.configuracion()
        self.cargar_datos()
    
    def configuracion(self):
        self.cargar_completer_tipos_servicio()
        
        self.botonAcualizarInfoTipoServicio.clicked.connect(self.actualizar_info_tipo_servicio)
        self.botonEliminarTipoServicio.clicked.connect(self.eliminar_tipo_servicio)
        self.botonCancelarInfoTipoServicio.clicked.connect(self.reject)
    
    def cargar_datos(self):
        self.inputInfoNombreTipoServicio.setText(self.tipo_servicio_data["tipo_servicio_prestado"])
    
    def actualizar_info_tipo_servicio(self):
        try:
            tipo_servicio_id = self.tipo_servicio_data["tipo_servicio_id"]
            nuevo_nombre_tipo_servicio = self.inputInfoNombreTipoServicio.text()
            
            self.servicio_controlador.actualizar_tipo_servicio_controlador(
                tipo_servicio_id,
                nuevo_nombre_tipo_servicio
            )
            
            QMessageBox.information(self, "Error", "La información del tipo de servicio se ha actualizado correctamente.")
            self.cargar_completer_tipos_servicio()
            self.accept()
        except TipoServicioValidacionError as error:
            QMessageBox.critical(self, "Error", "\n".join(error.errores))
        except Exception as error:
            QMessageBox.critical(self, "Error", f"{error}")
    
    def eliminar_tipo_servicio(self):
        mensaje_confirmacion = QMessageBox.question(
            self,
            "Confirmar eliminación",
            "¿Estás seguro de que quieres eliminar este tipo de servicio?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if (mensaje_confirmacion == QMessageBox.Yes):
            try:
                tipo_servicio_id = self.tipo_servicio_data["tipo_servicio_id"]
                self.servicio_controlador.eliminar_tipo_servicio_controlador(tipo_servicio_id)
                
                QMessageBox.information(self, "Éxito", "Se ha eliminado el tipo de servicio correctamente.")
                self.cargar_completer_tipos_servicio()
                self.accept()
            except TipoServicioValidacionError as error:
                QMessageBox.critical(self, "Error", "\n".join(error.errores))
            except Exception as error:
                QMessageBox.critical(self, "Error", f"{error}")