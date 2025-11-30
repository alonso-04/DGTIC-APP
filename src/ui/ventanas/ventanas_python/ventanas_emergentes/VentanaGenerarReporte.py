from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5.QtCore import QDate, Qt, QThread, pyqtSignal
from ui.ventanas.ventanas_pyuic.VentanaGenerarReportePyuic import Ui_VentanaGenerarReporte
from dominio.excepciones import ServicioValidacionError


class ReporteTrabajador(QThread):
    # SEÑALES QUE SE USARÁN PARA COMUNICAR EL ESTADO A LA UI
    SENIAL_EXITO = pyqtSignal()
    SENIAL_ERROR = pyqtSignal(Exception)
    SENIAL_ACTUALIZAR_ESTADO = pyqtSignal(str)
    
    def __init__(self, generador_reporte_mensual, mes_anio: str):
        super().__init__()
        self.generador_reporte_mensual = generador_reporte_mensual
        self.mes_anio = mes_anio
    
    def run(self):
        try:            
            # CARGA DE DATOS
            datos = self.generador_reporte_mensual.cargar_datos(self.mes_anio)
            
            #1. NOTIFICAR ESTADO: EXPORTACIÓN
            self.SENIAL_ACTUALIZAR_ESTADO.emit("Exportando reporte a archivo...")
            
            # EXPORTACIÓN
            self.generador_reporte_mensual.exportar(datos)
            
            #2. ÉXITO: EMITIR SEÑAL DE FINALIZACIÓN EXITOSA
            self.SENIAL_EXITO.emit()
        except Exception as error:
            #3. ERROR: EMITIR SEÑAL DE ERROR EN CASO DE FALLAS 
            self.SENIAL_ERROR.emit(error)


class VentanaGenerarReporte(QDialog, Ui_VentanaGenerarReporte):
    def __init__(self, generador_reporte_mensual):
        super().__init__()
        self.setupUi(self)
        
        self.setWindowFlags(
            Qt.WindowSystemMenuHint |
            Qt.WindowTitleHint |
            Qt.WindowCloseButtonHint
        )
        
        self.generador_reporte_mensual = generador_reporte_mensual
        self.configuracion()
        
        self.reporte_trabajador = None
    
    def configuracion(self):
        self.deFechaReporte.setDate(QDate.currentDate())
        
        self.botonGenerarReporteServicio.clicked.connect(self.generar_reporte)
        self.botonCancelarReporteServicio.clicked.connect(self.reject)
        
        self.barraProgresoReporte.hide()
    
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
            mes_anio_reporte_date = self.deFechaReporte.date()
            mes_anio_reporte_string = mes_anio_reporte_date.toString("MM-yyyy")
            
            #1. CONFIGURAR LA UI A ESTADO DE "OCUPADO"
            self.establecer_modo_ocupado(True, "Iniciando...")
            
            #2. INICIAR Y CONFIGURAR EL TRABAJADOR
            self.reporte_trabajador = ReporteTrabajador(
                self.generador_reporte_mensual,
                mes_anio_reporte_string
            )
            
            #3. CONECTAR LAS SEÑALES A LOS SLOTS
            self.reporte_trabajador.SENIAL_ACTUALIZAR_ESTADO.connect(self.actualizar_mensaje_estado)
            self.reporte_trabajador.SENIAL_EXITO.connect(self.reporte_exitoso)
            self.reporte_trabajador.SENIAL_ERROR.connect(self.reporte_fallido)
            
            self.reporte_trabajador.start()
        except Exception as error:
            self.establecer_modo_ocupado(False, "Error al iniciar el proceso")
            QMessageBox.critical(self, "Error al iniciar el proceso", f"{error}")
    
    def actualizar_mensaje_estado(self, mensaje: str):
        self.labelEstadoReporte.setText(mensaje)
    
    def reporte_exitoso(self):
        self.establecer_modo_ocupado(False, "Reporte generado con éxito")
        
        QMessageBox.information(self, "Éxito", "Se ha generado el reporte correctamente.")
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