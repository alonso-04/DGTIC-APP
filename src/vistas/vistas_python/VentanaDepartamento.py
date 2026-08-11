from typing import List, Tuple
from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import QHeaderView, QDialog
from PyQt5.QtGui import QStandardItemModel

from vistas.vistas_python.VentanaPrincipal import VentanaPrincipal
from vistas.utilidades_gui.cargar_completers import cargar_completer
from vistas.utilidades_gui.registrar import registrar_campos
from vistas.utilidades_gui.limpiar_campos import limpiar_campos
from vistas.utilidades_gui.filtrar import obtener_modelo_datos_y_data
from configuraciones.excepciones import ValidacionError, NoEncontradoError, LogicaError


class VentanaDepartamentos:
    def __init__(self, ventana_principal: VentanaPrincipal):
        super().__init__()
        self.ventana_principal = ventana_principal
        
        
        # SERVICIOS
        self._servicios = self.ventana_principal._servicios
        
        # SECCIÓN DE REGISTRAR DEPARTAMENTO
        self.inputNombreDepartamento = self.ventana_principal.inputNombreDepartamento
        self.botonRegistrarDepartamento = self.ventana_principal.botonRegistrarDepartamento
        
        
        # SECCIÓN DE FILTRAR DEPARTAMENTOS
        self.inputBuscarDepartamento = self.ventana_principal.inputBuscarDepartamento
        self.botonBuscarDepartamento = self.ventana_principal.botonBuscarDepartamento
        self.labelFiltroSeccionDepartamento = self.ventana_principal.labelFiltroSeccionDepartamento
        
        
        # SECCIÓN DE LA TABLA DEPARTAMENTOS
        self.tvDepartamentos = self.ventana_principal.tvDepartamentos
        self.departamento_data = []
        
        
        # FUNCIONES Y ELEMENTOS DE UTILIDAD
        self.mostrar_mensaje_error = self.ventana_principal.mostrar_mensaje_error
        
        lista_campos_departamento_completers = [
            self.ventana_principal.inputDepartamento, 
            self.ventana_principal.inputFiltroDepartamento,
            self.inputBuscarDepartamento
        ]
        
        self.cargar_completer_departamento = lambda: cargar_completer(
            self._servicios["departamento_servicio"],
            lista_campos_departamento_completers,
            "departamento"
        )
        
        self.cargar_manual_usuario = self.ventana_principal.ver_manual_usuario
        self.botonRefrescarDepartamentos = self.ventana_principal.botonRefrescarDepartamentos
        self.botonManualUsuarioSeccionDepartamentos = self.ventana_principal.botonManualUsuarioSeccionDepartamentos
        
        
        # BOTONES INFERIORES
        self.botonRegresarSeccionDepartamentos = self.ventana_principal.botonRegresarSeccionDepartamentos
        
        self.configuracion()
    
    def configuracion(self):
        self.filtrar_departamentos()
        self.botonRefrescarDepartamentos.clicked.connect(self.refrescar_pagina_departamentos)
        self.botonManualUsuarioSeccionDepartamentos.clicked.connect(self.ver_manual_usuario)
        self.botonRegresarSeccionDepartamentos.clicked.connect(self.ir_pagina_app)
        self.botonBuscarDepartamento.clicked.connect(self.filtrar_departamentos)
        self.botonRegistrarDepartamento.clicked.connect(self.registrar_departamento)
        self.tvDepartamentos.clicked.connect(self.seleccionar_departamento)
    
    def refrescar_pagina_departamentos(self):
        self.filtrar_departamentos()
        self.cargar_completer_departamento()
    
    def ver_manual_usuario(self):
        self.cargar_manual_usuario()
    
    def ir_pagina_app(self):
        self.ventana_principal.ventanas.setCurrentWidget(self.ventana_principal.paginaApp)
        self.ventana_principal.setWindowTitle("App")
        self.ventana_principal.deFiltroFecha.setDate(QDate.currentDate())
        self.ventana_principal.deFecha.setDate(QDate.currentDate())
        self.inputBuscarDepartamento.clear()
    
    def registrar_departamento(self):
        try:
            campos_a_registrar = [(self.inputNombreDepartamento, "nombre_departamento")]
            registrar_campos(self._servicios["departamento_servicio"], campos_a_registrar)
            limpiar_campos([self.inputNombreDepartamento])
            
            self.refrescar_pagina_departamentos()
        except ValidacionError as error:
            self.mostrar_mensaje_error("\n".join(error.errores))
        except LogicaError as error:
            self.mostrar_mensaje_error("\n".join(error.errores))
    
    def filtrar_departamentos(self):
        try:
            lista_campos_filtrar = [(self.inputBuscarDepartamento, "nombre_departamento")]
            nombres_labels = ["Nombre del departamento"]
            nombres_columnas = ["nombre_departamento"]
            
            modelo_datos, registros = obtener_modelo_datos_y_data(
                self._servicios["departamento_servicio"].obtener_por_nombre_o_todos,
                lista_campos_filtrar,
                nombres_labels,
                nombres_columnas
            )
            
            self.departamento_data = registros
            self.tvDepartamentos.setModel(modelo_datos)
            self.labelFiltroSeccionDepartamento.clear()
            
            header = self.tvDepartamentos.horizontalHeader()
            header.setSectionResizeMode(QHeaderView.Stretch)
        except NoEncontradoError as error:
            self.limpiar_tabla("\n".join(error.errores))
            self.departamento_data = []
            header = self.tvDepartamentos.horizontalHeader()
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
                departamento_data = departamento_data,
                ventana_principal = self.ventana_principal
            )
        
        self.ventana_info_departamento.actualizar_data_recibida(departamento_data)
        
        resultado = self.ventana_info_departamento.exec_()
        if (resultado == QDialog.Accepted):
            self.filtrar_departamentos()
    
    def mostrar_error_filtro(self, mensaje: str):
        self.labelFiltroSeccionDepartamento.setText(mensaje)
    
    def limpiar_tabla(self, mensaje: str = ""):
        modelo_vacio = QStandardItemModel(0, 1)
        modelo_vacio.setHorizontalHeaderLabels([
            "Nombre del departamento"
        ])
        
        self.tvDepartamentos.setModel(modelo_vacio)
        
        if (mensaje):
            self.labelFiltroSeccionDepartamento.setText(mensaje)