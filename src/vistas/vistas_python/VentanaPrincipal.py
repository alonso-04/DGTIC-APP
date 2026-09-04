from typing import Dict
from PyQt5.QtWidgets import QMessageBox, QLineEdit
from PyQt5.QtCore import QDate, QThread, pyqtSignal
from PyQt5.QtGui import QIcon

from utilidades.gui import UiBase
from configuraciones.excepciones import ValidacionError


class HiloIniciarSesion(QThread):
    exito = pyqtSignal(bool, str)
    error = pyqtSignal(str)

    def __init__(self, usuario_servicio, nombre_usuario, clave_usuario):
        super().__init__()
        self.usuario_servicio = usuario_servicio
        self.nombre_usuario = nombre_usuario
        self.clave_usuario = clave_usuario

    def run(self):
        try:
            self.usuario_servicio.iniciar_sesion(
                self.nombre_usuario,
                self.clave_usuario
            )
            self.exito.emit(True, "")
        except ValidacionError as error:
            self.error.emit("\n".join(error.errores))


class VentanaPrincipal(UiBase):
    def __init__(self, servicios: Dict, nombre_archivo_ui: str, nombre_archivo_estilos: str):
        super().__init__(nombre_archivo_ui, nombre_archivo_estilos)
        
        self._servicios = servicios
        self.configuracion()
    
    def configuracion(self):
        self.ui.ventanas.setCurrentWidget(self.ui.paginaIniciarSesion)
        
        self.ui.btn_mostrar_ocultar_clave.clicked.connect(self._mostrar_ocultar_clave)
        self.ui.btn_iniciar_sesion.setShortcut("Return")
        self.ui.btn_iniciar_sesion.clicked.connect(self.iniciar_sesion)
        
        self.ui.btn_manual_usuario_iniciar_sesion.clicked.connect(self.ver_manual_usuario)
    
    def iniciar_sesion(self):
        nombre_usuario = self.ui.txt_ingresar_nombre_usuario.text()
        clave_usuario = self.ui.txt_ingresar_clave_usuario.text()
        
        self.img_pantalla_carga = self._mostrar_ventana_carga
        self.img_pantalla_carga()
        
        self.hilo_iniciar_sesion = HiloIniciarSesion(self._servicios["usuario_servicio"], nombre_usuario, clave_usuario)
        self.hilo_iniciar_sesion.exito.connect(self.ir_pagina_app)
        self.hilo_iniciar_sesion.error.connect(self.error_inicio_sesion)
        self.hilo_iniciar_sesion.start()
        
        self.ui.txt_ingresar_nombre_usuario.clear()
        self.ui.txt_ingresar_clave_usuario.clear()
    
    def _mostrar_ventana_carga(self):
        from vistas.vistas_python.VentanaCarga import VentanaCarga
        
        self.ventana_carga = VentanaCarga("VentanaCarga.ui", "estilos_ventana_carga.qss")
        self.ventana_carga.abrir()
    
    def _mostrar_ocultar_clave(self):
        campo = self.ui.txt_ingresar_clave_usuario
        boton = self.ui.btn_mostrar_ocultar_clave
        
        if campo.echoMode() == QLineEdit.Password:
            campo.setEchoMode(QLineEdit.Normal)
            boton.setIcon(QIcon(":recursos/iconos/ocultar-clave.svg"))
        else:
            campo.setEchoMode(QLineEdit.Password)
            boton.setIcon(QIcon(":recursos/iconos/mostrar-clave.svg"))
    
    def ir_pagina_app(self):
        if not(hasattr(self, "ventana_app")):
            from vistas.vistas_python.VentanaApp import VentanaApp
            self.ventana_app = VentanaApp(self)
            self.cargar_estilos("estilos_ventana_app.qss", self.ui.paginaApp)
        
        if hasattr(self, "img_pantalla_carga"):
            self.ventana_carga.ui.close()
        
        self.ui.ventanas.setCurrentWidget(self.ui.paginaApp)
        self.ui.setWindowTitle("App")
        
        self.ui.de_filtro_fecha_servicio.setDate(QDate.currentDate())
        self.ui.de_fecha_servicio.setDate(QDate.currentDate())
    
    def error_inicio_sesion(self, mensaje: str):
        self.ventana_carga.ui.close()
        QMessageBox.critical(self.ui, "Error", mensaje)