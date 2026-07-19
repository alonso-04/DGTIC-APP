from typing import Tuple
from PyQt5.QtWidgets import QDialog, QMessageBox, QCompleter
from PyQt5.QtCore import Qt

from vistas.vistas_pyuic.VentanaInfoTipoServicioPyuic import Ui_VentanaInfoTipoServicio
from vistas.vistas_python.VentanaPrincipal import VentanaPrincipal
from configuraciones.excepciones import ValidacionError, NoEncontradoError, LogicaError


class VentanaInfoTipoServicio(QDialog, Ui_VentanaInfoTipoServicio):
    def __init__(self, tipo_servicio_data: Tuple, ventana_principal: VentanaPrincipal):
        super().__init__()
        self.setupUi(self)
        
        self.setWindowFlags(
            Qt.WindowSystemMenuHint |
            Qt.WindowTitleHint |
            Qt.WindowCloseButtonHint
        )
        
        self.tipo_servicio_data = tipo_servicio_data
        self.ventana_principal = ventana_principal
        self._servicios = self.ventana_principal._servicios
        
        self.cargar_completer_tipos_servicio = self.ventana_principal.cargar_completer_tipos_servicio
        
        self.configuracion()
    
    def configuracion(self):
        self.cargar_completer_tipos_servicio()
        self.cargar_completer_categorias()
        
        self.botonAcualizarInfoTipoServicio.clicked.connect(self.actualizar_info_tipo_servicio)
        self.botonEliminarTipoServicio.clicked.connect(self.eliminar_tipo_servicio)
        self.botonCancelarInfoTipoServicio.clicked.connect(self.reject)
    
    def actualizar_data_recibida(self, data_recibida: Tuple):
        self.tipo_servicio_data = data_recibida
        self.cargar_datos()
    
    def cargar_datos(self):
        self.inputInfoNombreTipoServicio.setText(self.tipo_servicio_data[1])
        self.inputInfoNombreCategoria.setText(self.tipo_servicio_data[2])
    
    def actualizar_info_tipo_servicio(self):
        try:
            tipo_servicio_id = self.tipo_servicio_data[0]
            nuevo_nombre_tipo_servicio = self.inputInfoNombreTipoServicio.text()
            nuevo_categoria_tipo_servicio = self.inputInfoNombreCategoria.text()
            
            self._servicios["tipo_servicio_tecnico_servicio"].actualizar(
                tipo_servicio_id,
                nuevo_categoria_tipo_servicio,
                nuevo_nombre_tipo_servicio.upper()
            )
            
            QMessageBox.information(self, "Éxito", "La información del tipo de servicio se ha actualizado correctamente.")
            self.cargar_completer_tipos_servicio()
            self.accept()
        except NoEncontradoError as error:
            QMessageBox.critical(self, "Error", "\n".join(error.errores))
        except ValidacionError as error:
            QMessageBox.critical(self, "Error", "\n".join(error.errores))
        except LogicaError as error:
            QMessageBox.critical(self, "Error", "\n".join(error.errores))
    
    def eliminar_tipo_servicio(self):
        mensaje_confirmacion = QMessageBox.question(
            self,
            "Confirmar eliminación",
            "¿Estás seguro de que quieres eliminar este tipo de servicio?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if (mensaje_confirmacion == QMessageBox.Yes):
            try:
                tipo_servicio_id = self.tipo_servicio_data[0]
                self._servicios["tipo_servicio_tecnico_servicio"].eliminar(tipo_servicio_id)
                
                QMessageBox.information(self, "Éxito", "Se ha eliminado el tipo de servicio correctamente.")
                self.cargar_completer_tipos_servicio()
                self.accept()
            except NoEncontradoError as error:
                QMessageBox.critical(self, "Error", "\n".join(error.errores))
            except ValidacionError as error:
                QMessageBox.critical(self, "Error", "\n".join(error.errores))
            except LogicaError as error:
                QMessageBox.critical(self, "Error", "\n".join(error.errores))
    
    def cargar_completer_categorias(self):
        categoria_tipo_servicio_tecnico_servicio = self._servicios["categoria_tipo_servicio_tecnico_servicio"]
        categorias = categoria_tipo_servicio_tecnico_servicio.obtener_todos()
        
        nombres_categorias = []
        
        if (categorias):
            for categoria in categorias:
                nombres_categorias.append(categoria.nombre_categoria)
        
        if not(nombres_categorias):
            completer_categorias = QCompleter([])
        else:
            completer_categorias = QCompleter(nombres_categorias)
            
        completer_categorias.setCaseSensitivity(Qt.CaseInsensitive)
        completer_categorias.setFilterMode(Qt.MatchContains)
        completer_categorias.setCompletionMode(QCompleter.PopupCompletion)
            
        self.inputInfoNombreCategoria.setCompleter(completer_categorias)