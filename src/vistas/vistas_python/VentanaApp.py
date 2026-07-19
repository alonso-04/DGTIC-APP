from typing import List, Tuple
from pathlib import Path
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QColor, QRegExpValidator
from PyQt5.QtCore import QThread, pyqtSignal, QRegExp, QEvent
from PyQt5.QtWidgets import QHeaderView, QDialog, QFileDialog

from vistas.vistas_python.VentanaPrincipal import VentanaPrincipal
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


class VentanaApp:
    def __init__(self, ventana_principal: VentanaPrincipal):
        super().__init__()
        self.ventana_principal = ventana_principal
        
        # SERVICIOS
        self._servicios = ventana_principal._servicios
        
        self.respaldo_local = RespaldoLocal
        
        # FUNCIONES Y ELEMENTOS DE UTILIDAD
        self.mostrar_mensaje_error = self.ventana_principal.mostrar_mensaje_error
        self.mostrar_mensaje_info = self.ventana_principal.mostrar_mensaje_info
        self.labelErrorFiltro = self.ventana_principal.labelErrorFiltro
        self.cargar_completer_departamento = self.ventana_principal.cargar_completer_departamento
        self.cargar_completer_tipos_servicio = self.ventana_principal.cargar_completer_tipos_servicio
        self.cargar_manual_usuario = self.ventana_principal.ver_manual_usuario
        self.botonRefrescarApp = self.ventana_principal.botonRefrescarApp
        self.botonManualUsuarioSeccionApp = self.ventana_principal.botonManualUsuarioSeccionApp
        
        
        # SECCIÓN DE REGISTRAR NUEVO SERVICIO
        self.inputDepartamento = self.ventana_principal.inputDepartamento
        self.tbOtroDepartamento = self.ventana_principal.tbOtroDepartamento
        self.inputFallaPresenta = self.ventana_principal.inputFallaPresenta
        self.inputNombreTecnico = self.ventana_principal.inputNombreTecnico
        
        self.spCantidad = self.ventana_principal.spCantidad
        self.lineEditspCantidad = self.spCantidad.lineEdit()
        regex = QRegExp("[0-9]+")
        validador = QRegExpValidator(regex, self.lineEditspCantidad)
        self.lineEditspCantidad.setValidator(validador)
        self.lineEditspCantidad.installEventFilter(self.ventana_principal)
        
        self.teDescripcion = self.ventana_principal.teDescripcion
        self.inputServicioPrestado = self.ventana_principal.inputServicioPrestado
        self.tbOtroServicioPrestado = self.ventana_principal.tbOtroServicioPrestado
        self.teObservacionesAdicionales = self.ventana_principal.teObservacionesAdicionales
        self.deFecha = self.ventana_principal.deFecha
        self.botonRegistrar = self.ventana_principal.botonRegistrar
        
        
        # SECCIÓN DE FILTRAR SERVICIOS
        self.deFiltroFecha = self.ventana_principal.deFiltroFecha
        self.inputFiltroDepartamento = self.ventana_principal.inputFiltroDepartamento
        self.inputFiltroServicioPrestado = self.ventana_principal.inputFiltroServicioPrestado
        self.botonBuscarServicios = self.ventana_principal.botonBuscarServicios
        
        
        # SECCIÓN DE LA TABLA DE REGISTROS
        self.tvRegistros = self.ventana_principal.tvRegistros
        self.servicio_data = []
        
        
        # BOTONES INFERIORES
        self.botonCrearUsuario = self.ventana_principal.botonCrearUsuario
        self.botonCrearRespaldo = self.ventana_principal.botonCrearRespaldo
        self.botonImportarRespaldo = self.ventana_principal.botonImportarRespaldo
        self.botonGenerarReporte = self.ventana_principal.botonGenerarReporte
        self.botonCerrarSesion = self.ventana_principal.botonCerrarSesion
        
        self.configuracion()
    
    def eventFilter(self, obj, event):
        if obj is self.lineEditspCantidad and event.type() == QEvent.KeyPress:
            if event.text() == ',':
                return True  # Bloquea la coma del spCantidad
        return super().eventFilter(obj, event)
    
    def configuracion(self):
        self.cargar_completer_departamento()
        self.cargar_completer_tipos_servicio()
        
        self.botonRefrescarApp.clicked.connect(self.refrescar_pagina_app)
        self.botonManualUsuarioSeccionApp.clicked.connect(self.ver_manual_usuario)
        
        self.tbOtroDepartamento.clicked.connect(self.ir_pagina_crear_departamento)
        self.tbOtroServicioPrestado.clicked.connect(self.ir_pagina_crear_tipo_servicio)
        
        self.botonRegistrar.clicked.connect(self.registrar_nuevo_servicio)
        
        self.botonBuscarServicios.clicked.connect(self.filtrar_servicios)
        self.deFiltroFecha.dateChanged.connect(self.filtrar_servicios)
        self.tvRegistros.clicked.connect(self.seleccionar_servicio)
        
        self.botonCrearUsuario.clicked.connect(self.ir_pagina_crear_usuario)
        self.botonCrearRespaldo.clicked.connect(self.generar_respaldo)
        self.botonImportarRespaldo.clicked.connect(self.importar_respaldo)
        self.botonGenerarReporte.clicked.connect(self.generar_reporte)
        self.botonCerrarSesion.clicked.connect(self.cerrar_sesion)
    
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
        self.ventana_principal.ventanas.setCurrentWidget(self.ventana_principal.paginaIniciarSesion)
        self.ventana_principal.setWindowTitle("Iniciar Sesión")
    
    def ir_pagina_crear_usuario(self):
        if (self._servicios["usuario_servicio"].usuario_es_admin()):
            if not(hasattr(self, "ventana_usuarios")):
                from vistas.vistas_python.VentanaUsuarios import VentanaUsuarios
                self.ventana_usuarios = VentanaUsuarios(self.ventana_principal)
                
            self.ventana_principal.ventanas.setCurrentWidget(self.ventana_principal.paginaCrearUsuario)
            self.ventana_principal.setWindowTitle("Usuarios")
        else:
            self.mostrar_mensaje_error("No puedes entrar a esta sección porque no eres Administrador.")
    
    def ir_pagina_crear_departamento(self):
        if not(hasattr(self, "ventana_departamentos")):
            from vistas.vistas_python.VentanaDepartamento import VentanaDepartamentos
            self.ventana_departamentos = VentanaDepartamentos(self.ventana_principal)
        
        self.ventana_principal.ventanas.setCurrentWidget(self.ventana_principal.paginaDepartamentos)
        self.ventana_principal.setWindowTitle("Departamentos")
    
    def ir_pagina_crear_tipo_servicio(self):
        if not(hasattr(self, "ventana_tipos_servicio")):
            from vistas.vistas_python.VentanaTiposServicio import VentanaTipoServicio
            self.ventana_tipos_servicio = VentanaTipoServicio(self.ventana_principal)
        
        self.ventana_principal.ventanas.setCurrentWidget(self.ventana_principal.paginaTiposServicio)
        self.ventana_principal.setWindowTitle("Tipos de servicio")
    
    def registrar_nuevo_servicio(self):
        try:
            nombre_departamento = self.inputDepartamento.text()
            falla_presenta = self.inputFallaPresenta.text()
            nombres_tecnicos = self.inputNombreTecnico.text()
            cantidad = self.spCantidad.value()
            descripcion = self.teDescripcion.toPlainText()
            servicio_prestado = self.inputServicioPrestado.text()
            fecha_servicio = self.deFecha.date().toPyDate()
            observaciones_adicionales = self.teObservacionesAdicionales.toPlainText()
            
            self._servicios["servicio_tecnico_servicio"].registrar(
                nombre_departamento,
                fecha_servicio,
                falla_presenta.upper(),
                servicio_prestado,
                nombres_tecnicos.upper(),
                cantidad,
                descripcion.upper(),
                observaciones_adicionales.upper()
            )
            
            self.inputDepartamento.clear()
            self.inputFallaPresenta.clear()
            self.inputNombreTecnico.clear()
            self.spCantidad.setValue(1)
            self.teDescripcion.clear()
            self.inputServicioPrestado.clear()
            self.teObservacionesAdicionales.clear()
            
            self.filtrar_servicios()
        except NoEncontradoError as error:
            self.mostrar_mensaje_error("\n".join(error.errores))
        except ValidacionError as error:
            self.mostrar_mensaje_error("\n".join(error.errores))
        except LogicaError as error:
            self.mostrar_mensaje_error("\n".join(error.errores))
    
    def filtrar_servicios(self):
        try:
            fecha_servicio = self.deFiltroFecha.date().toPyDate()
            nombre_departamento = self.inputFiltroDepartamento.text()
            tipo_servicio_prestado = self.inputFiltroServicioPrestado.text()
                
            servicios = self._servicios["servicio_tecnico_servicio"].obtener_por_fecha_o_departamento_o_tipo_servicio(
                fecha_servicio,
                nombre_departamento,
                tipo_servicio_prestado
            )
            
            self.servicio_data = servicios
            
            modelo_datos = QStandardItemModel(len(servicios), 6)
            modelo_datos.setHorizontalHeaderLabels([
                "Departamento",
                "Fecha",
                "Falla que presenta",
                "Servicio prestado",
                "Nombre del técnico",
                "Descripción",
                "Cantidad",
                "Observaciones"
            ])
            
            COLOR_RESALTE = QColor(255, 240, 180)
            
            for fila, servicio in enumerate(servicios):
                descripcion = servicio[8] if servicio[8] else ""
                observacion_adicional = servicio[10] if servicio[10] else ""
                fecha_servicio_formateada = servicio[4].strftime("%d-%m-%Y")
                
                items = [
                    QStandardItem(str(servicio[3])),
                    QStandardItem(fecha_servicio_formateada),
                    QStandardItem(str(servicio[5])),
                    QStandardItem(str(servicio[6])),
                    QStandardItem(str(servicio[7])),
                    QStandardItem(descripcion),
                    QStandardItem(str(servicio[9])),
                    QStandardItem(observacion_adicional)
                ]
                
                if (observacion_adicional):
                    for item in items:
                        item.setBackground(COLOR_RESALTE)
                
                for col, item in enumerate(items):
                    item.setToolTip(item.text())
                    modelo_datos.setItem(fila, col, item)
            
            self.tvRegistros.setModel(modelo_datos)
            self.labelErrorFiltro.clear()
            
            header = self.tvRegistros.horizontalHeader()
            header.setSectionResizeMode(QHeaderView.Stretch)
        except NoEncontradoError as error:
            self.servicio_data = []
            self.limpiar_tabla("\n".join(error.errores))
            header = self.tvRegistros.horizontalHeader()
            header.setSectionResizeMode(QHeaderView.Stretch)
    
    def seleccionar_servicio(self, indice: int):
        fila_seleccionada = indice.row()
        
        if ((fila_seleccionada >= 0) and (fila_seleccionada < len(self.servicio_data))):
            servicio_seleccionado = self.servicio_data[fila_seleccionada]
            self.mostrar_ventana_info_servicio(servicio_seleccionado)
    
    def mostrar_ventana_info_servicio(self, servicio_data: List[Tuple]):
        if not(hasattr(self, "ventana_info_servicio")):
            from vistas.vistas_python.VentanaInfoServicio import VentanaInfoServicio
            self.ventana_info_servicio = VentanaInfoServicio(servicio_data, self._servicios)
        
        self.ventana_info_servicio.actualizar_data_recibida(servicio_data)
        
        resultado = self.ventana_info_servicio.exec_()
        if (resultado == QDialog.Accepted):
            self.filtrar_servicios()
    
    def mostrar_error_filtro(self, mensaje: str):
        self.labelErrorFiltro.setText(mensaje)
    
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
        
        self.tvRegistros.setModel(modelo_vacio)
        
        if (mensaje):
            self.labelErrorFiltro.setText(mensaje)
    
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
            self.ventana_principal.ventanas,
            titulo,
            directorio_inicial,
            filtro
        )
        
        if (ruta_archivo):
            ruta_path = Path(ruta_archivo)
            
            if not(hasattr(self, "ventana_carga_importacion_bd")):
                from vistas.vistas_python.VentanaImportacionBD import VentanaImportacionBd
                self.ventana_carga_importacion_bd = VentanaImportacionBd()
            
            self.hilo_importar_respaldo_bd = HiloImportarRespaldoBD(
                self.respaldo_local,
                ruta_path
            )
            
            self.hilo_importar_respaldo_bd.resultado.connect(self._resultado_importacion)
            self.hilo_importar_respaldo_bd.start()
            
            self.ventana_carga_importacion_bd.exec_()
    
    def _resultado_importacion(self, hubo_exito: bool, mensaje: str):
        if (self.ventana_carga_importacion_bd):
            self.ventana_carga_importacion_bd.accept()
        
        if (hubo_exito):
            self.mostrar_mensaje_info(mensaje)
            self.filtrar_servicios()
        else:
            self.mostrar_mensaje_error(mensaje)
    
    def generar_reporte(self):
        if not(hasattr(self, "ventana_generar_reporte")):
            from vistas.vistas_python.VentanaGenerarReporte import VentanaGenerarReporte
            self.ventana_generar_reporte = VentanaGenerarReporte(
                generador_reporte_servicios = ReporteServicios(),
                servicios = self._servicios
            )
            
        self.ventana_generar_reporte.exec_()