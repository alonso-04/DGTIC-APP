from typing import List, Tuple
from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import QHeaderView, QDialog
from PyQt5.QtGui import QStandardItemModel

from utilidades.gui import UiBase
from vistas.vistas_python.VentanaPrincipal import VentanaPrincipal
from vistas.utilidades_gui.cargar_completers import cargar_completer
from vistas.utilidades_gui.registrar import registrar_campos
from vistas.utilidades_gui.limpiar_campos import limpiar_campos
from vistas.utilidades_gui.filtrar import obtener_modelo_datos_y_data
from configuraciones.excepciones import ValidacionError, NoEncontradoError, LogicaError


class VentanaDepartamentos(UiBase):
    def __init__(self, ventana_principal: VentanaPrincipal):
        super().__init__()
        self.ventana_principal = ventana_principal
        self.ui = ventana_principal.ui
        
        
        # SERVICIOS
        self._servicios = self.ventana_principal._servicios
        
        
        # SECCIÓN DE LA TABLA DEPARTAMENTOS
        self.departamento_data = []
        
        
        # FUNCIONES Y ELEMENTOS DE UTILIDAD
        self.mostrar_mensaje_error = self.ventana_principal.mostrar_mensaje_error
        
        lista_campos_departamento_completers = [
            self.ui.txt_filtrar_departamentos_registrados,
            self.ui.txt_filtro_nombre_departamento,
            self.ui.txt_nombre_departamento
        ]
        
        self.cargar_completer_departamento = lambda: cargar_completer(
            self._servicios["departamento_servicio"],
            lista_campos_departamento_completers,
            "departamento"
        )
        
        self.cargar_manual_usuario = self.ventana_principal.ver_manual_usuario
        
        self.configuracion()
    
    def configuracion(self):
        self.filtrar_departamentos()
        self.ui.btn_refrescar_pagina_ventana_departamentos.clicked.connect(self.refrescar_pagina_departamentos)
        self.ui.btn_manual_usuario_ventana_departamento.clicked.connect(self.ver_manual_usuario)
        self.ui.btn_regresar_ventana_departamento.clicked.connect(self.ir_pagina_app)
        self.ui.btn_buscar_departamentos.clicked.connect(self.filtrar_departamentos)
        self.ui.btn_registrar_departamento.clicked.connect(self.registrar_departamento)
        
        self.ui.tabla_departamentos.clicked.connect(self.seleccionar_departamento)
        self.configurar_tabla(self.ui.tabla_departamentos)
    
    def refrescar_pagina_departamentos(self):
        self.filtrar_departamentos()
        self.cargar_completer_departamento()
    
    def ver_manual_usuario(self):
        self.cargar_manual_usuario()
    
    def ir_pagina_app(self):
        self.ui.ventanas.setCurrentWidget(self.ui.paginaApp)
        self.ui.setWindowTitle("App")
        self.ui.de_filtro_fecha_servicio.setDate(QDate.currentDate())
        self.ui.de_fecha_servicio.setDate(QDate.currentDate())
    
    def registrar_departamento(self):
        try:
            campos_a_registrar = [(self.ui.txt_registrar_departamento, "nombre_departamento")]
            registrar_campos(self._servicios["departamento_servicio"], campos_a_registrar)
            limpiar_campos([self.ui.txt_registrar_departamento])
            
            self.refrescar_pagina_departamentos()
        except ValidacionError as error:
            self.mostrar_mensaje_error("\n".join(error.errores))
        except LogicaError as error:
            self.mostrar_mensaje_error("\n".join(error.errores))
    
    def filtrar_departamentos(self):
        try:
            lista_campos_filtrar = [(self.ui.txt_filtrar_departamentos_registrados, "nombre_departamento")]
            nombres_labels = ["Nombre del departamento"]
            nombres_columnas = ["nombre_departamento"]
            
            modelo_datos, registros = obtener_modelo_datos_y_data(
                self._servicios["departamento_servicio"].obtener_por_nombre_o_todos,
                nombres_labels,
                nombres_columnas,
                lista_campos_filtrar
            )
            
            self.departamento_data = registros
            self.ui.tabla_departamentos.setModel(modelo_datos)
            self.ui.lbl_errores_filtro_departamentos.clear()
            
            header = self.ui.tabla_departamentos.horizontalHeader()
            header.setSectionResizeMode(QHeaderView.Stretch)
        except NoEncontradoError as error:
            self.limpiar_tabla("\n".join(error.errores))
            self.departamento_data = []
            header = self.ui.tabla_departamentos.horizontalHeader()
            header.setSectionResizeMode(QHeaderView.Stretch)
    
    def seleccionar_departamento(self, indice: int):
        fila_seleccionada = indice.row()
        
        if ((fila_seleccionada >= 0) and (fila_seleccionada < len(self.departamento_data))):
            departamento_seleccionado = self.departamento_data[fila_seleccionada]
            self.mostrar_ventana_info_departamento(departamento_seleccionado)
    
    def mostrar_ventana_info_departamento(self, departamento_data: List[Tuple]):
        if not(hasattr(self, "ventana_info_departamento")):
            from vistas.vistas_python.VentanaInfoDepartamento import VentanaInfoDepartamento
            self.ventana_info_departamento = VentanaInfoDepartamento(
                departamento_data,
                self.ventana_principal,
                "VentanaInfoDepartamento.ui",
                "estilos_ventanas_info.qss"
            )
        
        self.ventana_info_departamento.actualizar_data_recibida(departamento_data)
        
        resultado = self.ventana_info_departamento.ui.exec_()
        if (resultado == QDialog.Accepted):
            self.filtrar_departamentos()
    
    def mostrar_error_filtro(self, mensaje: str):
        self.ui.lbl_errores_filtro_departamentos.setText(mensaje)
    
    def limpiar_tabla(self, mensaje: str = ""):
        modelo_vacio = QStandardItemModel(0, 1)
        modelo_vacio.setHorizontalHeaderLabels([
            "Nombre del departamento"
        ])
        
        self.ui.tabla_departamentos.setModel(modelo_vacio)
        
        if (mensaje):
            self.ui.lbl_errores_filtro_departamentos.setText(mensaje)