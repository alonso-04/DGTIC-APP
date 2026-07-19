from typing import Tuple
from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5.QtCore import Qt

from vistas.vistas_pyuic.VentanaInfoCategoriaPyuic import Ui_VentanaInfoCategoria
from vistas.vistas_python.VentanaPrincipal import VentanaPrincipal
from configuraciones.excepciones import ValidacionError, NoEncontradoError, LogicaError


class VentanaInfoCategoria(QDialog, Ui_VentanaInfoCategoria):
    def __init__(self, categoria_data: Tuple, ventana_principal: VentanaPrincipal):
        super().__init__()
        self.setupUi(self)
        
        self.setWindowFlags(
            Qt.WindowSystemMenuHint |
            Qt.WindowTitleHint |
            Qt.WindowCloseButtonHint
        )
        
        self.categoria_data = categoria_data
        self.ventana_principal = ventana_principal
        self._servicios = self.ventana_principal._servicios
        
        self.cargar_completer_categorias = self.ventana_principal.cargar_completer_categorias
        self.filtrar_tipos_servicio = self.ventana_principal.botonBuscarTipoServicio.click
        
        self.configuracion()
    
    def configuracion(self):
        self.cargar_completer_categorias()
        
        self.botonAcualizarInfoCategoria.clicked.connect(self.actualizar_info_categoria)
        self.botonEliminarCategoria.clicked.connect(self.eliminar_categoria)
        self.botonCancelarInfoCategoria.clicked.connect(self.reject)
    
    def actualizar_data_recibida(self, data_recibida: Tuple):
        self.categoria_data = data_recibida
        self.cargar_datos()
    
    def cargar_datos(self):
        self.inputInfoNombreCategoria.setText(self.categoria_data[1])
    
    def actualizar_info_categoria(self):
        try:
            categoria_tipo_servicio_id = self.categoria_data[0]
            nuevo_nombre_categoria = self.inputInfoNombreCategoria.text()
            
            self._servicios["categoria_tipo_servicio_tecnico_servicio"].actualizar(
                categoria_tipo_servicio_id,
                nuevo_nombre_categoria.upper()
            )
            
            QMessageBox.information(self, "Éxito", "La información del tipo de servicio se ha actualizado correctamente.")
            self.cargar_completer_categorias()
            self.filtrar_tipos_servicio()
            self.accept()
        except NoEncontradoError as error:
            QMessageBox.critical(self, "Error", "\n".join(error.errores))
        except ValidacionError as error:
            QMessageBox.critical(self, "Error", "\n".join(error.errores))
        except LogicaError as error:
            QMessageBox.critical(self, "Error", "\n".join(error.errores))
    
    def eliminar_categoria(self):
        mensaje_confirmacion = QMessageBox.question(
            self,
            "Confirmar eliminación",
            "¿Estás seguro de que quieres eliminar esta categoría?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if (mensaje_confirmacion == QMessageBox.Yes):
            try:
                categoria_tipo_servicio_id = self.categoria_data[0]
                self._servicios["categoria_tipo_servicio_tecnico_servicio"].eliminar(categoria_tipo_servicio_id)
                
                QMessageBox.information(self, "Éxito", "Se ha eliminado la categoría correctamente.")
                self.cargar_completer_categorias()
                self.accept()
            except NoEncontradoError as error:
                QMessageBox.critical(self, "Error", "\n".join(error.errores))
            except ValidacionError as error:
                QMessageBox.critical(self, "Error", "\n".join(error.errores))
            except LogicaError as error:
                QMessageBox.critical(self, "Error", "\n".join(error.errores))