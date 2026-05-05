from PyQt5.QtWidgets import QDialog, QMessageBox, QCompleter
from PyQt5.QtCore import QDate, Qt, QThread, pyqtSignal
from ui.ventanas.ventanas_pyuic.VentanaGenerarReportePyuic import Ui_VentanaGenerarReporte
from dominio.excepciones import ServicioValidacionError
from typing import Optional
from datetime import date


class HiloReporteServicio(QThread):
    # SEÑALES QUE SE USARÁN PARA COMUNICAR EL ESTADO A LA UI
    SENIAL_EXITO = pyqtSignal(str)
    SENIAL_ERROR = pyqtSignal(Exception)
    SENIAL_ACTUALIZAR_ESTADO = pyqtSignal(str)
    
    def __init__(
        self,
        generador_reporte_servicios,
        opcion_seleccionada: str,
        mes_anio: Optional[str] = None,
        fecha_desde: Optional[date] = None,
        fecha_hasta: Optional[date] = None,
        anio: Optional[str] = None,
        tipo_servicio_prestado: Optional[str] = None
    ):
        super().__init__()
        self.generador_reporte_servicios = generador_reporte_servicios
        self.opcion_seleccionada = opcion_seleccionada
        self.mes_anio = mes_anio
        self.fecha_desde = fecha_desde
        self.fecha_hasta = fecha_hasta
        self.anio = anio
        self.tipo_servicio_prestado = tipo_servicio_prestado
    
    def run(self):
        try:            
            # CARGA DE DATOS
            datos = self.generador_reporte_servicios.cargar_datos(
                self.opcion_seleccionada,
                self.mes_anio,
                self.fecha_desde,
                self.fecha_hasta,
                self.anio,
                self.tipo_servicio_prestado
            )
            
            #1. NOTIFICAR ESTADO: EXPORTACIÓN
            self.SENIAL_ACTUALIZAR_ESTADO.emit("Exportando reporte a archivo...")
            
            # EXPORTACIÓN
            RUTA_REPORTE_GENERADO = self.generador_reporte_servicios.exportar(datos)
            
            #2. ÉXITO: EMITIR SEÑAL DE FINALIZACIÓN EXITOSA
            self.SENIAL_EXITO.emit(RUTA_REPORTE_GENERADO)
        except Exception as error:
            #3. ERROR: EMITIR SEÑAL DE ERROR EN CASO DE FALLAS 
            self.SENIAL_ERROR.emit(error)


