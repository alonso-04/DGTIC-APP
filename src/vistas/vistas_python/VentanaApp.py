from typing import List, Tuple
from pathlib import Path
from PyQt5.QtGui import QStandardItemModel, QColor, QRegExpValidator
from PyQt5.QtCore import QThread, pyqtSignal, QRegExp, QEvent
from PyQt5.QtWidgets import QHeaderView, QDialog, QFileDialog

from utilidades.gui import UiBase
from vistas.vistas_python.VentanaPrincipal import VentanaPrincipal
from vistas.utilidades_gui.cargar_completers import cargar_completer
from vistas.utilidades_gui.registrar import registrar_campos
from vistas.utilidades_gui.limpiar_campos import limpiar_campos
from vistas.utilidades_gui.filtrar import obtener_modelo_datos_y_data
from configuraciones.respaldo import RespaldoLocal
from configuraciones.excepciones import ValidacionError, NoEncontradoError, LogicaError
from reportes.reporte_servicios import ReporteServicios


class HiloImportarRespaldoBD(QThread):
    resultado = pyqtSignal(bool, str)
    
    def __init__(self, respaldo_local: RespaldoLocal, ruta_archivo: Path):
        super().__init__()
        self.respaldo_local = respaldo_local
        self.ruta_archivo = ruta_archivo
    
    def run(self):
        try:
            self.respaldo_local().importar(self.ruta_archivo)
            self.resultado.emit(True, "Se importó el respaldo correctamente.")
        except Exception as error:
            self.resultado.emit(False, f"Error al importar el respaldo: {error}")


