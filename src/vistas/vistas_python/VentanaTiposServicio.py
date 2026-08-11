from typing import Tuple
from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import QHeaderView, QDialog
from PyQt5.QtGui import QStandardItemModel

from vistas.vistas_python.VentanaPrincipal import VentanaPrincipal
from vistas.utilidades_gui.cargar_completers import cargar_completer
from vistas.utilidades_gui.registrar import registrar_campos
from vistas.utilidades_gui.limpiar_campos import limpiar_campos
from vistas.utilidades_gui.filtrar import obtener_modelo_datos_y_data
from configuraciones.excepciones import NoEncontradoError, ValidacionError, LogicaError


class VentanaTipoServicio:
    def __init__(self, ventana_principal: VentanaPrincipal):
        super().__init__()
        self.ventana_principal = ventana_principal
        
        
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
        
        
        # FUNCIONES Y ELEMENTOS DE UTILIDAD
        self.mostrar_mensaje_error = self.ventana_principal.mostrar_mensaje_error
        
        lista_campos_tipos_servicio_completers = [
            self.ventana_principal.inputServicioPrestado,
            self.ventana_principal.inputFiltroServicioPrestado,
            self.inputFiltroTipoServicio
        ]
        
        lista_campos_categorias_completers = [
            self.inputRegistrarCategoria,
            self.inputFiltroCategoria
        ]
        
        self.cargar_completer_tipos_servicio = lambda: cargar_completer(
            self._servicios["tipo_servicio_tecnico_servicio"],
            lista_campos_tipos_servicio_completers,
            "tipo_servicio"
        )
        
        self.cargar_completer_categorias = lambda: cargar_completer(
            self._servicios["categoria_tipo_servicio_tecnico_servicio"],
            lista_campos_categorias_completers,
            "categoria"
        )
        
        self.cargar_manual_usuario = self.ventana_principal.ver_manual_usuario
        self.botonRefrescarTiposServicio = self.ventana_principal.botonRefrescarTiposServicio
        self.botonManualUsuarioSeccionTipoServicio = self.ventana_principal.botonManualUsuarioSeccionTipoServicio
        
        
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
            campos_a_registrar = [
                (self.inputRegistrarTipoServicio, "tipo_servicio_prestado"),
                (self.inputRegistrarCategoria, "nombre_categoria")
            ]
            
            registrar_campos(self._servicios["tipo_servicio_tecnico_servicio"], campos_a_registrar)
            limpiar_campos([self.inputRegistrarTipoServicio, self.inputRegistrarCategoria])
            
            self.refrescar_pagina_tipos_servicio()
        except ValidacionError as error:
            self.mostrar_mensaje_error("\n".join(error.errores))
        except NoEncontradoError as error:
            self.mostrar_mensaje_error("\n".join(error.errores))
        except LogicaError as error:
            self.mostrar_mensaje_error("\n".join(error.errores))
    
    def filtrar_tipos_servicio(self):
        try:
            lista_campos_filtrar = [
                (self.inputFiltroTipoServicio, "tipo_servicio_prestado"),
                (self.inputFiltroCategoria, "nombre_categoria")
            ]
            
            nombres_labels = ["Nombre del tipo de servicio", "Categoría"]
            nombres_columnas = ["tipo_servicio_prestado", "nombre_categoria"]
            
            modelo_datos, registros = obtener_modelo_datos_y_data(
                self._servicios["tipo_servicio_tecnico_servicio"].obtener_por_tipo_categoria_o_todos,
                lista_campos_filtrar,
                nombres_labels,
                nombres_columnas
            )
            
            self.tipo_servicio_data = registros
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