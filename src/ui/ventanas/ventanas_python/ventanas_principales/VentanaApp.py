from PyQt5.QtGui import QStandardItemModel, QStandardItem, QColor
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QHeaderView, QDialog, QFileDialog
from ui.ventanas.ventanas_python.ventanas_principales.VentanaPrincipal import VentanaPrincipal
from ui.ventanas.ventanas_python.ventanas_info.VentanaInfoServicio import VentanaInfoServicio
from ui.ventanas.ventanas_python.ventanas_emergentes.VentanaGenerarReporte import VentanaGenerarReporte
from ui.ventanas.ventanas_python.ventanas_emergentes.VentanaImportacionBd import VentanaImportacionBd
from dominio.excepciones import ServicioValidacionError, DepartamentoValidacionError, TipoServicioValidacionError
from infraestructura.conexiones.respaldo import RespaldoLocal
from infraestructura.reportes.reporte_servicios import ReporteServicios
from typing import Dict
from pathlib import Path


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
        
        self.respaldo_local = RespaldoLocal
        
        # FUNCIONES Y ELEMENTOS DE UTILIDAD
        self.mostrar_mensaje_error = self.ventana_principal.mostrar_mensaje_error
        self.mostrar_mensaje_info = self.ventana_principal.mostrar_mensaje_info
        self.esta_vacio = self.ventana_principal.esta_vacio
        self.labelErrorFiltro = self.ventana_principal.labelErrorFiltro
        self.cargar_completer_departamento = self.ventana_principal.cargar_completer_departamento
        self.cargar_completer_tipos_servicio = self.ventana_principal.cargar_completer_tipos_servicio
        self.botonRefrescarApp = self.ventana_principal.botonRefrescarApp
        
        # CONTROLADORES
        self.usuario_controlador = self.ventana_principal.usuario_controlador
        self.servicio_controlador = self.ventana_principal.servicio_controlador
        
        
        # SECCIÓN DE REGISTRAR NUEVO SERVICIO
        self.inputDepartamento = self.ventana_principal.inputDepartamento
        self.tbOtroDepartamento = self.ventana_principal.tbOtroDepartamento
        self.inputFallaPresenta = self.ventana_principal.inputFallaPresenta
        self.inputNombreTecnico = self.ventana_principal.inputNombreTecnico
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
    
    def configuracion(self):
        self.cargar_completer_departamento()
        self.cargar_completer_tipos_servicio()
        
        self.botonRefrescarApp.clicked.connect(self.refrescar_pagina_app)
        
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
    
    def cerrar_sesion(self):
        self.usuario_controlador.cerrar_sesion_controlador()
        self.ir_pagina_inicio_sesion()
    
    def ir_pagina_inicio_sesion(self):
        self.ventana_principal.ventanas.setCurrentWidget(self.ventana_principal.paginaIniciarSesion)
        self.ventana_principal.setWindowTitle("Iniciar Sesión")
    
    def ir_pagina_crear_usuario(self):
        if (self.usuario_controlador.usuario_es_admin()):
            self.ventana_principal.ventanas.setCurrentWidget(self.ventana_principal.paginaCrearUsuario)
            self.ventana_principal.setWindowTitle("Usuarios")
        else:
            self.mostrar_mensaje_error("No puedes entrar a esta sección porque no eres Administrador.")
    
    def ir_pagina_crear_departamento(self):
        self.ventana_principal.ventanas.setCurrentWidget(self.ventana_principal.paginaDepartamentos)
        self.ventana_principal.setWindowTitle("Departamentos")
        self.ventana_principal.botonBuscarDepartamento.click()
    
    def ir_pagina_crear_tipo_servicio(self):
        self.ventana_principal.ventanas.setCurrentWidget(self.ventana_principal.paginaTiposServicio)
        self.ventana_principal.setWindowTitle("Tipos de servicio")
        self.ventana_principal.botonBuscarTipoServicio.click()
    
    def registrar_nuevo_servicio(self):
        try:
            nombre_departamento = self.inputDepartamento.text()
            falla_presenta = self.inputFallaPresenta.text()
            nombres_tecnicos = self.inputNombreTecnico.text()
            servicio_prestado = self.inputServicioPrestado.text()
            fecha_servicio = self.deFecha.date().toPyDate()
            observaciones_adicionales = self.teObservacionesAdicionales.toPlainText()
            
            if (self.esta_vacio(nombre_departamento)):
                nombre_departamento = None
            
            if (self.esta_vacio(servicio_prestado)):
                servicio_prestado = None
            
            if (self.esta_vacio(observaciones_adicionales)):
                observaciones_adicionales = None
            
            if (self.esta_vacio(nombres_tecnicos)):
                nombres_tecnicos = None
            
            self.servicio_controlador.registrar_servicio_controlador(
                nombre_departamento = nombre_departamento,
                fecha_servicio = fecha_servicio,
                falla_presenta = falla_presenta,
                tipo_servicio_prestado = servicio_prestado,
                nombres_tecnicos = nombres_tecnicos,
                observaciones_adicionales = observaciones_adicionales
            )
            
            self.inputDepartamento.clear()
            self.inputFallaPresenta.clear()
            self.inputNombreTecnico.clear()
            self.inputServicioPrestado.clear()
            self.teObservacionesAdicionales.clear()
            
            self.filtrar_servicios()
        except ServicioValidacionError as error:
            self.mostrar_mensaje_error("\n".join(error.errores))
        except DepartamentoValidacionError as error:
            self.mostrar_mensaje_error("\n".join(error.errores))
        except TipoServicioValidacionError as error:
            self.mostrar_mensaje_error("\n".join(error.errores))
    
    def filtrar_servicios(self):
        try:
            fecha_servicio = self.deFiltroFecha.date().toPyDate()
            nombre_departamento = self.inputFiltroDepartamento.text()
            tipo_servicio_prestado = self.inputFiltroServicioPrestado.text()
            
            servicios = self.servicio_controlador.filtrar_servicios_controlador(
                fecha_servicio = fecha_servicio,
                nombre_departamento = nombre_departamento,
                tipo_servicio_prestado = tipo_servicio_prestado
            )
            
            self.servicio_data = servicios
                
            if not(servicios):
                self.servicio_data = []
                return
                
            modelo_datos = QStandardItemModel(len(servicios), 6)
            modelo_datos.setHorizontalHeaderLabels([
                "Departamento",
                "Fecha",
                "Falla que presenta",
                "Servicio prestado",
                "Nombre del técnico",
                "Observaciones"
            ])
            
            COLOR_RESALTE = QColor(255, 240, 180)
                
            for fila, servicio in enumerate(servicios):
                observacion_adicional = servicio["observaciones_adicionales"]
                if (self.esta_vacio(observacion_adicional)):
                    observacion_adicional = ""
                
                items = [
                    QStandardItem(str(servicio["nombre_departamento"])),
                    QStandardItem(str(servicio["fecha_servicio"])),
                    QStandardItem(str(servicio["falla_presenta"])),
                    QStandardItem(str(servicio["tipo_servicio_prestado"])),
                    QStandardItem(str(servicio["nombres_tecnicos"])),
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
        except ServicioValidacionError as error:
            self.limpiar_tabla("\n".join(error.errores))
            self.servicio_data = []
        finally:
            header = self.tvRegistros.horizontalHeader()
            header.setSectionResizeMode(QHeaderView.Stretch)
    
    def seleccionar_servicio(self, indice):
        fila_seleccionada = indice.row()
        
        if ((fila_seleccionada >= 0) and (fila_seleccionada < len(self.servicio_data))):
            servicio_seleccionado = self.servicio_data[fila_seleccionada]
            self.mostrar_ventana_info_servicio(servicio_seleccionado)
    
    def mostrar_ventana_info_servicio(self, servicio_data: Dict):
        try:
            ventana_info_servicio = VentanaInfoServicio(
                servicio_data = servicio_data,
                servicio_controlador = self.servicio_controlador
            )
            
            resultado = ventana_info_servicio.exec_()
            
            if (resultado == QDialog.Accepted):
                self.filtrar_servicios()
        except Exception as error:
            self.mostrar_mensaje_error(f"Error al mostrar la ventana de la info del servicio: {error}")
    
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
            
            self.ventana_carga_importacion_bd = VentanaImportacionBd()
            
            self.hilo_importar_respaldo_bd = HiloImportarRespaldoBD(
                self.respaldo_local,
                ruta_path
            )
            
            self.hilo_importar_respaldo_bd.resultado.connect(self._resultado_importacion)
            self.hilo_importar_respaldo_bd.start()
            
            self.ventana_carga_importacion_bd.exec_()
            
            self.filtrar_servicios()
    
    def _resultado_importacion(self, hubo_exito: bool, mensaje: str):
        if (self.ventana_carga_importacion_bd):
            self.ventana_carga_importacion_bd.accept()
        
        if (hubo_exito):
            self.mostrar_mensaje_info(mensaje)
        else:
            self.mostrar_mensaje_error(mensaje)
    
    def generar_reporte(self):
        try:
            ventana_generar_reporte = VentanaGenerarReporte(
                generador_reporte_servicios = ReporteServicios()
            )
            
            ventana_generar_reporte.exec_()
        except Exception as error:
            self.mostrar_mensaje_error(f"Error al mostrar la ventana de generar reporte: {error}")