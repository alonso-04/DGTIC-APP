from typing import Tuple
from datetime import datetime
from PyQt5.QtWidgets import QDialog, QMessageBox, QCompleter
from PyQt5.QtCore import Qt, QRegExp, QEvent
from PyQt5.QtGui import QRegExpValidator

from vistas.vistas_pyuic.VentanaInfoServicioPyuic import Ui_ventanaInfoServicio
from configuraciones.excepciones import NoEncontradoError, ValidacionError, LogicaError


class VentanaInfoServicio(QDialog, Ui_ventanaInfoServicio):
    def __init__(self, servicio_data: Tuple, servicios):
        super().__init__()
        self.setupUi(self)
        
        self.setWindowFlags(
            Qt.WindowSystemMenuHint |
            Qt.WindowTitleHint |
            Qt.WindowCloseButtonHint
        )
        
        self.servicio_data = servicio_data
        self._servicios = servicios
        
        self.lineEditspInfoCantidad = self.spInfoCantidad.lineEdit()
        regex = QRegExp("[0-9]+")
        validador = QRegExpValidator(regex, self.lineEditspInfoCantidad)
        self.lineEditspInfoCantidad.setValidator(validador)
        self.lineEditspInfoCantidad.installEventFilter(self)
        
        self.configuracion()
    
    def eventFilter(self, obj, event):
        if obj is self.lineEditspInfoCantidad and event.type() == QEvent.KeyPress:
            if event.text() == ',':
                return True  # Bloquea la coma del spInfoCantidad
        return super().eventFilter(obj, event)
    
    def configuracion(self):
        self.cargar_completer_departamentos()
        self.cargar_completer_tipos_servicio()
        
        self.botonAcualizarInfoServicio.clicked.connect(self.actualizar_info_servicio)
        self.botonEliminarServicio.clicked.connect(self.eliminar_servicio)
        self.botonCancelar.clicked.connect(self.reject)
    
    def actualizar_data_recibida(self, data_recibida: Tuple):
        self.servicio_data = data_recibida
        self.cargar_datos()
    
    def cargar_datos(self):
        fecha_servicio_str = self.servicio_data[4].strftime("%d-%m-%Y")
        fecha_servicio_date = datetime.strptime(fecha_servicio_str, "%d-%m-%Y").date()
        
        self.deInfoFechaServicio.setDate(fecha_servicio_date)
        self.inputInfoNombreDepartamento.setText(self.servicio_data[3])
        self.inputInfoFallaPresenta.setText(self.servicio_data[5])
        self.inputInfoServicioPrestado.setText(self.servicio_data[6])
        self.inputInfoNombresTecnicos.setText(self.servicio_data[7])
        self.teInfoDescripcion.setText(self.servicio_data[8])
        self.spInfoCantidad.setValue(self.servicio_data[9])
        self.teInfoObservacionesAdicionales.setText(self.servicio_data[10])
    
    def cargar_completer_departamentos(self):
        departamento_servicio = self._servicios["departamento_servicio"]
        departamentos = departamento_servicio.obtener_todos()
        nombres_departamentos = []
        
        for departamento in departamentos:
            nombres_departamentos.append(departamento.nombre_departamento)

        if (nombres_departamentos):
            completer_departamentos = QCompleter(nombres_departamentos)
            completer_departamentos.setCaseSensitivity(Qt.CaseInsensitive)
            completer_departamentos.setFilterMode(Qt.MatchContains)
            completer_departamentos.setCompletionMode(QCompleter.PopupCompletion)
            
            self.inputInfoNombreDepartamento.setCompleter(completer_departamentos)
    
    def cargar_completer_tipos_servicio(self):
        tipos_servicio_tecnico_servicio = self._servicios["tipo_servicio_tecnico_servicio"]
        tipos_servicio = tipos_servicio_tecnico_servicio.obtener_todos()
        nombres_tipo_servicio = []
        
        for tipo_servicio in tipos_servicio:
            nombres_tipo_servicio.append(tipo_servicio.tipo_servicio_prestado)
        
        if (tipos_servicio):
            completer_tipos_servicio = QCompleter(nombres_tipo_servicio)
            completer_tipos_servicio.setCaseSensitivity(Qt.CaseInsensitive)
            completer_tipos_servicio.setFilterMode(Qt.MatchContains)
            completer_tipos_servicio.setCompletionMode(QCompleter.PopupCompletion)
            
            self.inputInfoServicioPrestado.setCompleter(completer_tipos_servicio)
    
    def actualizar_info_servicio(self):
        try:
            servicio_id = self.servicio_data[0]

            nueva_fecha_servicio = self.deInfoFechaServicio.date().toPyDate()
            nuevo_nombre_departamento = self.inputInfoNombreDepartamento.text()
            nueva_falla_presenta = self.inputInfoFallaPresenta.text()
            nuevo_servicio_prestado = self.inputInfoServicioPrestado.text()
            nuevo_nombres_tecnicos  = self.inputInfoNombresTecnicos.text()
            nuevo_cantidad = self.spInfoCantidad.value()
            nuevo_descripcion = self.teInfoDescripcion.toPlainText()
            nueva_observacion_adicional = self.teInfoObservacionesAdicionales.toPlainText()
            
            self._servicios["servicio_tecnico_servicio"].actualizar(
                servicio_id,
                nuevo_nombre_departamento,
                nueva_fecha_servicio,
                nueva_falla_presenta,
                nuevo_servicio_prestado,
                nuevo_nombres_tecnicos,
                nuevo_cantidad,
                nuevo_descripcion,
                nueva_observacion_adicional
            )
            
            QMessageBox.information(self, "Éxito", "La información del servicio se ha actualizado correctamente.")
            self.accept()
        except NoEncontradoError as error:
            QMessageBox.critical(self, "Error", "\n".join(error.errores))
        except ValidacionError as error:
            QMessageBox.critical(self, "Error", "\n".join(error.errores))
        except LogicaError as error:
            QMessageBox.critical(self, "Error", "\n".join(error.errores))
    
    def eliminar_servicio(self):
        mensaje_confirmacion = QMessageBox.question(
            self,
            "Confirmar eliminación",
            "¿Estás seguro de que quieres eliminar este registro?",
            QMessageBox.Yes | QMessageBox.No
        )
            
        if (mensaje_confirmacion == QMessageBox.Yes):
            try:
                servicio_id = self.servicio_data[0]
                self._servicios["servicio_tecnico_servicio"].eliminar(servicio_id)
                
                QMessageBox.information(self, "Éxito", "Se eliminó el registro correctamente.")
                self.accept()
            except NoEncontradoError as error:
                QMessageBox.critical(self, "Error", "\n".join(error.errores))
            except LogicaError as error:
                QMessageBox.critical(self, "Error", "\n".join(error.errores))