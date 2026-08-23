from typing import Tuple
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import Qt

from utilidades.gui import UiBase
from vistas.vistas_python.VentanaPrincipal import VentanaPrincipal
from vistas.utilidades_gui.cargar_completers import cargar_completer
from configuraciones.excepciones import ValidacionError, NoEncontradoError, LogicaError


class VentanaInfoTipoServicio(UiBase):
    def __init__(self, tipo_servicio_data: Tuple, ventana_principal: VentanaPrincipal, nombre_archivo_ui: str, nombre_archivo_estilos: str):
        super().__init__(nombre_archivo_ui, nombre_archivo_estilos)
        
        self.ui.setWindowFlags(
            Qt.WindowSystemMenuHint |
            Qt.WindowTitleHint |
            Qt.WindowCloseButtonHint
        )
        
        self.tipo_servicio_data = tipo_servicio_data
        self.ventana_principal = ventana_principal.ui
        self._servicios = ventana_principal._servicios
        
        lista_campos_tipos_servicio_completers = [
            self.ventana_principal.txt_servicio_prestado,
            self.ventana_principal.txt_filtro_servicio_prestado,
            self.ventana_principal.txt_filtro_tipos_servicios_registrados
        ]
        
        lista_campos_categorias_completers = [self.ui.txt_nombre_categoria_asociada]
        
        self.cargar_completer_tipos_servicio = lambda: cargar_completer(
            self._servicios["tipo_servicio_tecnico_servicio"],
            lista_campos_tipos_servicio_completers,
            "tipo_servicio"
        )
        
        self.cargar_completer_categorias = lambda: cargar_completer(
            self._servicios["categoria_tipo_servicio_tecnico_servicio"],
            lista_campos_categorias_completers,
            "categoria"
        )
        
        self.cargar_botones()
        self.configuracion()
    
    def configuracion(self):
        self.cargar_completer_categorias()
        
        self.btn_actualizar.clicked.connect(self.actualizar_info_tipo_servicio)
        self.btn_eliminar.clicked.connect(self.eliminar_tipo_servicio)
        self.btn_cancelar.clicked.connect(self.ui.reject)
    
    def actualizar_data_recibida(self, data_recibida: Tuple):
        self.tipo_servicio_data = data_recibida
        self.cargar_datos()
    
    def cargar_datos(self):
        self.ui.txt_nombre_tipo_servicio.setText(self.tipo_servicio_data[1])
        self.ui.txt_nombre_categoria_asociada.setText(self.tipo_servicio_data[2])
    
    def actualizar_info_tipo_servicio(self):
        try:
            tipo_servicio_id = self.tipo_servicio_data[0]
            nuevo_nombre_tipo_servicio = self.ui.txt_nombre_tipo_servicio.text()
            nuevo_categoria_tipo_servicio = self.ui.txt_nombre_categoria_asociada.text()
            
            self._servicios["tipo_servicio_tecnico_servicio"].actualizar(
                tipo_servicio_id,
                nuevo_categoria_tipo_servicio,
                nuevo_nombre_tipo_servicio.upper()
            )
            
            QMessageBox.information(self.ui, "Éxito", "La información del tipo de servicio se ha actualizado correctamente.")
            self.cargar_completer_tipos_servicio()
            self.ui.accept()
        except NoEncontradoError as error:
            QMessageBox.critical(self.ui, "Error", "\n".join(error.errores))
        except ValidacionError as error:
            QMessageBox.critical(self.ui, "Error", "\n".join(error.errores))
        except LogicaError as error:
            QMessageBox.critical(self.ui, "Error", "\n".join(error.errores))
    
    def eliminar_tipo_servicio(self):
        mensaje_confirmacion = QMessageBox.question(
            self.ui,
            "Confirmar eliminación",
            "¿Estás seguro de que quieres eliminar este tipo de servicio?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if (mensaje_confirmacion == QMessageBox.Yes):
            try:
                tipo_servicio_id = self.tipo_servicio_data[0]
                self._servicios["tipo_servicio_tecnico_servicio"].eliminar(tipo_servicio_id)
                
                QMessageBox.information(self.ui, "Éxito", "Se ha eliminado el tipo de servicio correctamente.")
                self.cargar_completer_tipos_servicio()
                self.ui.accept()
            except NoEncontradoError as error:
                QMessageBox.critical(self.ui, "Error", "\n".join(error.errores))
            except ValidacionError as error:
                QMessageBox.critical(self.ui, "Error", "\n".join(error.errores))
            except LogicaError as error:
                QMessageBox.critical(self.ui, "Error", "\n".join(error.errores))