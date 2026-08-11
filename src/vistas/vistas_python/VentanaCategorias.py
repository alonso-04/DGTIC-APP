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


class VentanaCategorias:
    def __init__(self, ventana_principal: VentanaPrincipal):
        super().__init__()
        self.ventana_principal = ventana_principal
        
        
        # CONTROLADORES
        self._servicios = self.ventana_principal._servicios
        
        # SECCIÓN DE REGISTRAR TIPO DE SERVICIO
        self.inputRegistrarCategoriaTipoServicio = self.ventana_principal.inputRegistrarCategoriaTipoServicio
        self.botonRegistrarCategoriaTipoServicio = self.ventana_principal.botonRegistrarCategoriaTipoServicio
        
        
        # SECCIÓN DE FILTRAR LOS TIPOS DE SERVICIO
        self.inputFiltroCategoriaTipoServicio = self.ventana_principal.inputFiltroSeccionCategoriaTipoServicio
        self.botonBuscarCategoriaTipoServicio = self.ventana_principal.botonBuscarCategoriaTipoServicio
        self.labelFiltroCategoriaTipoServicio = self.ventana_principal.labelFiltroCategoriaTipoServicio
        
        
        # SECCIÓN DE LA TABLA DE TIPOS DE SERVICIO
        self.tvRegistrosCategoriasTipoServicio = self.ventana_principal.tvRegistrosCategoriaTipoServicio
        self.categoria_data = []
        
        
        # FUNCIONES Y ELEMENTOS DE UTILIDAD
        self.mostrar_mensaje_error = self.ventana_principal.mostrar_mensaje_error
        
        lista_campos_categorias_completers = [
            self.ventana_principal.inputRegistrarCategoria,
            self.ventana_principal.inputFiltroCategoria,
            self.inputFiltroCategoriaTipoServicio
        ]
        
        self.cargar_completer_categorias = lambda: cargar_completer(
            self._servicios["categoria_tipo_servicio_tecnico_servicio"],
            lista_campos_categorias_completers,
            "categoria"
        )
        
        self.cargar_manual_usuario = self.ventana_principal.ver_manual_usuario
        self.botonRefrescarCategoriasTiposServicio = self.ventana_principal.botonRefrescarCategoriaTiposServicio
        self.botonManualUsuarioSeccionCategoriasTipoServicio = self.ventana_principal.botonManualUsuarioSeccionCategoriaTipoServicio
        
        
        # BOTOES INFERIORES
        self.botonRegresarSeccionCategoriaTipoServicio = self.ventana_principal.botonRegresarSeccionCategoriaTipoServicio
        
        self.configuracion()
    
    def configuracion(self):
        self.filtrar_categorias()
        self.cargar_completer_categorias()
        self.botonRefrescarCategoriasTiposServicio.clicked.connect(self.refrescar_pagina_categorias)
        self.botonManualUsuarioSeccionCategoriasTipoServicio.clicked.connect(self.ver_manual_usuario)
        self.botonRegresarSeccionCategoriaTipoServicio.clicked.connect(self.ir_pagina_tipos_servicio)
        self.botonBuscarCategoriaTipoServicio.clicked.connect(self.filtrar_categorias)
        self.botonRegistrarCategoriaTipoServicio.clicked.connect(self.registrar_categoria)
        self.tvRegistrosCategoriasTipoServicio.clicked.connect(self.seleccionar_categoria)
    
    def refrescar_pagina_categorias(self):
        self.filtrar_categorias()
        self.cargar_completer_categorias()
    
    def ver_manual_usuario(self):
        self.cargar_manual_usuario()
    
    def ir_pagina_tipos_servicio(self):
        self.ventana_principal.ventanas.setCurrentWidget(self.ventana_principal.paginaTiposServicio)
        self.ventana_principal.setWindowTitle("Tipos de servicio")
    
    def registrar_categoria(self):
        try:
            campos_a_registrar = [(self.inputRegistrarCategoriaTipoServicio, "nombre_categoria")]
            registrar_campos(self._servicios["categoria_tipo_servicio_tecnico_servicio"], campos_a_registrar)
            limpiar_campos([self.inputRegistrarCategoriaTipoServicio])
            
            self.refrescar_pagina_categorias()
        except ValidacionError as error:
            self.mostrar_mensaje_error("\n".join(error.errores))
        except LogicaError as error:
            self.mostrar_mensaje_error("\n".join(error.errores))
    
    def filtrar_categorias(self):
        try:
            lista_campos_filtrar = [(self.inputFiltroCategoriaTipoServicio, "nombre_categoria")]
            nombres_labels = ["Nombre de la categoría"]
            nombres_columnas = ["nombre_categoria"]
            
            modelo_datos, registros = obtener_modelo_datos_y_data(
                self._servicios["categoria_tipo_servicio_tecnico_servicio"].obtener_por_categoria_o_todos,
                lista_campos_filtrar,
                nombres_labels,
                nombres_columnas
            )
            
            self.categoria_data = registros
            self.tvRegistrosCategoriasTipoServicio.setModel(modelo_datos)
            self.labelFiltroCategoriaTipoServicio.clear()
            
            header = self.tvRegistrosCategoriasTipoServicio.horizontalHeader()
            header.setSectionResizeMode(QHeaderView.Stretch)
        except NoEncontradoError as error:
            self.limpiar_tabla("\n".join(error.errores))
            self.categoria_data = []
            header = self.tvRegistrosCategoriasTipoServicio.horizontalHeader()
            header.setSectionResizeMode(QHeaderView.Stretch)
    
    def seleccionar_categoria(self, indice: int):
        fila_seleccionada = indice.row()
        
        if ((fila_seleccionada >= 0) and (fila_seleccionada < len(self.categoria_data))):
            categoria_seleccionada = self.categoria_data[fila_seleccionada]
            self.mostrar_ventana_info_categoria(categoria_seleccionada)
    
    def mostrar_ventana_info_categoria(self, categoria_data: Tuple):
        if not(hasattr(self, "ventana_info_categoria")):
            from vistas.vistas_python.VentanaInfoCategoria import VentanaInfoCategoria
            self.ventana_info_categoria = VentanaInfoCategoria(
                categoria_data = categoria_data,
                ventana_principal = self.ventana_principal
            )
        
        self.ventana_info_categoria.actualizar_data_recibida(categoria_data)
        resultado = self.ventana_info_categoria.exec_()
            
        if (resultado == QDialog.Accepted):
            self.filtrar_categorias()
    
    def mostrar_error_filtro(self, mensaje: str):
        self.labelFiltroCategoriaTipoServicio.setText(mensaje)
    
    def limpiar_tabla(self, mensaje: str = ""):
        modelo_vacio = QStandardItemModel(0, 1)
        modelo_vacio.setHorizontalHeaderLabels([
            "Nombre de la categoría"
        ])
        
        self.tvRegistrosCategoriasTipoServicio.setModel(modelo_vacio)
        
        if (mensaje):
            self.labelFiltroCategoriaTipoServicio.setText(mensaje)