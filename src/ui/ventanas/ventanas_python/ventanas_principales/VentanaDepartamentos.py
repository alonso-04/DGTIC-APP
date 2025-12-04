from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import QHeaderView, QDialog
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from typing import Dict
from dominio.excepciones import DepartamentoValidacionError
from ui.ventanas.ventanas_python.ventanas_principales.VentanaPrincipal import VentanaPrincipal
from ui.ventanas.ventanas_python.ventanas_info.VentanaInfoDepartamento import VentanaInfoDepartamento


class VentanaDepartamentos:
    def __init__(self, ventana_principal: VentanaPrincipal):
        super().__init__()
        self.ventana_principal = ventana_principal
        
        # FUNCIONES Y ELEMENTOS DE UTILIDAD
        self.esta_vacio = self.ventana_principal.esta_vacio
        self.mostrar_mensaje_error = self.ventana_principal.mostrar_mensaje_error
        self.cargar_completer_departamento = self.ventana_principal.cargar_completer_departamento
        self.botonRefrescarDepartamentos = self.ventana_principal.botonRefrescarDepartamentos
        
        # CONTROLADORES
        self.servicio_controlador = self.ventana_principal.servicio_controlador
        
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
        
        
        # BOTONES INFERIORES
        self.botonRegresarSeccionDepartamentos = self.ventana_principal.botonRegresarSeccionDepartamentos
        
        self.configuracion()
    
    def configuracion(self):
        self.botonRefrescarDepartamentos.clicked.connect(self.refrescar_pagina_departamentos)
        self.botonRegresarSeccionDepartamentos.clicked.connect(self.ir_pagina_app)
        self.botonBuscarDepartamento.clicked.connect(self.filtrar_departamentos)
        self.botonRegistrarDepartamento.clicked.connect(self.registrar_departamento)
        self.tvDepartamentos.clicked.connect(self.seleccionar_departamento)
    
    def refrescar_pagina_departamentos(self):
        self.filtrar_departamentos()
        self.cargar_completer_departamento()
    
    def ir_pagina_app(self):
        self.ventana_principal.ventanas.setCurrentWidget(self.ventana_principal.paginaApp)
        self.ventana_principal.setWindowTitle("App")
        self.ventana_principal.deFiltroFecha.setDate(QDate.currentDate())
        self.ventana_principal.deFecha.setDate(QDate.currentDate())
        self.inputBuscarDepartamento.clear()
    
    def registrar_departamento(self):
        try:
            nombre_departamento = self.inputNombreDepartamento.text()
            
            if (self.esta_vacio(nombre_departamento)):
                nombre_departamento = None
            
            self.servicio_controlador.registrar_departamento_controlador(
                nombre_departamento
            )
            
            self.inputNombreDepartamento.clear()
            self.filtrar_departamentos()
            self.cargar_completer_departamento()
        except DepartamentoValidacionError as error:
            self.mostrar_mensaje_error("\n".join(error.errores))
    
    def filtrar_departamentos(self):
        try:
            nombre_departamento = self.inputBuscarDepartamento.text()
            
            if (self.esta_vacio(nombre_departamento)):
                nombre_departamento = None
            
            departamentos = self.servicio_controlador.filtrar_por_nombre_departamento_controlador(nombre_departamento)
            
            self.departamento_data = departamentos
            
            if not(departamentos):
                self.departamento_data = []
                self.limpiar_tabla("")
                return
            
            modelo_datos = QStandardItemModel(len(departamentos), 1)
            modelo_datos.setHorizontalHeaderLabels([
                "Nombre del departamento"
            ])
            
            for fila, departamento in enumerate(departamentos):
                items = [
                    QStandardItem(str(departamento["nombre_departamento"]))
                ]
                
                for columna, item in enumerate(items):
                    item.setToolTip(item.text())
                    modelo_datos.setItem(fila, columna, item)
            
            self.tvDepartamentos.setModel(modelo_datos)
            self.labelFiltroSeccionDepartamento.clear()
        except DepartamentoValidacionError as error:
            self.limpiar_tabla("\n".join(error.errores))
            self.departamento_data = []
        finally:
            header = self.tvDepartamentos.horizontalHeader()
            header.setSectionResizeMode(QHeaderView.Stretch)
    
    def seleccionar_departamento(self, indice):
        fila_seleccionada = indice.row()
        
        if ((fila_seleccionada >= 0) and (fila_seleccionada < len(self.departamento_data))):
            departamento_seleccionado = self.departamento_data[fila_seleccionada]
            self.mostrar_ventana_info_departamento(departamento_seleccionado)
    
    def mostrar_ventana_info_departamento(self, departamento_data: Dict):
        try:
            ventana_info_departamento = VentanaInfoDepartamento(
                departamento_data = departamento_data,
                servicio_controlador = self.servicio_controlador,
                ventana_principal = self.ventana_principal
            )
            
            resultado = ventana_info_departamento.exec_()
            
            if (resultado == QDialog.Accepted):
                self.filtrar_departamentos()
        except Exception as error:
            self.mostrar_mensaje_error(f"Error al mostrar la ventana de info departamento: {error}")
    
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