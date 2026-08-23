import os
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QMessageBox, QTableView, QAbstractItemView, QHBoxLayout
from PyQt5.QtGui import QIcon

from configuraciones.rutas import RUTA_BASE, obtener_ruta_icono_app
from componentes.boton_acciones import BotonAcciones


class UiBase:
    def __init__(self, nombre_archivo_ui: str = None, nombre_archivo_estilos: str = None):
        self.ui = self._cargar_ui(nombre_archivo_ui)
        self.cargar_estilos(nombre_archivo_estilos)
    
    def abrir(self):
        self.ui.show()
    
    def _cargar_ui(self, nombre_archivo_ui: str):
        try:
            if not nombre_archivo_ui:
                return
            
            ruta_ui = os.path.abspath(os.path.join(RUTA_BASE, "vistas", "vistas_qt", nombre_archivo_ui))
            ui_cargada = uic.loadUi(ruta_ui, None)
            return ui_cargada
        except FileNotFoundError:
            self.mostrar_error(f"Error: No se encontró el archivo: {ruta_ui}")
            sys.exit(1)
    
    def _cargar_icono_app(self):
        ruta_icono_app = obtener_ruta_icono_app()
        self.ui.setWindowIcon(QIcon(ruta_icono_app))
    
    def cargar_estilos(self, nombre_archivo_estilos: str, pagina_stacked_widget: object = None):
        try:
            if not nombre_archivo_estilos:
                return
            
            ruta_estilos = os.path.abspath(os.path.join(RUTA_BASE, "recursos", "estilos", nombre_archivo_estilos))
            
            with open(ruta_estilos, "r", encoding="utf-8") as archivo:
                if not pagina_stacked_widget:
                    self.ui.setStyleSheet(archivo.read())
                else:
                    pagina_stacked_widget.setStyleSheet(archivo.read())
            
            ruta_icono_app = obtener_ruta_icono_app()
            self.ui.setWindowIcon(QIcon(ruta_icono_app))
        except FileNotFoundError:
            self.mostrar_error(f"Error: No se encontró el archivo: {ruta_estilos}")
            sys.exit(1)
    
    def cargar_botones(self):
        ruta_estilos_boton = os.path.abspath(os.path.join(RUTA_BASE, "recursos", "estilos", "estilos_botones_acciones.qss"))
        
        self.btn_actualizar = BotonAcciones("Actualizar", "actualizar", ruta_estilos_boton)
        self.btn_eliminar = BotonAcciones("Eliminar", "eliminar", ruta_estilos_boton)
        self.btn_cancelar = BotonAcciones("Cancelar", "cancelar", ruta_estilos_boton)
        
        layout_botones = QHBoxLayout()
        
        layout_botones.addWidget(self.btn_actualizar)
        layout_botones.addWidget(self.btn_eliminar)
        layout_botones.addWidget(self.btn_cancelar)
        
        self.ui.layout_principal.addLayout(layout_botones)
    
    def configurar_tabla(self, tabla: QTableView):
        # SELECCIÓN DE FILA COMPLETA E INDIVIDUAL
        tabla.setSelectionBehavior(self.ui.tabla_servicios.SelectRows)
        tabla.setSelectionMode(self.ui.tabla_servicios.SingleSelection)
        
        # DESACTIVAR LA EDICIÓN DE CELDAS AL HACER DOBLE CLICK
        tabla.setEditTriggers(QAbstractItemView.NoEditTriggers)
        
        # OCULTAR LOS NÚMEROS DE FILA DE LA TABLA
        cabecera_vertical = tabla.verticalHeader()
        cabecera_vertical.setVisible(False)
    
    def mostrar_error(self, mensaje: str):
        QMessageBox.critical(None, "Error", mensaje)