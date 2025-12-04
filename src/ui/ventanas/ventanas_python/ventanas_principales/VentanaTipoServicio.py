from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import QHeaderView, QDialog
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from typing import Dict
from dominio.excepciones import TipoServicioValidacionError
from ui.ventanas.ventanas_python.ventanas_principales.VentanaPrincipal import VentanaPrincipal
from ui.ventanas.ventanas_python.ventanas_info.VentanaInfoTipoServicio import VentanaInfoTipoServicio


class VentanaTipoServicio:
    def __init__(self, ventana_principal: VentanaPrincipal):
        super().__init__()
        self.ventana_principal = ventana_principal
        
        # FUNCIONES Y ELEMENTOS DE UTILIDAD
        self.esta_vacio = self.ventana_principal.esta_vacio
        self.mostrar_mensaje_error = self.ventana_principal.mostrar_mensaje_error
        self.cargar_completer_tipos_servicio = self.ventana_principal.cargar_completer_tipos_servicio
        self.botonRefrescarTiposServicio = self.ventana_principal.botonRefrescarTiposServicio
        
        # CONTROLADORES
        self.servicio_controlador = self.ventana_principal.servicio_controlador
        
        # SECCIÓN DE REGISTRAR TIPO DE SERVICIO
        self.inputRegistrarTipoServicio = self.ventana_principal.inputRegistrarTipoServicio
        self.botonRegistrarTipoServicio = self.ventana_principal.botonRegistrarTipoServicio
        
        
        # SECCIÓN DE FILTRAR LOS TIPOS DE SERVICIO
        self.inputFiltroTipoServicio = self.ventana_principal.inputFiltroTipoServicio
        self.botonBuscarTipoServicio = self.ventana_principal.botonBuscarTipoServicio
        self.labelFiltroSeccionTipoServicio = self.ventana_principal.labelFiltroSeccionTipoServicio
        
        
        # SECCIÓN DE LA TABLA DE TIPOS DE SERVICIO
        self.tvRegistrosTipoServicio = self.ventana_principal.tvRegistrosTipoServicio
        self.tipo_servicio_data = []
        
        
        # BOTOES INFERIORES
        self.botonRegresarSeccionTipoServicio = self.ventana_principal.botonRegresarSeccionTipoServicio
        
        self.configuracion()
    
    def configuracion(self):
        self.botonRefrescarTiposServicio.clicked.connect(self.refrescar_pagina_tipos_servicio)
        self.botonRegresarSeccionTipoServicio.clicked.connect(self.ir_pagina_app)
        self.botonBuscarTipoServicio.clicked.connect(self.filtrar_tipos_servicio)
        self.botonRegistrarTipoServicio.clicked.connect(self.registrar_tipo_servicio)
        self.tvRegistrosTipoServicio.clicked.connect(self.seleccionar_tipo_servicio)
    
    def refrescar_pagina_tipos_servicio(self):
        self.filtrar_tipos_servicio()
        self.cargar_completer_tipos_servicio()
    
    def ir_pagina_app(self):
        self.ventana_principal.ventanas.setCurrentWidget(self.ventana_principal.paginaApp)
        self.ventana_principal.setWindowTitle("App")
        self.ventana_principal.deFiltroFecha.setDate(QDate.currentDate())
        self.ventana_principal.deFecha.setDate(QDate.currentDate())
    
    def registrar_tipo_servicio(self):
        try:
            tipo_servicio_prestado = self.inputRegistrarTipoServicio.text()
            
            if (self.esta_vacio(tipo_servicio_prestado)):
                tipo_servicio_prestado = None
            
            self.servicio_controlador.registrar_tipo_servicio_controlador(
                tipo_servicio_prestado
            )
            
            self.inputRegistrarTipoServicio.clear()
            self.filtrar_tipos_servicio()
            self.cargar_completer_tipos_servicio()
        except TipoServicioValidacionError as error:
            self.mostrar_mensaje_error("\n".join(error.errores))
    
    def filtrar_tipos_servicio(self):
        try:
            nombre_tipo_servicio = self.inputFiltroTipoServicio.text()
            
            if (self.esta_vacio(nombre_tipo_servicio)):
                nombre_tipo_servicio = None
            
            tipos_servicio = self.servicio_controlador.filtrar_por_nombre_tipo_servicio_controlador(nombre_tipo_servicio)
            self.tipo_servicio_data = tipos_servicio
            
            if not(tipos_servicio):
                self.tipo_servicio_data = []
                self.limpiar_tabla("")
                return
            
            modelo_datos = QStandardItemModel(len(tipos_servicio), 1)
            modelo_datos.setHorizontalHeaderLabels([
                "Nombre del tipo de servicio"
            ])
            
            for fila, tipo_servicio in enumerate(tipos_servicio):
                items = [
                    QStandardItem(str(tipo_servicio["tipo_servicio_prestado"]))
                ]
                
                for columna, item in enumerate(items):
                    item.setToolTip(item.text())
                    modelo_datos.setItem(fila, columna, item)
            
            self.tvRegistrosTipoServicio.setModel(modelo_datos)
            self.labelFiltroSeccionTipoServicio.clear()
        except TipoServicioValidacionError as error:
            self.limpiar_tabla("\n".join(error.errores))
            self.tipo_servicio_data = []
        finally:
            header = self.tvRegistrosTipoServicio.horizontalHeader()
            header.setSectionResizeMode(QHeaderView.Stretch)
    
    def seleccionar_tipo_servicio(self, indice):
        fila_seleccionada = indice.row()
        
        if ((fila_seleccionada >= 0) and (fila_seleccionada < len(self.tipo_servicio_data))):
            tipo_servicio_seleccionado = self.tipo_servicio_data[fila_seleccionada]
            self.mostrar_ventana_info_tipo_servicio(tipo_servicio_seleccionado)
    
    def mostrar_ventana_info_tipo_servicio(self, tipo_servicio_data: Dict):
        try:
            ventana_info_tipo_servicio = VentanaInfoTipoServicio(
                tipo_servicio_data = tipo_servicio_data,
                servicio_controlador = self.servicio_controlador,
                ventana_principal = self.ventana_principal
            )
            
            resultado = ventana_info_tipo_servicio.exec_()
            
            if (resultado == QDialog.Accepted):
                self.filtrar_tipos_servicio()
        except Exception as error:
            self.mostrar_mensaje_error(f"Error al mostrar la ventana de info tipo de servicio: {error}")
    
    def mostrar_error_filtro(self, mensaje: str):
        self.labelFiltroSeccionTipoServicio.setText(mensaje)
    
    def limpiar_tabla(self, mensaje: str = ""):
        modelo_vacio = QStandardItemModel(0, 1)
        modelo_vacio.setHorizontalHeaderLabels([
            "Nombre del tipo de servicio"
        ])
        
        self.tvRegistrosTipoServicio.setModel(modelo_vacio)
        
        if (mensaje):
            self.labelFiltroSeccionTipoServicio.setText(mensaje)