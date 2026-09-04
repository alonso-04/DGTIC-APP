from typing import Tuple
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import Qt

from utilidades.gui import UiBase, cargar_completer
from vistas.vistas_python.VentanaPrincipal import VentanaPrincipal
from configuraciones.excepciones import ValidacionError, NoEncontradoError, LogicaError


class VentanaInfoDepartamento(UiBase):
    def __init__(self, departamento_data: Tuple, ventana_principal: VentanaPrincipal, nombre_archivo_ui: str, nombre_archivo_estilos: str):
        super().__init__(nombre_archivo_ui, nombre_archivo_estilos)
        
        self.ui.setWindowFlags(
            Qt.WindowSystemMenuHint |
            Qt.WindowTitleHint |
            Qt.WindowCloseButtonHint
        )
        
        self.departamento_data = departamento_data
        self._servicios = ventana_principal._servicios
        self.ventana_principal = ventana_principal.ui
        
        
        # LISTA Y MÉTODOS DE LOS COMPLETERS
        lista_campos_departamento_completers = [
            self.ventana_principal.txt_nombre_departamento,
            self.ventana_principal.txt_filtro_nombre_departamento,
            self.ventana_principal.txt_filtrar_departamentos_registrados,
        ]
        
        self.cargar_completer_departamento = lambda: cargar_completer(
            self._servicios["departamento_servicio"],
            lista_campos_departamento_completers,
            "departamento"
        )
        
        
        self.cargar_botones()
        self.configuracion()
    
    def configuracion(self):
        self.cargar_completer_departamento()
        
        self.btn_actualizar.clicked.connect(self.actualizar_info_departamento)
        self.btn_eliminar.clicked.connect(self.eliminar_departamento)
        self.btn_cancelar.clicked.connect(self.ui.reject)
    
    def actualizar_data_recibida(self, data_recibida: Tuple):
        self.departamento_data = data_recibida
        self.cargar_datos()
    
    def cargar_datos(self):
        self.ui.txt_nombre_departamento.setText(self.departamento_data[1])
    
    def actualizar_info_departamento(self):
        try:
            departamento_id = self.departamento_data[0]
            nuevo_nombre_departamento = self.ui.txt_nombre_departamento.text()
            
            self._servicios["departamento_servicio"].actualizar(
                departamento_id,
                nuevo_nombre_departamento.upper()
            )
            
            self.mostrar_mensaje_info("La información del departamento se ha actualizado correctamente.")
            self.cargar_completer_departamento()
            self.ui.accept()
        except NoEncontradoError as error:
            self.mostrar_mensaje_error("\n".join(error.errores))
        except ValidacionError as error:
            self.mostrar_mensaje_error("\n".join(error.errores))
        except LogicaError as error:
            self.mostrar_mensaje_error("\n".join(error.errores))
    
    def eliminar_departamento(self):
        mensaje_confirmacion = QMessageBox.question(
            self.ui,
            "Confirmar eliminación",
            "¿Estás seguro de que quieres eliminar este departamento?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if (mensaje_confirmacion == QMessageBox.Yes):
            try:
                departamento_id = self.departamento_data[0]
                self._servicios["departamento_servicio"].eliminar(departamento_id)
                
                self.mostrar_mensaje_info("Se ha eliminado el departamento correctamente.")
                self.cargar_completer_departamento()
                self.ui.accept()
            except NoEncontradoError as error:
                self.mostrar_mensaje_error("\n".join(error.errores))
            except ValidacionError as error:
                self.mostrar_mensaje_error("\n".join(error.errores))
            except LogicaError as error:
                self.mostrar_mensaje_error("\n".join(error.errores))