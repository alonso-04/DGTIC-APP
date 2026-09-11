from typing import Tuple
from PyQt5.QtWidgets import QHeaderView, QDialog
from PyQt5.QtGui import QStandardItemModel

from utilidades.gui import UiBase, cargar_completer, registrar_campos, limpiar_campos, obtener_modelo_datos_y_data
from vistas.vistas_python.VentanaPrincipal import VentanaPrincipal
from configuraciones.excepciones import NoEncontradoError, ValidacionError, LogicaError


class VentanaCategorias(UiBase):
    def __init__(self, ventana_principal: VentanaPrincipal):
        super().__init__()
        self.ventana_principal = ventana_principal
        self.ui = ventana_principal.ui
        self._servicios = self.ventana_principal._servicios
        
        
        # DATA DE LAS CATEGORÍAS DE TIPOS DE SERVICIOS
        self.categoria_data = []
        
        
        # LISTA Y MÉTODOS DE LOS COMPLETERS
        lista_campos_categorias_completers = [
            self.ui.txt_filtro_categorias_registradas,
            self.ui.txt_categoria_asociada,
            self.ui.txt_filtro_por_categoria
        ]
        
        self.cargar_completer_categorias = lambda: cargar_completer(
            self._servicios["categoria_tipo_servicio_tecnico_servicio"],
            lista_campos_categorias_completers,
            "categoria"
        )
        
        
        self.configuracion()
    
    def configuracion(self):
        self.filtrar_categorias()
        self.cargar_completer_categorias()
        
        self.ui.btn_refrescar_pagina_ventana_categorias.clicked.connect(self.refrescar_pagina_categorias)
        self.ui.btn_manual_usuario_ventana_categoria.clicked.connect(self.ver_manual_usuario)
        self.ui.btn_regresar_ventana_categoria.clicked.connect(self.ir_pagina_tipos_servicio)
        self.ui.btn_buscar_categorias.clicked.connect(self.filtrar_categorias)
        self.ui.btn_registrar_categoria.clicked.connect(self.registrar_categoria)
        
        self.ui.tabla_categorias.clicked.connect(self.seleccionar_categoria)
        self.configurar_tabla(self.ui.tabla_categorias)
    
    def refrescar_pagina_categorias(self):
        self.filtrar_categorias()
        self.cargar_completer_categorias()
    
    def ir_pagina_tipos_servicio(self):
        self.ui.ventanas.setCurrentWidget(self.ui.paginaTiposServicio)
        self.ui.setWindowTitle("Tipos de servicio")
    
    def registrar_categoria(self):
        try:
            campos_a_registrar = [(self.ui.txt_registrar_categoria, "nombre_categoria")]
            registrar_campos(self._servicios["categoria_tipo_servicio_tecnico_servicio"], campos_a_registrar, "categoria")
            limpiar_campos([self.ui.txt_registrar_categoria])
            
            self.refrescar_pagina_categorias()
        except ValidacionError as error:
            self.mostrar_mensaje_error("\n".join(error.errores))
        except LogicaError as error:
            self.mostrar_mensaje_error("\n".join(error.errores))
    
    def filtrar_categorias(self):
        try:
            lista_campos_filtrar = [(self.ui.txt_filtro_categorias_registradas, "nombre_categoria")]
            nombres_labels = ["Nombre de la categoría"]
            nombres_columnas = ["nombre_categoria"]
            
            modelo_datos, registros = obtener_modelo_datos_y_data(
                self._servicios["categoria_tipo_servicio_tecnico_servicio"].obtener_por_categoria_o_todos,
                nombres_labels,
                nombres_columnas,
                lista_campos_filtrar
            )
            
            self.categoria_data = registros
            self.ui.tabla_categorias.setModel(modelo_datos)
            self.ui.lbl_errores_filtro_categorias.clear()
            
            header = self.ui.tabla_categorias.horizontalHeader()
            header.setSectionResizeMode(QHeaderView.Stretch)
        except NoEncontradoError as error:
            self.limpiar_tabla("\n".join(error.errores))
            self.categoria_data = []
            header = self.ui.tabla_categorias.horizontalHeader()
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
                categoria_data,
                self.ventana_principal,
                "VentanaInfoCategoria.ui",
                "estilos_ventanas_info.qss"
            )
        
        self.ventana_info_categoria.actualizar_data_recibida(categoria_data)
        resultado = self.ventana_info_categoria.ui.exec_()
            
        if (resultado == QDialog.Accepted):
            self.filtrar_categorias()
    
    def mostrar_error_filtro(self, mensaje: str):
        self.ui.lbl_errores_filtro_categorias.setText(mensaje)
    
    def limpiar_tabla(self, mensaje: str = ""):
        modelo_vacio = QStandardItemModel(0, 1)
        modelo_vacio.setHorizontalHeaderLabels([
            "Nombre de la categoría"
        ])
        
        self.ui.tabla_categorias.setModel(modelo_vacio)
        
        if (mensaje):
            self.ui.lbl_errores_filtro_categorias.setText(mensaje)