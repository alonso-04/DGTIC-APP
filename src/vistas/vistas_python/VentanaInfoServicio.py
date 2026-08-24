from typing import Tuple
from datetime import datetime
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import Qt, QRegExp, QEvent
from PyQt5.QtGui import QRegExpValidator

from utilidades.gui import UiBase
from vistas.utilidades_gui.cargar_completers import cargar_completer
from configuraciones.excepciones import NoEncontradoError, ValidacionError, LogicaError


class VentanaInfoServicio(UiBase):
    def __init__(self, servicio_data: Tuple, servicios, nombre_archivo_ui: str, nombre_archivo_estilos: str):
        super().__init__(nombre_archivo_ui, nombre_archivo_estilos)
        
        self.ui.setWindowFlags(
            Qt.WindowSystemMenuHint |
            Qt.WindowTitleHint |
            Qt.WindowCloseButtonHint
        )
        
        self.servicio_data = servicio_data
        self._servicios = servicios
        
        self.line_edit_spbox_cantidad = self.ui.spbox_cantidad.lineEdit()
        regex = QRegExp("[0-9]+")
        validador = QRegExpValidator(regex, self.line_edit_spbox_cantidad)
        self.line_edit_spbox_cantidad.setValidator(validador)
        self.line_edit_spbox_cantidad.installEventFilter(self.ui)
        
        lista_campos_departamento_completers = [self.ui.txt_nombre_departamento]
        lista_campos_tipos_servicio_completers = [self.ui.txt_servicio_prestado]
        lista_campos_comuna_completers = [self.ui.txt_nombre_comuna]
        
        self.cargar_completer_comunas = lambda: cargar_completer(
            self._servicios["comuna_servicio"],
            lista_campos_comuna_completers,
            "comuna"
        )
        
        self.cargar_completer_departamento = lambda: cargar_completer(
            self._servicios["departamento_servicio"],
            lista_campos_departamento_completers,
            "departamento"
        )
                
        self.cargar_completer_tipos_servicio = lambda: cargar_completer(
            self._servicios["tipo_servicio_tecnico_servicio"],
            lista_campos_tipos_servicio_completers,
            "tipo_servicio"
        )
        
        self.cargar_botones()
        
        self.configuracion()
    
    def eventFilter(self, obj, event):
        if obj is self.line_edit_spbox_cantidad and event.type() == QEvent.KeyPress:
            if event.text() == ',':
                return True  # Bloquea la coma del spInfoCantidad
        return super().eventFilter(obj, event)
    
    def configuracion(self):
        self.cargar_completer_departamento()
        self.cargar_completer_tipos_servicio()
        self.cargar_completer_comunas()
        
        self.btn_actualizar.clicked.connect(self.actualizar_info_servicio)
        self.btn_eliminar.clicked.connect(self.eliminar_servicio)
        self.btn_cancelar.clicked.connect(self.ui.reject)
    
    def actualizar_data_recibida(self, data_recibida: Tuple):
        self.servicio_data = data_recibida
        self.cargar_datos()
    
    def cargar_datos(self):
        fecha_servicio_str = self.servicio_data[4].strftime("%d-%m-%Y")
        fecha_servicio_date = datetime.strptime(fecha_servicio_str, "%d-%m-%Y").date()
        
        self.ui.de_fecha.setDate(fecha_servicio_date)
        self.ui.txt_nombre_departamento.setText(self.servicio_data[3])
        self.ui.txt_falla_presenta.setText(self.servicio_data[5])
        self.ui.txt_servicio_prestado.setText(self.servicio_data[6])
        self.ui.txt_nombres_tecnicos.setText(self.servicio_data[7])
        self.ui.txt_descripcion.setText(self.servicio_data[8])
        self.ui.spbox_cantidad.setValue(self.servicio_data[9])
        self.ui.txt_observaciones.setText(self.servicio_data[10])
        self.ui.txt_nombre_comuna.setText(self.servicio_data[11])
    
    def actualizar_info_servicio(self):
        try:
            servicio_id = self.servicio_data[0]

            nueva_fecha_servicio = self.ui.de_fecha.date().toPyDate()
            nuevo_nombre_departamento = self.ui.txt_nombre_departamento.text()
            nueva_falla_presenta = self.ui.txt_falla_presenta.text()
            nuevo_servicio_prestado = self.ui.txt_servicio_prestado.text()
            nuevo_nombres_tecnicos  = self.ui.txt_nombres_tecnicos.text()
            nuevo_cantidad = self.ui.spbox_cantidad.value()
            nuevo_descripcion = self.ui.txt_descripcion.text()
            nueva_observacion_adicional = self.ui.txt_observaciones.text()
            nueva_comuna = self.ui.txt_nombre_comuna.text()
            
            self._servicios["servicio_tecnico_servicio"].actualizar(
                servicio_id,
                nuevo_nombre_departamento,
                nueva_fecha_servicio,
                nueva_falla_presenta.upper(),
                nuevo_servicio_prestado,
                nuevo_nombres_tecnicos.upper(),
                nuevo_cantidad,
                nuevo_descripcion.upper(),
                nueva_observacion_adicional.upper(),
                nueva_comuna.upper()
            )
            
            QMessageBox.information(self.ui, "Éxito", "La información del servicio se ha actualizado correctamente.")
            self.ui.accept()
        except NoEncontradoError as error:
            QMessageBox.critical(self.ui, "Error", "\n".join(error.errores))
        except ValidacionError as error:
            QMessageBox.critical(self.ui, "Error", "\n".join(error.errores))
        except LogicaError as error:
            QMessageBox.critical(self.ui, "Error", "\n".join(error.errores))
    
    def eliminar_servicio(self):
        mensaje_confirmacion = QMessageBox.question(
            self.ui,
            "Confirmar eliminación",
            "¿Estás seguro de que quieres eliminar este registro?",
            QMessageBox.Yes | QMessageBox.No
        )
            
        if (mensaje_confirmacion == QMessageBox.Yes):
            try:
                servicio_id = self.servicio_data[0]
                self._servicios["servicio_tecnico_servicio"].eliminar(servicio_id)
                
                QMessageBox.information(self.ui, "Éxito", "Se eliminó el registro correctamente.")
                self.ui.accept()
            except NoEncontradoError as error:
                QMessageBox.critical(self.ui, "Error", "\n".join(error.errores))
            except LogicaError as error:
                QMessageBox.critical(self.ui, "Error", "\n".join(error.errores))