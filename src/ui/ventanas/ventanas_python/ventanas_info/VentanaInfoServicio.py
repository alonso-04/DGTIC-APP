from PyQt5.QtWidgets import QDialog, QMessageBox, QCompleter
from PyQt5.QtCore import Qt
from ui.ventanas.ventanas_pyuic.VentanaInfoServicioPyuic import Ui_ventanaInfoServicio
from typing import Dict
from dominio.excepciones import ServicioValidacionError, DepartamentoValidacionError, TipoServicioValidacionError


class VentanaInfoServicio(QDialog, Ui_ventanaInfoServicio):
    def __init__(self, servicio_data: Dict, servicio_controlador):
        super().__init__()
        self.setupUi(self)
        
        self.setWindowFlags(
            Qt.WindowSystemMenuHint |
            Qt.WindowTitleHint |
            Qt.WindowCloseButtonHint
        )
        
        self.servicio_data = servicio_data
        self.servicio_controlador = servicio_controlador
        
        self.configuracion()
        self.cargar_datos()
    
    def configuracion(self):
        self.cargar_completer_departamentos()
        self.cargar_completer_tipos_servicio()
        
        self.botonAcualizarInfoServicio.clicked.connect(self.actualizar_info_servicio)
        self.botonEliminarServicio.clicked.connect(self.eliminar_servicio)
        self.botonCancelar.clicked.connect(self.reject)
    
    def cargar_datos(self): 
        self.deInfoFechaServicio.setDate(self.servicio_data["fecha_servicio"])
        self.inputInfoNombreDepartamento.setText(self.servicio_data["nombre_departamento"])
        self.inputInfoFallaPresenta.setText(self.servicio_data["falla_presenta"])
        self.inputInfoServicioPrestado.setText(self.servicio_data["tipo_servicio_prestado"])
        self.inputInfoNombresTecnicos.setText(self.servicio_data["nombres_tecnicos"])
        self.teInfoObservacionesAdicionales.setText(self.servicio_data["observaciones_adicionales"])
    
    def cargar_completer_departamentos(self):
        departamentos = self.servicio_controlador.filtrar_todos_departamentos_controlador()
        nombres_departamentos = []
        
        for departamento in departamentos:
            nombres_departamentos.append(departamento["nombre_departamento"])

        if (nombres_departamentos):
            completer_departamentos = QCompleter(nombres_departamentos)
            completer_departamentos.setCaseSensitivity(Qt.CaseInsensitive)
            completer_departamentos.setFilterMode(Qt.MatchContains)
            completer_departamentos.setCompletionMode(QCompleter.PopupCompletion)
            
            self.inputInfoNombreDepartamento.setCompleter(completer_departamentos)
    
    def cargar_completer_tipos_servicio(self):
        tipos_servicio = self.servicio_controlador.filtrar_todos_tipos_servicio_controlador()
        nombres_tipo_servicio = []
        
        for tipo_servicio in tipos_servicio:
            nombres_tipo_servicio.append(tipo_servicio["tipo_servicio_prestado"])
        
        if (tipos_servicio):
            completer_tipos_servicio = QCompleter(nombres_tipo_servicio)
            completer_tipos_servicio.setCaseSensitivity(Qt.CaseInsensitive)
            completer_tipos_servicio.setFilterMode(Qt.MatchContains)
            completer_tipos_servicio.setCompletionMode(QCompleter.PopupCompletion)
            
            self.inputInfoServicioPrestado.setCompleter(completer_tipos_servicio)
    
    def actualizar_info_servicio(self):
        try:
            servicio_id = self.servicio_data["servicio_id"]

            nueva_fecha_servicio = self.deInfoFechaServicio.date().toPyDate()
            nuevo_nombre_departamento = self.inputInfoNombreDepartamento.text()
            nueva_falla_presenta = self.inputInfoFallaPresenta.text()
            nuevo_servicio_prestado = self.inputInfoServicioPrestado.text()
            nuevo_nombres_tecnicos  = self.inputInfoNombresTecnicos.text()
            nueva_observacion_adicional = self.teInfoObservacionesAdicionales.toPlainText()
            
            self.servicio_controlador.actualizar_info_servicio_controlador(
                servicio_id,
                nueva_fecha_servicio,
                nuevo_nombre_departamento,
                nueva_falla_presenta,
                nuevo_servicio_prestado,
                nuevo_nombres_tecnicos,
                nueva_observacion_adicional
            )
            
            QMessageBox.information(self, "Éxito", "La información del servicio se ha actualizado correctamente.")
            self.accept()
        except ServicioValidacionError as error:
            QMessageBox.critical(self, "Error", "\n".join(error.errores))
        except DepartamentoValidacionError as error:
            QMessageBox.critical(self, "Error", "\n".join(error.errores))
        except TipoServicioValidacionError as error:
            QMessageBox.critical(self, "Error", "\n".join(error.errores))
        except Exception as error:
            QMessageBox.critical(self, "Error", f"{error}")
    
    def eliminar_servicio(self):
        mensaje_confirmacion = QMessageBox.question(
            self,
            "Confirmar eliminación",
            "¿Estás seguro de que quieres eliminar este registro?",
            QMessageBox.Yes | QMessageBox.No
        )
            
        if (mensaje_confirmacion == QMessageBox.Yes):
            try:
                servicio_id = self.servicio_data["servicio_id"]
                self.servicio_controlador.eliminar_servicio_controlador(servicio_id)
                
                QMessageBox.information(self, "Éxito", "Se eliminó el registro correctamente.")
                self.accept()
            except Exception as error:
                QMessageBox.critical(self, "Error", f"{error}")