class VentanaApp(UiBase):
    def __init__(self, ventana_principal: VentanaPrincipal):
        super().__init__()
        self.ventana_principal = ventana_principal
        self.ui = ventana_principal.ui
        
        # SERVICIOS
        self._servicios = ventana_principal._servicios
        
        self.respaldo_local = RespaldoLocal
        
        
        self.line_edit_spbox_cantidad = self.ui.spbox_cantidad.lineEdit()
        regex = QRegExp("[0-9]+")
        validador = QRegExpValidator(regex, self.line_edit_spbox_cantidad)
        self.line_edit_spbox_cantidad.setValidator(validador)
        self.line_edit_spbox_cantidad.installEventFilter(self.ui)
        
        
        # SECCIÓN DE LA TABLA DE REGISTROS
        self.servicio_data = []
        
        # FUNCIONES Y ELEMENTOS DE UTILIDAD
        self.mostrar_mensaje_error = self.ventana_principal.mostrar_mensaje_error
        self.mostrar_mensaje_info = self.ventana_principal.mostrar_mensaje_info
        self.cargar_manual_usuario = self.ventana_principal.ver_manual_usuario
        
        lista_campos_departamento_completers = [
            self.ui.txt_nombre_departamento,
            self.ui.txt_filtro_nombre_departamento,
            self.ui.txt_filtrar_departamentos_registrados
        ]
        
        lista_campos_tipos_servicio_completers = [
            self.ui.txt_servicio_prestado,
            self.ui.txt_filtro_servicio_prestado,
            self.ui.txt_filtro_tipos_servicios_registrados
        ]
        
        self.cargar_completer_departamento = lambda: cargar_completer(
            self._servicios["departamento_servicio"],
            lista_campos_departamento_completers,
            "departamento"
        )
        
        self.cargar_completer_tipos_servicio = lambda: cargar_completer(
            self._servicios["tipo_servicio_tecnico_servicio"],
            lista_campos_tipos_servicio_completers,
            "tipo_servicio"
        )
        
        self.configuracion()
    
    def eventFilter(self, obj, event):
        if obj is self.line_edit_spbox_cantidad and event.type() == QEvent.KeyPress:
            if event.text() == ',':
                return True  # Bloquea la coma del spbox_cantidad
        return super().eventFilter(obj, event)
    
    def configuracion(self):
        self.cargar_completer_departamento()
        self.cargar_completer_tipos_servicio()
        
        self.ui.btn_refrescar_pagina_ventana_app.clicked.connect(self.refrescar_pagina_app)
        self.ui.btn_manual_usuario_ventana_app.clicked.connect(self.ver_manual_usuario)
        
        self.ui.tool_ventana_departamentos.clicked.connect(self.ir_pagina_crear_departamento)
        self.ui.tool_ventana_tipos_servicio.clicked.connect(self.ir_pagina_crear_tipo_servicio)
        
        self.ui.btn_registrar_servicio.clicked.connect(self.registrar_nuevo_servicio)
        
        self.ui.btn_buscar_servicios.clicked.connect(self.filtrar_servicios)
        self.ui.de_filtro_fecha_servicio.dateChanged.connect(self.filtrar_servicios)
        
        self.ui.tabla_servicios.clicked.connect(self.seleccionar_servicio)
        self.configurar_tabla(self.ui.tabla_servicios)
        
        self.ui.btn_gestion_usuarios.clicked.connect(self.ir_pagina_gestion_usuarios)
        self.ui.btn_crear_respaldo.clicked.connect(self.generar_respaldo)
        self.ui.btn_importar_respaldo.clicked.connect(self.importar_respaldo)
        self.ui.btn_generar_reporte.clicked.connect(self.generar_reporte)
        self.ui.btn_cerrar_sesion.clicked.connect(self.cerrar_sesion)
    
    def refrescar_pagina_app(self):
        self.filtrar_servicios()
        self.cargar_completer_departamento()
        self.cargar_completer_tipos_servicio()
    
    def ver_manual_usuario(self):
        self.cargar_manual_usuario()
    
    def cerrar_sesion(self):
        self._servicios["usuario_servicio"].cerrar_sesion()
        self.ir_pagina_inicio_sesion()
    
    def ir_pagina_inicio_sesion(self):
        self.ui.ventanas.setCurrentWidget(self.ui.paginaIniciarSesion)
        self.ui.setWindowTitle("Iniciar Sesión")
    
    def ir_pagina_gestion_usuarios(self):
        if (self._servicios["usuario_servicio"].usuario_es_admin()):
            if not(hasattr(self, "ventana_usuarios")):
                from vistas.vistas_python.VentanaUsuarios import VentanaUsuarios
                self.ventana_usuarios = VentanaUsuarios(self.ventana_principal)
                self.cargar_estilos("estilos_ventana_gestion_usuarios.qss", self.ui.paginaCrearUsuario)
                
            self.ui.ventanas.setCurrentWidget(self.ui.paginaCrearUsuario)
            self.ui.setWindowTitle("Usuarios")
        else:
            self.mostrar_mensaje_error("No puedes entrar a esta sección porque no eres Administrador.")
    
    def ir_pagina_crear_departamento(self):
        if not(hasattr(self, "ventana_departamentos")):
            from vistas.vistas_python.VentanaDepartamento import VentanaDepartamentos
            self.ventana_departamentos = VentanaDepartamentos(self.ventana_principal)
        
        self.ui.ventanas.setCurrentWidget(self.ui.paginaDepartamentos)
        self.ui.setWindowTitle("Departamentos")
    
    def ir_pagina_crear_tipo_servicio(self):
        if not(hasattr(self, "ventana_tipos_servicio")):
            from vistas.vistas_python.VentanaTiposServicio import VentanaTipoServicio
            self.ventana_tipos_servicio = VentanaTipoServicio(self.ventana_principal)
        
        self.ui.ventanas.setCurrentWidget(self.ui.paginaTiposServicio)
        self.ui.setWindowTitle("Tipos de servicio")
    
    def registrar_nuevo_servicio(self):
        try:
            campos_a_registrar = [
                (self.ui.txt_nombre_departamento, "nombre_departamento"),
                (self.ui.txt_falla_presenta, "falla_presenta"),
                (self.ui.txt_nombres_tecnicos, "nombres_tecnicos"),
                (self.ui.spbox_cantidad, "cantidad"),
                (self.ui.txt_descripcion, "descripcion"),
                (self.ui.txt_servicio_prestado, "tipo_servicio_prestado"),
                (self.ui.de_fecha_servicio, "fecha_servicio"),
                (self.ui.txt_observaciones_adicionales, "observaciones_adicionales")
            ]
            
            registrar_campos(self._servicios["servicio_tecnico_servicio"], campos_a_registrar)
            
            limpiar_campos([
                self.ui.txt_nombre_departamento,
                self.ui.txt_falla_presenta,
                self.ui.txt_nombres_tecnicos,
                self.ui.spbox_cantidad,
                self.ui.txt_descripcion,
                self.ui.txt_servicio_prestado,
                self.ui.txt_observaciones_adicionales
            ])
            
            self.filtrar_servicios()
        except NoEncontradoError as error:
            self.mostrar_mensaje_error("\n".join(error.errores))
        except ValidacionError as error:
            self.mostrar_mensaje_error("\n".join(error.errores))
        except LogicaError as error:
            self.mostrar_mensaje_error("\n".join(error.errores))
    
    def filtrar_servicios(self):
        try:
            lista_campos_filtrar = [
                (self.ui.de_filtro_fecha_servicio, "fecha_servicio"),
                (self.ui.txt_filtro_nombre_departamento, "nombre_departamento"),
                (self.ui.txt_filtro_servicio_prestado, "tipo_servicio_prestado")
            ]
            
            nombres_labels = [
                "Departamento",
                "Fecha",
                "Falla que presenta",
                "Servicio prestado",
                "Nombre del técnico",
                "Descripción",
                "Cantidad",
                "Observaciones"
            ]
            
            nombres_columnas = [
                "nombre_departamento",
                "fecha_servicio",
                "falla_presenta",
                "tipo_servicio_prestado",
                "nombres_tecnicos",
                "descripcion",
                "cantidad",
                "observaciones_adicionales"
            ]
            
            # Resaltar la columna de "Observaciones"
            FILAS_A_RESALTAR = {"color": QColor(255, 240, 180), "nombre_columna": nombres_columnas[7]}
            
            modelo_datos, registros = obtener_modelo_datos_y_data(
                self._servicios["servicio_tecnico_servicio"].obtener_por_fecha_o_departamento_o_tipo_servicio,
                nombres_labels,
                nombres_columnas,
                lista_campos_filtrar,
                FILAS_A_RESALTAR
            )
            
            self.servicio_data = registros
            self.ui.tabla_servicios.setModel(modelo_datos)
            self.ui.lbl_errores_filtro_servicios.clear()
            
            header = self.ui.tabla_servicios.horizontalHeader()
            header.setSectionResizeMode(QHeaderView.Stretch)
        except NoEncontradoError as error:
            self.servicio_data = []
            self.limpiar_tabla("\n".join(error.errores))
            header = self.ui.tabla_servicios.horizontalHeader()
            header.setSectionResizeMode(QHeaderView.Stretch)
    
    def seleccionar_servicio(self, indice: int):
        fila_seleccionada = indice.row()
        
        if ((fila_seleccionada >= 0) and (fila_seleccionada < len(self.servicio_data))):
            servicio_seleccionado = self.servicio_data[fila_seleccionada]
            self.mostrar_ventana_info_servicio(servicio_seleccionado)
    
    def mostrar_ventana_info_servicio(self, servicio_data: List[Tuple]):
        if not(hasattr(self, "ventana_info_servicio")):
            from vistas.vistas_python.VentanaInfoServicio import VentanaInfoServicio
            self.ventana_info_servicio = VentanaInfoServicio(servicio_data, self._servicios, "VentanaInfoServicio.ui", "estilos_ventanas_info.qss")
        
        self.ventana_info_servicio.actualizar_data_recibida(servicio_data)
        
        resultado = self.ventana_info_servicio.ui.exec_()
        if (resultado == QDialog.Accepted):
            self.filtrar_servicios()
    
    def mostrar_error_filtro(self, mensaje: str):
        self.lbl_errores_filtro_servicios.setText(mensaje)
    
    def limpiar_tabla(self, mensaje: str = ""):
        modelo_vacio = QStandardItemModel(0, 6)
        modelo_vacio.setHorizontalHeaderLabels([
            "Departamento",
            "Fecha",
            "Falla que presenta",
            "Servicio prestado",
            "Nombre del técnico",
            "Descripción",
            "Cantidad",
            "Observaciones"
        ])
        
        self.ui.tabla_servicios.setModel(modelo_vacio)
        
        if (mensaje):
            self.ui.lbl_errores_filtro_servicios.setText(mensaje)
    
    def generar_respaldo(self):
        try:
            ruta_respaldo = self.respaldo_local().exportar()
            self.mostrar_mensaje_info(f"El respaldo se generó correctamente en: {ruta_respaldo}")
        except Exception as error:
            self.mostrar_mensaje_error(f"No se pudo generar el respaldo porque: {error}")
    
    def importar_respaldo(self):
        titulo = "Seleccione el archivo de respaldo .sql"
        directorio_inicial = str(Path.home())
        filtro = "Archivos SQL (*.sql);;"
        
        ruta_archivo, filtro_archivo = QFileDialog.getOpenFileName(
            self.ui.ventanas,
            titulo,
            directorio_inicial,
            filtro
        )
        
        if (ruta_archivo):
            ruta_path = Path(ruta_archivo)
            
            if not(hasattr(self, "ventana_carga_importacion_bd")):
                from vistas.vistas_python.VentanaImportacionBD import VentanaImportacionBd
                self.ventana_carga_importacion_bd = VentanaImportacionBd("VentanaCargaImportacionBd.ui", "estilos_ventana_importacion_respaldo.qss")
            
            self.hilo_importar_respaldo_bd = HiloImportarRespaldoBD(
                self.respaldo_local,
                ruta_path
            )
            
            self.hilo_importar_respaldo_bd.resultado.connect(self._resultado_importacion)
            self.hilo_importar_respaldo_bd.start()
            
            self.ventana_carga_importacion_bd.ui.exec_()
    
    def _resultado_importacion(self, hubo_exito: bool, mensaje: str):
        if (self.ventana_carga_importacion_bd):
            self.ventana_carga_importacion_bd.ui.accept()
        
        if (hubo_exito):
            self.mostrar_mensaje_info(mensaje)
            self.filtrar_servicios()
        else:
            self.mostrar_mensaje_error(mensaje)
    
    def generar_reporte(self):
        if not(hasattr(self, "ventana_generar_reporte")):
            from vistas.vistas_python.VentanaGenerarReporte import VentanaGenerarReporte
            self.ventana_generar_reporte = VentanaGenerarReporte(
                ReporteServicios(),
                self._servicios,
                "VentanaGenerarReporte.ui",
                "estilos_ventana_generar_reporte.qss"
            )
            
        self.ventana_generar_reporte.ui.exec_()