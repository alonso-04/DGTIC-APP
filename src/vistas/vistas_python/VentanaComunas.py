from typing import Tuple
from PyQt5.QtWidgets import QHeaderView, QDialog
from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtCore import QDate

from utilidades.gui import UiBase, cargar_completer, registrar_campos, limpiar_campos, obtener_modelo_datos_y_data
from vistas.vistas_python.VentanaPrincipal import VentanaPrincipal
from configuraciones.excepciones import NoEncontradoError, ValidacionError, LogicaError


class VentanaComunas(UiBase):
    def __init__(self, ventana_principal: VentanaPrincipal):
        super().__init__()
        self.ventana_principal = ventana_principal
        self.ui = ventana_principal.ui
        self._servicios = self.ventana_principal._servicios
        
        
        # DATA DE LAS COMUNAS
        self.comuna_data = []
        
        
        # LISTA Y MÉTODOS DE LOS COMPLETERS
        lista_campos_comuna_completers = [
            self.ui.txt_nombre_comuna,
            self.ui.txt_filtro_comunas_registradas
        ]
        
        self.cargar_completer_comunas = lambda: cargar_completer(
            self._servicios["comuna_servicio"],
            lista_campos_comuna_completers,
            "categoria"
        )
        
        
        self.configuracion()
    
    def configuracion(self):
        self.filtrar_comunas()
        self.cargar_completer_comunas()
        
        self.ui.btn_refrescar_pagina_ventana_comunas.clicked.connect(self.refrescar_pagina_comunas)
        self.ui.btn_manual_usuario_ventana_comuna.clicked.connect(self.ver_manual_usuario)
        self.ui.btn_regresar_ventana_comuna.clicked.connect(self.ir_pagina_app)
        self.ui.btn_buscar_comunas.clicked.connect(self.filtrar_comunas)
        self.ui.btn_registrar_comuna.clicked.connect(self.registrar_comuna)
        
        self.ui.tabla_comunas.clicked.connect(self.seleccionar_comuna)
        self.configurar_tabla(self.ui.tabla_comunas)
    
    def refrescar_pagina_comunas(self):
        self.filtrar_comunas()
        self.cargar_completer_comunas()
    
    def ir_pagina_app(self):
        self.ui.ventanas.setCurrentWidget(self.ui.paginaApp)
        self.ui.setWindowTitle("App")
        self.ui.de_filtro_fecha_servicio.setDate(QDate.currentDate())
        self.ui.de_fecha_servicio.setDate(QDate.currentDate())
    
    def registrar_comuna(self):
        try:
            campos_a_registrar = [(self.ui.txt_registrar_comuna, "nombre_comuna")]
            registrar_campos(self._servicios["comuna_servicio"], campos_a_registrar, "comuna")
            limpiar_campos([self.ui.txt_registrar_comuna])
            
            self.refrescar_pagina_comunas()
        except ValidacionError as error:
            self.mostrar_mensaje_error("\n".join(error.errores))
        except LogicaError as error:
            self.mostrar_mensaje_error("\n".join(error.errores))
    
    def filtrar_comunas(self):
        try:
            lista_campos_filtrar = [(self.ui.txt_filtro_comunas_registradas, "nombre_comuna")]
            nombres_labels = ["Nombre de la comuna"]
            nombres_columnas = ["nombre_comuna"]
            
            modelo_datos, registros = obtener_modelo_datos_y_data(
                self._servicios["comuna_servicio"].obtener_por_comuna_o_todos,
                nombres_labels,
                nombres_columnas,
                lista_campos_filtrar
            )
            
            self.comuna_data = registros
            self.ui.tabla_comunas.setModel(modelo_datos)
            self.ui.lbl_errores_filtro_comunas.clear()
            
            header = self.ui.tabla_comunas.horizontalHeader()
            header.setSectionResizeMode(QHeaderView.Stretch)
        except NoEncontradoError as error:
            self.limpiar_tabla("\n".join(error.errores))
            self.comuna_data = []
            header = self.ui.tabla_comunas.horizontalHeader()
            header.setSectionResizeMode(QHeaderView.Stretch)
    
    def seleccionar_comuna(self, indice: int):
        fila_seleccionada = indice.row()
        
        if ((fila_seleccionada >= 0) and (fila_seleccionada < len(self.comuna_data))):
            comuna_seleccionada = self.comuna_data[fila_seleccionada]
            self.mostrar_ventana_info_comuna(comuna_seleccionada)
    
    def mostrar_ventana_info_comuna(self, comuna_data: Tuple):
        if not(hasattr(self, "ventana_info_categoria")):
            from vistas.vistas_python.VentanaInfoComuna import VentanaInfoComuna
            self.ventana_info_comuna = VentanaInfoComuna(
                comuna_data,
                self.ventana_principal,
                "VentanaInfoComuna.ui",
                "estilos_ventanas_info.qss"
            )
        
        self.ventana_info_comuna.actualizar_data_recibida(comuna_data)
        resultado = self.ventana_info_comuna.ui.exec_()
            
        if (resultado == QDialog.Accepted):
            self.filtrar_comunas()
    
    def mostrar_error_filtro(self, mensaje: str):
        self.ui.lbl_errores_filtro_comunas.setText(mensaje)
    
    def limpiar_tabla(self, mensaje: str = ""):
        modelo_vacio = QStandardItemModel(0, 1)
        modelo_vacio.setHorizontalHeaderLabels([
            "Nombre de la comuna"
        ])
        
        self.ui.tabla_comunas.setModel(modelo_vacio)
        
        if (mensaje):
            self.ui.lbl_errores_filtro_comunas.setText(mensaje)