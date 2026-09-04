from typing import Tuple
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import Qt

from utilidades.gui import UiBase, cargar_completer
from vistas.vistas_python.VentanaPrincipal import VentanaPrincipal
from configuraciones.excepciones import ValidacionError, NoEncontradoError, LogicaError


class VentanaInfoCategoria(UiBase):
    def __init__(self, categoria_data: Tuple, ventana_principal: VentanaPrincipal, nombre_archivo_ui: str, nombre_archivo_estilos: str):
        super().__init__(nombre_archivo_ui, nombre_archivo_estilos)
        
        self.ui.setWindowFlags(
            Qt.WindowSystemMenuHint |
            Qt.WindowTitleHint |
            Qt.WindowCloseButtonHint
        )
        
        self.categoria_data = categoria_data
        self.ventana_principal = ventana_principal.ui
        self._servicios = ventana_principal._servicios
        
        
        # LISTA Y MÉTODOS DE LOS COMPLETERS
        lista_completers_categorias = [
            self.ventana_principal.txt_categoria_asociada,
            self.ventana_principal.txt_filtro_por_categoria,
            self.ventana_principal.txt_filtro_categorias_registradas
        ]
        
        self.cargar_completer_categorias = lambda: cargar_completer(
            self._servicios["categoria_tipo_servicio_tecnico_servicio"],
            lista_completers_categorias,
            "categoria"
        )
        
        
        self.filtrar_tipos_servicio = ventana_principal.ui.btn_buscar_tipos_servicio.click
        
        
        self.cargar_botones()
        self.configuracion()
    
    def configuracion(self):
        self.cargar_completer_categorias()
        
        self.btn_actualizar.clicked.connect(self.actualizar_info_categoria)
        self.btn_eliminar.clicked.connect(self.eliminar_categoria)
        self.btn_cancelar.clicked.connect(self.ui.reject)
    
    def actualizar_data_recibida(self, data_recibida: Tuple):
        self.categoria_data = data_recibida
        self.cargar_datos()
    
    def cargar_datos(self):
        self.ui.txt_nombre_categoria.setText(self.categoria_data[1])
    
    def actualizar_info_categoria(self):
        try:
            categoria_tipo_servicio_id = self.categoria_data[0]
            nuevo_nombre_categoria = self.ui.txt_nombre_categoria.text()
            
            self._servicios["categoria_tipo_servicio_tecnico_servicio"].actualizar(
                categoria_tipo_servicio_id,
                nuevo_nombre_categoria.upper()
            )

            self.mostrar_mensaje_info("La información de la categoría se ha actualizado correctamente.")
            self.cargar_completer_categorias()
            self.filtrar_tipos_servicio()
            self.ui.accept()
        except NoEncontradoError as error:
            self.mostrar_mensaje_error("\n".join(error.errores))
        except ValidacionError as error:
            self.mostrar_mensaje_error("\n".join(error.errores))
        except LogicaError as error:
            self.mostrar_mensaje_error("\n".join(error.errores))
    
    def eliminar_categoria(self):
        mensaje_confirmacion = QMessageBox.question(
            self.ui,
            "Confirmar eliminación",
            "¿Estás seguro de que quieres eliminar esta categoría?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if (mensaje_confirmacion == QMessageBox.Yes):
            try:
                categoria_tipo_servicio_id = self.categoria_data[0]
                self._servicios["categoria_tipo_servicio_tecnico_servicio"].eliminar(categoria_tipo_servicio_id)
                
                self.mostrar_mensaje_info("Se ha eliminado la categoría correctamente.")
                self.cargar_completer_categorias()
                self.ui.accept()
            except NoEncontradoError as error:
                self.mostrar_mensaje_error("\n".join(error.errores))
            except ValidacionError as error:
                self.mostrar_mensaje_error("\n".join(error.errores))
            except LogicaError as error:
                self.mostrar_mensaje_error("\n".join(error.errores))