class VentanaGenerarReporte(QDialog, Ui_VentanaGenerarReporte):
    def __init__(self, generador_reporte_servicios, servicio_controlador):
        super().__init__()
        self.setupUi(self)
        
        self.setWindowFlags(
            Qt.WindowSystemMenuHint |
            Qt.WindowTitleHint |
            Qt.WindowCloseButtonHint
        )
        
        self.generador_reporte_servicios = generador_reporte_servicios
        self.servicio_controlador = servicio_controlador
        
        self.configuracion()
        
        self.reporte_trabajador = None
    
    def configuracion(self):
        self.cbTipoReporte.currentIndexChanged.connect(self.seleccionar_opcion)
        
        self.deFechaReporte.setDate(QDate.currentDate())
        self.deFechaDesde.setDate(QDate.currentDate())
        self.deFechaHasta.setDate(QDate.currentDate())
        self.deOpcionAnual.setDate(QDate.currentDate())
        
        self.botonGenerarReporteServicio.clicked.connect(self.generar_reporte)
        self.botonCancelarReporteServicio.clicked.connect(self.reject)
        
        self.barraProgresoReporte.hide()
        
        self.seleccionar_opcion(0)
        self.cargar_completer_tipos_servicio()
    
    def cargar_completer_tipos_servicio(self):
        tipos_servicio = self.servicio_controlador.filtrar_todos_tipos_servicio_controlador()
        nombres_tipo_servicio = []
        
        for tipo_servicio in tipos_servicio:
            nombres_tipo_servicio.append(tipo_servicio["tipo_servicio_prestado"])
        
        if (tipos_servicio):
            completer_tipos_servicio = QCompleter(nombres_tipo_servicio)
            completer_tipos_servicio.setCaseSensitivity(Qt.CaseInsensitive)
            completer_tipos_servicio.setFilterMode(Qt.MatchContains)
            completer_tipos_servicio.setCompletionMode(QCompleter.PopupCompletion)
            
            self.inputTipoServicio.setCompleter(completer_tipos_servicio)
    
    def seleccionar_opcion(self, indice):
        opcion_seleccionada = self.cbTipoReporte.itemText(indice)
        
        if (indice == 0):
            self.deFechaDesde.setEnabled(False)
            self.deFechaHasta.setEnabled(False)
            self.deOpcionAnual.setEnabled(False)
            
            self.deFechaReporte.setEnabled(True)
        
        if (indice == 1):
            opcion_seleccionada = "RANGO_FECHA"
            
            self.deOpcionAnual.setEnabled(False)
            self.deFechaReporte.setEnabled(False)
            
            self.deFechaDesde.setEnabled(True)
            self.deFechaHasta.setEnabled(True)
        
        if (indice == 2):
            self.deFechaReporte.setEnabled(False)
            self.deFechaDesde.setEnabled(False)
            self.deFechaHasta.setEnabled(False)
            
            self.deOpcionAnual.setEnabled(True)
        
        return opcion_seleccionada
    
    def establecer_modo_ocupado(self, ocupado, texto_estado: str = ""):
        self.botonGenerarReporteServicio.setEnabled(not ocupado)
        self.botonCancelarReporteServicio.setEnabled(not ocupado)
        
        if (ocupado):
            self.barraProgresoReporte.setRange(0, 0)
            self.barraProgresoReporte.show()
            self.labelEstadoReporte.setText(texto_estado)
        else:
            self.barraProgresoReporte.setRange(0, 100)
            self.barraProgresoReporte.hide()
            self.labelEstadoReporte.setText(texto_estado)
    
    def generar_reporte(self):
        try:
            indice_opcion_seleccionada = self.cbTipoReporte.currentIndex()
            opcion_seleccionada = self.seleccionar_opcion(indice_opcion_seleccionada)
            
            tipo_servicio_prestado = self.inputTipoServicio.text()
            tipo_servicio_prestado_sin_espacios = tipo_servicio_prestado.replace(" ", "")
                
            if (len(tipo_servicio_prestado_sin_espacios) == 0):
                tipo_servicio_prestado = None
            
            if (indice_opcion_seleccionada == 0):
                mes_anio_reporte_date = self.deFechaReporte.date()
                mes_anio_reporte_string = mes_anio_reporte_date.toString("MM-yyyy")
                
                self.reporte_trabajador = HiloReporteServicio(
                    generador_reporte_servicios = self.generador_reporte_servicios,
                    opcion_seleccionada = opcion_seleccionada,
                    mes_anio = mes_anio_reporte_string,
                    tipo_servicio_prestado = tipo_servicio_prestado
                )
            
            if (indice_opcion_seleccionada == 1):
                fecha_desde = self.deFechaDesde.date().toPyDate()
                fecha_hasta = self.deFechaHasta.date().toPyDate()
                
                self.reporte_trabajador = HiloReporteServicio(
                    generador_reporte_servicios = self.generador_reporte_servicios,
                    opcion_seleccionada = opcion_seleccionada,
                    fecha_desde = fecha_desde,
                    fecha_hasta = fecha_hasta,
                    tipo_servicio_prestado = tipo_servicio_prestado
                )
            
            if (indice_opcion_seleccionada == 2):
                anio_date = self.deOpcionAnual.date()
                anio_string = anio_date.toString("yyyy")
                
                self.reporte_trabajador = HiloReporteServicio(
                    generador_reporte_servicios = self.generador_reporte_servicios,
                    opcion_seleccionada = opcion_seleccionada,
                    anio = anio_string,
                    tipo_servicio_prestado = tipo_servicio_prestado
                )
            
            self.establecer_modo_ocupado(True, "Iniciando...")
            
            self.reporte_trabajador.SENIAL_ACTUALIZAR_ESTADO.connect(self.actualizar_mensaje_estado)
            self.reporte_trabajador.SENIAL_EXITO.connect(self.reporte_exitoso)
            self.reporte_trabajador.SENIAL_ERROR.connect(self.reporte_fallido)
            
            self.reporte_trabajador.start()
        except Exception as error:
            self.establecer_modo_ocupado(False, "Error al iniciar el proceso")
            QMessageBox.critical(self, "Error al iniciar el proceso", f"{error}")
    
    def actualizar_mensaje_estado(self, mensaje: str):
        self.labelEstadoReporte.setText(mensaje)
    
    def reporte_exitoso(self, RUTA_REPORTE_GENERADO: str):
        self.establecer_modo_ocupado(False, "Reporte generado con éxito")
        self.inputTipoServicio.clear()
        
        QMessageBox.information(self, "Éxito", f"Se ha generado el reporte correctamente en {RUTA_REPORTE_GENERADO}")
        self.accept()
    
    def reporte_fallido(self, error):
        self.establecer_modo_ocupado(False, "Error al generar el reporte")
        
        if isinstance(error, ServicioValidacionError):
            QMessageBox.critical(self, "Error", "\n".join(error.errores))
        else:
            QMessageBox.critical(self, "Error", f"{error}")
        
        if (self.reporte_trabajador):
            self.reporte_trabajador.wait()
            self.reporte_trabajador = None