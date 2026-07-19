from typing import Tuple
from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5.QtCore import Qt

from vistas.vistas_pyuic.VentanaInfoDepartamentoPyuic import Ui_VentanaInfoDepartamento
from vistas.vistas_python.VentanaPrincipal import VentanaPrincipal
from configuraciones.excepciones import ValidacionError, NoEncontradoError, LogicaError


class VentanaInfoDepartamento(QDialog, Ui_VentanaInfoDepartamento):
    def __init__(self, departamento_data: Tuple, ventana_principal: VentanaPrincipal):
        super().__init__()
        self.setupUi(self)
        
        self.setWindowFlags(
            Qt.WindowSystemMenuHint |
            Qt.WindowTitleHint |
            Qt.WindowCloseButtonHint
        )
        
        self.departamento_data = departamento_data
        self.ventana_principal = ventana_principal
        self._servicios = self.ventana_principal._servicios
        
        self.cargar_completer_departamento = self.ventana_principal.cargar_completer_departamento
        
        self.configuracion()
    
    def configuracion(self):
        self.cargar_completer_departamento()
        
        self.botonAcualizarInfoDepartamento.clicked.connect(self.actualizar_info_departamento)
        self.botonEliminarDepartamento.clicked.connect(self.eliminar_departamento)
        self.botonCancelarInfoDepartamento.clicked.connect(self.reject)
    
    def actualizar_data_recibida(self, data_recibida: Tuple):
        self.departamento_data = data_recibida
        self.cargar_datos()
    
    def cargar_datos(self):
        self.inputInfoNombreDepartamento.setText(self.departamento_data[1])
    
    def actualizar_info_departamento(self):
        try:
            departamento_id = self.departamento_data[0]
            nuevo_nombre_departamento = self.inputInfoNombreDepartamento.text()
            
            self._servicios["departamento_servicio"].actualizar(
                departamento_id,
                nuevo_nombre_departamento
            )
            
            QMessageBox.information(self, "Éxito", "La información del departamento se ha actualizado correctamente.")
            self.cargar_completer_departamento()
            self.accept()
        except NoEncontradoError as error:
            QMessageBox.critical(self, "Error", "\n".join(error.errores))
        except ValidacionError as error:
            QMessageBox.critical(self, "Error", "\n".join(error.errores))
        except LogicaError as error:
            QMessageBox.critical(self, "Error", "\n".join(error.errores))
    
    def eliminar_departamento(self):
        mensaje_confirmacion = QMessageBox.question(
            self,
            "Confirmar eliminación",
            "¿Estás seguro de que quieres eliminar este departamento?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if (mensaje_confirmacion == QMessageBox.Yes):
            try:
                departamento_id = self.departamento_data[0]
                self._servicios["departamento_servicio"].eliminar(departamento_id)
                
                QMessageBox.information(self, "Éxito", "Se ha eliminado el departamento correctamente.")
                self.cargar_completer_departamento()
                self.accept()
            except NoEncontradoError as error:
                QMessageBox.critical(self, "Error", "\n".join(error.errores))
            except ValidacionError as error:
                QMessageBox.critical(self, "Error", "\n".join(error.errores))
            except LogicaError as error:
                QMessageBox.critical(self, "Error", "\n".join(error.errores))