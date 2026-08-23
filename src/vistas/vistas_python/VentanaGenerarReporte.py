from typing import Optional
from datetime import date
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import QDate, Qt, QThread, pyqtSignal

from utilidades.gui import UiBase
from vistas.utilidades_gui.cargar_completers import cargar_completer
from configuraciones.excepciones import NoEncontradoError, ValidacionError


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


class VentanaGenerarReporte(UiBase):
    def __init__(self, generador_reporte_servicios, servicios, nombre_archivo_ui: str, nombre_archivo_estilos: str):
        super().__init__(nombre_archivo_ui, nombre_archivo_estilos)
        
        self.ui.setWindowFlags(
            Qt.WindowSystemMenuHint |
            Qt.WindowTitleHint |
            Qt.WindowCloseButtonHint
        )
        
        self.generador_reporte_servicios = generador_reporte_servicios
        self._servicios = servicios
        
        lista_campos_tipos_servicio_completers = [self.ui.txt_tipo_servicio_reporte]
        self.cargar_completer_tipos_servicio = lambda: cargar_completer(
            self._servicios["tipo_servicio_tecnico_servicio"],
            lista_campos_tipos_servicio_completers,
            "tipo_servicio"
        )
        
        self.configuracion()
        
        self.reporte_trabajador = None
    
    def configuracion(self):
        self.ui.cb_tipo_reporte.currentIndexChanged.connect(self.seleccionar_opcion)
        
        self.ui.de_fecha_reporte_mensual.setDate(QDate.currentDate())
        self.ui.de_fecha_reporte_desde.setDate(QDate.currentDate())
        self.ui.de_fecha_reporte_hasta.setDate(QDate.currentDate())
        self.ui.de_fecha_reporte_anual.setDate(QDate.currentDate())
        
        self.ui.btn_exportar_reporte.clicked.connect(self.generar_reporte)
        self.ui.btn_cancelar.clicked.connect(self.ui.reject)
        
        self.ui.barra_carga_reporte.hide()
        
        self.seleccionar_opcion(0)
        self.cargar_completer_tipos_servicio()
    
    def seleccionar_opcion(self, indice: int):
        opcion_seleccionada = self.ui.cb_tipo_reporte.itemText(indice)
        
        if (indice == 0):
            self.ui.de_fecha_reporte_desde.setEnabled(False)
            self.ui.de_fecha_reporte_hasta.setEnabled(False)
            self.ui.de_fecha_reporte_anual.setEnabled(False)
            
            self.ui.de_fecha_reporte_mensual.setEnabled(True)
        
        if (indice == 1):
            opcion_seleccionada = "RANGO_FECHA"
            
            self.ui.de_fecha_reporte_anual.setEnabled(False)
            self.ui.de_fecha_reporte_mensual.setEnabled(False)
            
            self.ui.de_fecha_reporte_desde.setEnabled(True)
            self.ui.de_fecha_reporte_hasta.setEnabled(True)
        
        if (indice == 2):
            self.ui.de_fecha_reporte_mensual.setEnabled(False)
            self.ui.de_fecha_reporte_desde.setEnabled(False)
            self.ui.de_fecha_reporte_hasta.setEnabled(False)
            
            self.ui.de_fecha_reporte_anual.setEnabled(True)
        
        return opcion_seleccionada
    
    def establecer_modo_ocupado(self, ocupado, texto_estado: str = ""):
        self.ui.btn_exportar_reporte.setEnabled(not ocupado)
        self.ui.btn_cancelar.setEnabled(not ocupado)
        
        if (ocupado):
            self.ui.barra_carga_reporte.setRange(0, 0)
            self.ui.barra_carga_reporte.show()
            self.ui.lbl_estado_reporte.setText(texto_estado)
        else:
            self.ui.barra_carga_reporte.setRange(0, 100)
            self.ui.barra_carga_reporte.hide()
            self.ui.lbl_estado_reporte.setText(texto_estado)
    
    def generar_reporte(self):
        try:
            indice_opcion_seleccionada = self.ui.cb_tipo_reporte.currentIndex()
            opcion_seleccionada = self.seleccionar_opcion(indice_opcion_seleccionada)
            
            tipo_servicio_prestado = self.ui.txt_tipo_servicio_reporte.text()
            tipo_servicio_prestado_sin_espacios = tipo_servicio_prestado.replace(" ", "")
                
            if (len(tipo_servicio_prestado_sin_espacios) == 0):
                tipo_servicio_prestado = None
            
            if (indice_opcion_seleccionada == 0):
                mes_anio_reporte_date = self.ui.de_fecha_reporte_mensual.date()
                mes_anio_reporte_string = mes_anio_reporte_date.toString("MM-yyyy")
                
                self.reporte_trabajador = HiloReporteServicio(
                    generador_reporte_servicios = self.generador_reporte_servicios,
                    opcion_seleccionada = opcion_seleccionada,
                    mes_anio = mes_anio_reporte_string,
                    tipo_servicio_prestado = tipo_servicio_prestado
                )
            
            if (indice_opcion_seleccionada == 1):
                fecha_desde = self.ui.de_fecha_reporte_desde.date().toPyDate()
                fecha_hasta = self.ui.de_fecha_reporte_hasta.date().toPyDate()
                
                self.reporte_trabajador = HiloReporteServicio(
                    generador_reporte_servicios = self.generador_reporte_servicios,
                    opcion_seleccionada = opcion_seleccionada,
                    fecha_desde = fecha_desde,
                    fecha_hasta = fecha_hasta,
                    tipo_servicio_prestado = tipo_servicio_prestado
                )
            
            if (indice_opcion_seleccionada == 2):
                anio_date = self.ui.de_fecha_reporte_anual.date()
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
            QMessageBox.critical(self.ui, "Error al iniciar el proceso", f"{error}")
    
    def actualizar_mensaje_estado(self, mensaje: str):
        self.ui.lbl_estado_reporte.setText(mensaje)
    
    def reporte_exitoso(self, RUTA_REPORTE_GENERADO: str):
        self.establecer_modo_ocupado(False, "Reporte generado con éxito")
        self.ui.txt_tipo_servicio_reporte.clear()
        
        QMessageBox.information(self.ui, "Éxito", f"Se ha generado el reporte correctamente en {RUTA_REPORTE_GENERADO}")
        self.ui.accept()
    
    def reporte_fallido(self, error: Exception):
        self.establecer_modo_ocupado(False, "Error al generar el reporte")
        
        if isinstance(error, NoEncontradoError):
            QMessageBox.critical(self.ui, "Error", "\n".join(error.errores))
        elif isinstance(error, ValidacionError):
            QMessageBox.critical(self.ui, "Error", "\n".join(error.errores))
        else:
            QMessageBox.critical(self.ui, "Error", f"{error}")
        
        if (self.reporte_trabajador):
            self.reporte_trabajador.wait()
            self.reporte_trabajador = None