from typing import Tuple
from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import QHeaderView, QDialog
from PyQt5.QtGui import QStandardItemModel, QStandardItem

from vistas.vistas_python.VentanaPrincipal import VentanaPrincipal
from configuraciones.excepciones import NoEncontradoError, ValidacionError, LogicaError


class VentanaTipoServicio:
    def __init__(self, ventana_principal: VentanaPrincipal):
        super().__init__()
        self.ventana_principal = ventana_principal
        
        # FUNCIONES Y ELEMENTOS DE UTILIDAD
        self.mostrar_mensaje_error = self.ventana_principal.mostrar_mensaje_error
        self.cargar_completer_tipos_servicio = self.ventana_principal.cargar_completer_tipos_servicio
        self.cargar_completer_categorias = self.ventana_principal.cargar_completer_categorias
        self.cargar_manual_usuario = self.ventana_principal.ver_manual_usuario
        self.botonRefrescarTiposServicio = self.ventana_principal.botonRefrescarTiposServicio
        self.botonManualUsuarioSeccionTipoServicio = self.ventana_principal.botonManualUsuarioSeccionTipoServicio
        
        # CONTROLADORES
        self._servicios = self.ventana_principal._servicios
        
        # SECCIÓN DE REGISTRAR TIPO DE SERVICIO
        self.inputRegistrarTipoServicio = self.ventana_principal.inputRegistrarTipoServicio
        self.inputRegistrarCategoria = self.ventana_principal.inputRegistrarCategoria
        self.tbOtraCategoria = self.ventana_principal.tbOtraCategoria
        self.botonRegistrarTipoServicio = self.ventana_principal.botonRegistrarTipoServicio
        
        
        # SECCIÓN DE FILTRAR LOS TIPOS DE SERVICIO
        self.inputFiltroTipoServicio = self.ventana_principal.inputFiltroTipoServicio
        self.inputFiltroCategoria = self.ventana_principal.inputFiltroCategoria
        self.botonBuscarTipoServicio = self.ventana_principal.botonBuscarTipoServicio
        self.labelFiltroSeccionTipoServicio = self.ventana_principal.labelFiltroSeccionTipoServicio
        
        
        # SECCIÓN DE LA TABLA DE TIPOS DE SERVICIO
        self.tvRegistrosTipoServicio = self.ventana_principal.tvRegistrosTipoServicio
        self.tipo_servicio_data = []
        
        
        # BOTOES INFERIORES
        self.botonRegresarSeccionTipoServicio = self.ventana_principal.botonRegresarSeccionTipoServicio
        
        self.configuracion()
    
    def configuracion(self):
        self.filtrar_tipos_servicio()
        self.cargar_completer_categorias()
        self.botonRefrescarTiposServicio.clicked.connect(self.refrescar_pagina_tipos_servicio)
        self.botonManualUsuarioSeccionTipoServicio.clicked.connect(self.ver_manual_usuario)
        self.botonRegresarSeccionTipoServicio.clicked.connect(self.ir_pagina_app)
        self.botonBuscarTipoServicio.clicked.connect(self.filtrar_tipos_servicio)
        self.tbOtraCategoria.clicked.connect(self.ir_pagina_categorias)
        self.botonRegistrarTipoServicio.clicked.connect(self.registrar_tipo_servicio)
        self.tvRegistrosTipoServicio.clicked.connect(self.seleccionar_tipo_servicio)
    
    def refrescar_pagina_tipos_servicio(self):
        self.filtrar_tipos_servicio()
        self.cargar_completer_tipos_servicio()
        self.cargar_completer_categorias()
    
    def ver_manual_usuario(self):
        self.cargar_manual_usuario()
    
    def ir_pagina_app(self):
        self.ventana_principal.ventanas.setCurrentWidget(self.ventana_principal.paginaApp)
        self.ventana_principal.setWindowTitle("App")
        self.ventana_principal.deFiltroFecha.setDate(QDate.currentDate())
        self.ventana_principal.deFecha.setDate(QDate.currentDate())
    
    def ir_pagina_categorias(self):
        if not(hasattr(self, "ventana_categorias")):
            from vistas.vistas_python.VentanaCategorias import VentanaCategorias
            self.ventana_categorias = VentanaCategorias(self.ventana_principal)
            
        self.ventana_principal.ventanas.setCurrentWidget(self.ventana_principal.paginaCategoriaTipoServicio)
        self.ventana_principal.setWindowTitle("Categorías de tipo de servicio")
    
    def registrar_tipo_servicio(self):
        try:
            tipo_servicio_prestado = self.inputRegistrarTipoServicio.text()
            categoria = self.inputRegistrarCategoria.text()
            
            self._servicios["tipo_servicio_tecnico_servicio"].registrar(categoria, tipo_servicio_prestado)
            
            self.inputRegistrarTipoServicio.clear()
            self.inputRegistrarCategoria.clear()
            self.filtrar_tipos_servicio()
            self.cargar_completer_tipos_servicio()
        except ValidacionError as error:
            self.mostrar_mensaje_error("\n".join(error.errores))
        except NoEncontradoError as error:
            self.mostrar_mensaje_error("\n".join(error.errores))
        except LogicaError as error:
            self.mostrar_mensaje_error("\n".join(error.errores))
    
    def filtrar_tipos_servicio(self):
        try:
            nombre_tipo_servicio = self.inputFiltroTipoServicio.text()
            nombre_categoria = self.inputFiltroCategoria.text()
            
            tipos_servicio = self._servicios["tipo_servicio_tecnico_servicio"].obtener_por_tipo_categoria_o_todos(nombre_tipo_servicio, nombre_categoria)
            
            self.tipo_servicio_data = tipos_servicio
            
            modelo_datos = QStandardItemModel(len(tipos_servicio), 1)
            modelo_datos.setHorizontalHeaderLabels([
                "Nombre del tipo de servicio",
                "Categoría"
            ])
            
            for fila, tipo_servicio in enumerate(tipos_servicio):
                items = [
                    QStandardItem(str(tipo_servicio[1])),
                    QStandardItem(str(tipo_servicio[2]))
                ]
                
                for columna, item in enumerate(items):
                    item.setToolTip(item.text())
                    modelo_datos.setItem(fila, columna, item)
            
            self.tvRegistrosTipoServicio.setModel(modelo_datos)
            self.labelFiltroSeccionTipoServicio.clear()
            
            header = self.tvRegistrosTipoServicio.horizontalHeader()
            header.setSectionResizeMode(QHeaderView.Stretch)
        except NoEncontradoError as error:
            self.limpiar_tabla("\n".join(error.errores))
            self.tipo_servicio_data = []
            header = self.tvRegistrosTipoServicio.horizontalHeader()
            header.setSectionResizeMode(QHeaderView.Stretch)
    
    def seleccionar_tipo_servicio(self, indice: int):
        fila_seleccionada = indice.row()
        
        if ((fila_seleccionada >= 0) and (fila_seleccionada < len(self.tipo_servicio_data))):
            tipo_servicio_seleccionado = self.tipo_servicio_data[fila_seleccionada]
            self.mostrar_ventana_info_tipo_servicio(tipo_servicio_seleccionado)
    
    def mostrar_ventana_info_tipo_servicio(self, tipo_servicio_data: Tuple):
        if not(hasattr(self, "ventana_info_tipo_servicio")):
            from vistas.vistas_python.VentanaInfoTipoServicio import VentanaInfoTipoServicio
            self.ventana_info_tipo_servicio = VentanaInfoTipoServicio(
                tipo_servicio_data = tipo_servicio_data,
                ventana_principal = self.ventana_principal
            )
        
        self.ventana_info_tipo_servicio.actualizar_data_recibida(tipo_servicio_data)
        resultado = self.ventana_info_tipo_servicio.exec_()
            
        if (resultado == QDialog.Accepted):
            self.filtrar_tipos_servicio()
    
    def mostrar_error_filtro(self, mensaje: str):
        self.labelFiltroSeccionTipoServicio.setText(mensaje)
    
    def limpiar_tabla(self, mensaje: str = ""):
        modelo_vacio = QStandardItemModel(0, 1)
        modelo_vacio.setHorizontalHeaderLabels([
            "Nombre del tipo de servicio",
            "Categoría"
        ])
        
        self.tvRegistrosTipoServicio.setModel(modelo_vacio)
        
        if (mensaje):
            self.labelFiltroSeccionTipoServicio.setText(mensaje)