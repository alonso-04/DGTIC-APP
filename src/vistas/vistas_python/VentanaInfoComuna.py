from typing import Tuple
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import Qt

from utilidades.gui import UiBase
from vistas.vistas_python.VentanaPrincipal import VentanaPrincipal
from vistas.utilidades_gui.cargar_completers import cargar_completer
from configuraciones.excepciones import ValidacionError, NoEncontradoError, LogicaError


class VentanaInfoComuna(UiBase):
    def __init__(self, comuna_data: Tuple, ventana_principal: VentanaPrincipal, nombre_archivo_ui: str, nombre_archivo_estilos: str):
        super().__init__(nombre_archivo_ui, nombre_archivo_estilos)
        
        self.ui.setWindowFlags(
            Qt.WindowSystemMenuHint |
            Qt.WindowTitleHint |
            Qt.WindowCloseButtonHint
        )
        
        self.comuna_data = comuna_data
        self._servicios = ventana_principal._servicios
        self.ventana_principal = ventana_principal.ui
        
        lista_campos_comuna_completers = [
            self.ventana_principal.txt_nombre_comuna,
            self.ventana_principal.txt_filtro_comunas_registradas
        ]
        
        self.cargar_completer_comunas = lambda: cargar_completer(
            self._servicios["comuna_servicio"],
            lista_campos_comuna_completers,
            "comuna"
        )
        
        self.cargar_botones()
        self.configuracion()
    
    def configuracion(self):
        self.btn_actualizar.clicked.connect(self.actualizar_info_comuna)
        self.btn_eliminar.clicked.connect(self.eliminar_comuna)
        self.btn_cancelar.clicked.connect(self.ui.reject)
    
    def actualizar_data_recibida(self, data_recibida: Tuple):
        self.comuna_data = data_recibida
        self.cargar_datos()
    
    def cargar_datos(self):
        self.ui.txt_nombre_comuna.setText(self.comuna_data[1])
    
    def actualizar_info_comuna(self):
        try:
            comuna_id = self.comuna_data[0]
            nuevo_nombre_comuna = self.ui.txt_nombre_comuna.text()
            
            self._servicios["comuna_servicio"].actualizar(
                comuna_id,
                nuevo_nombre_comuna.upper()
            )
            
            QMessageBox.information(self.ui, "Éxito", "La información de la comuna se ha actualizado correctamente.")
            self.cargar_completer_comunas()
            self.ui.accept()
        except NoEncontradoError as error:
            QMessageBox.critical(self.ui, "Error", "\n".join(error.errores))
        except ValidacionError as error:
            QMessageBox.critical(self.ui, "Error", "\n".join(error.errores))
        except LogicaError as error:
            QMessageBox.critical(self.ui, "Error", "\n".join(error.errores))
    
    def eliminar_comuna(self):
        mensaje_confirmacion = QMessageBox.question(
            self.ui,
            "Confirmar eliminación",
            "¿Estás seguro de que quieres eliminar esta comuna?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if (mensaje_confirmacion == QMessageBox.Yes):
            try:
                comuna_id = self.comuna_data[0]
                self._servicios["comuna_servicio"].eliminar(comuna_id)
                
                QMessageBox.information(self.ui, "Éxito", "Se ha eliminado la comuna correctamente.")
                self.cargar_completer_comunas()
                self.ui.accept()
            except NoEncontradoError as error:
                QMessageBox.critical(self.ui, "Error", "\n".join(error.errores))
            except ValidacionError as error:
                QMessageBox.critical(self.ui, "Error", "\n".join(error.errores))
            except LogicaError as error:
                QMessageBox.critical(self.ui, "Error", "\n".join(error.errores))