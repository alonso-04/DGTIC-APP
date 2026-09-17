from typing import Tuple
from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import QHeaderView, QDialog
from PyQt5.QtGui import QStandardItemModel

from utilidades.gui import UiBase, cargar_completer, registrar_campos, limpiar_campos, obtener_modelo_datos_y_data
from vistas.vistas_python.VentanaPrincipal import VentanaPrincipal
from configuraciones.excepciones import NoEncontradoError, ValidacionError, LogicaError


class VentanaTipoServicio(UiBase):
    def __init__(self, ventana_principal: VentanaPrincipal):
        super().__init__()
        self.ventana_principal = ventana_principal
        self.ui = ventana_principal.ui
        self._servicios = self.ventana_principal._servicios
        
        
        # DATA DE LOS TIPOS DE SERVICIO
        self.tipo_servicio_data = []
        
        
        # LISTA Y MÉTODOS DE LOS COMPLETERS
        lista_campos_tipos_servicio_completers = [
            self.ui.txt_filtro_tipos_servicios_registrados,
            self.ui.txt_filtro_servicio_prestado,
            self.ui.txt_servicio_prestado
        ]
        
        lista_campos_categorias_completers = [
            self.ui.txt_categoria_asociada,
            self.ui.txt_filtro_categorias_registradas,
            self.ui.txt_filtro_por_categoria
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
        
        
        self.configuracion()
    
    def configuracion(self):
        self.filtrar_tipos_servicio()
        self.cargar_completer_categorias()
        
        self.ui.btn_refrescar_pagina_ventana_tipos_servicio.clicked.connect(self.refrescar_pagina_tipos_servicio)
        self.ui.btn_manual_usuario_ventana_tipos_servicio.clicked.connect(self.ver_manual_usuario)
        self.ui.btn_regresar_ventana_tipos_servicio.clicked.connect(self.ir_pagina_app)
        self.ui.btn_buscar_tipos_servicio.clicked.connect(self.filtrar_tipos_servicio)
        self.ui.tool_ventana_categorias.clicked.connect(self.ir_pagina_categorias)
        self.ui.btn_registrar_tipo_servicio.clicked.connect(self.registrar_tipo_servicio)
        
        self.ui.tabla_tipos_servicio.clicked.connect(self.seleccionar_tipo_servicio)
        self.configurar_tabla(self.ui.tabla_tipos_servicio)
    
    def refrescar_pagina_tipos_servicio(self):
        self.filtrar_tipos_servicio()
        self.cargar_completer_tipos_servicio()
        self.cargar_completer_categorias()
    
    def ir_pagina_app(self):
        self.ui.ventanas.setCurrentWidget(self.ui.paginaApp)
        self.ui.setWindowTitle("App")
        self.ui.de_filtro_fecha_servicio.setDate(QDate.currentDate())
        self.ui.de_fecha_servicio.setDate(QDate.currentDate())
        self.ui.btn_buscar_servicios.click()
    
    def ir_pagina_categorias(self):
        if not(hasattr(self, "ventana_categorias")):
            from vistas.vistas_python.VentanaCategorias import VentanaCategorias
            self.ventana_categorias = VentanaCategorias(self.ventana_principal)
            
        self.ui.ventanas.setCurrentWidget(self.ui.paginaCategoriaTipoServicio)
        self.ui.setWindowTitle("Categorías de tipo de servicio")
    
    def registrar_tipo_servicio(self):
        try:
            campos_a_registrar = [
                (self.ui.txt_registrar_tipo_servicio, "tipo_servicio_prestado"),
                (self.ui.txt_categoria_asociada, "nombre_categoria")
            ]
            
            registrar_campos(self._servicios["tipo_servicio_tecnico_servicio"], campos_a_registrar, "tipo_servicio")
            limpiar_campos([self.ui.txt_registrar_tipo_servicio, self.ui.txt_categoria_asociada])
            
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
                (self.ui.txt_filtro_tipos_servicios_registrados, "tipo_servicio_prestado"),
                (self.ui.txt_filtro_por_categoria, "nombre_categoria")
            ]
            
            nombres_labels = ["Nombre del tipo de servicio", "Categoría"]
            nombres_columnas = ["tipo_servicio_prestado", "nombre_categoria"]
            
            modelo_datos, registros = obtener_modelo_datos_y_data(
                self._servicios["tipo_servicio_tecnico_servicio"].obtener_por_tipo_categoria_o_todos,
                nombres_labels,
                nombres_columnas,
                lista_campos_filtrar
            )
            
            self.tipo_servicio_data = registros
            self.ui.tabla_tipos_servicio.setModel(modelo_datos)
            self.ui.lbl_errores_filtro_tipos_servicio.clear()
            
            header = self.ui.tabla_tipos_servicio.horizontalHeader()
            header.setSectionResizeMode(QHeaderView.Stretch)
        except NoEncontradoError as error:
            self.limpiar_tabla("\n".join(error.errores))
            self.tipo_servicio_data = []
            header = self.ui.tabla_tipos_servicio.horizontalHeader()
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
                tipo_servicio_data,
                self.ventana_principal,
                "VentanaInfoTipoServicio.ui",
                "estilos_ventanas_info.qss"
            )
        
        self.ventana_info_tipo_servicio.actualizar_data_recibida(tipo_servicio_data)
        self.ventana_info_tipo_servicio.cargar_completers_info()
        
        resultado = self.ventana_info_tipo_servicio.ui.exec_()
            
        if (resultado == QDialog.Accepted):
            self.filtrar_tipos_servicio()
    
    def mostrar_error_filtro(self, mensaje: str):
        self.ui.lbl_errores_filtro_tipos_servicio.setText(mensaje)
    
    def limpiar_tabla(self, mensaje: str = ""):
        modelo_vacio = QStandardItemModel(0, 1)
        modelo_vacio.setHorizontalHeaderLabels([
            "Nombre del tipo de servicio",
            "Categoría"
        ])
        
        self.ui.tabla_tipos_servicio.setModel(modelo_vacio)
        
        if (mensaje):
            self.ui.lbl_errores_filtro_tipos_servicio.setText(mensaje)