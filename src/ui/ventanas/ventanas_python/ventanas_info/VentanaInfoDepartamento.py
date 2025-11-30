from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5.QtCore import Qt
from ui.ventanas.ventanas_pyuic.VentanaInfoDepartamentoPyuic import Ui_VentanaInfoDepartamento
from dominio.excepciones import DepartamentoValidacionError
from typing import Dict


class VentanaInfoDepartamento(QDialog, Ui_VentanaInfoDepartamento):
    def __init__(self, departamento_data: Dict, servicio_controlador, ventana_principal):
        super().__init__()
        self.setupUi(self)
        
        self.setWindowFlags(
            Qt.WindowSystemMenuHint |
            Qt.WindowTitleHint |
            Qt.WindowCloseButtonHint
        )
        
        self.departamento_data = departamento_data
        self.servicio_controlador = servicio_controlador
        self.ventana_principal = ventana_principal
        
        self.cargar_completer_departamento = self.ventana_principal.cargar_completer_departamento
        
        self.configuracion()
        self.cargar_datos()
    
    def configuracion(self):
        self.cargar_completer_departamento()
        
        self.botonAcualizarInfoDepartamento.clicked.connect(self.actualizar_info_departamento)
        self.botonEliminarDepartamento.clicked.connect(self.eliminar_departamento)
        self.botonCancelarInfoDepartamento.clicked.connect(self.reject)
    
    def cargar_datos(self):
        self.inputInfoNombreDepartamento.setText(self.departamento_data["nombre_departamento"])
    
    def actualizar_info_departamento(self):
        try:
            departamento_id = self.departamento_data["departamento_id"]
            nuevo_nombre_departamento = self.inputInfoNombreDepartamento.text()
            
            self.servicio_controlador.actualizar_info_departamento_controlador(
                departamento_id,
                nuevo_nombre_departamento
            )
            
            QMessageBox.information(self, "Éxito", "La información del departamento se ha actualizado correctamente.")
            self.cargar_completer_departamento()
            self.accept()
        except DepartamentoValidacionError as error:
            QMessageBox.critical(self, "Error", "\n".join(error.errores))
        except Exception as error:
            QMessageBox.critical(self, "Error", f"{error}")
    
    def eliminar_departamento(self):
        mensaje_confirmacion = QMessageBox.question(
            self,
            "Confirmar eliminación",
            "¿Estás seguro de que quieres eliminar este departamento?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if (mensaje_confirmacion == QMessageBox.Yes):
            try:
                departamento_id = self.departamento_data["departamento_id"]
                self.servicio_controlador.eliminar_departamento_controlador(departamento_id)
                
                QMessageBox.information(self, "Éxito", "Se ha eliminado el departamento correctamente.")
                self.cargar_completer_departamento()
                self.accept()
            except DepartamentoValidacionError as error:
                QMessageBox.critical(self, "Error", "\n".join(error.errores))
            except Exception as error:
                QMessageBox.critical(self, "Error", f"{error}")