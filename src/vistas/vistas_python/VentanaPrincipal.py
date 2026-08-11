from PyQt5.QtWidgets import QWidget, QMessageBox, QCompleter
from PyQt5.QtCore import QDate, Qt

from vistas.vistas_pyuic.VentanaPrincipalPyuic import Ui_ventanaPrincipal
from configuraciones.excepciones import ValidacionError
from configuraciones.rutas import obtener_ruta_manual_usuario


class VentanaPrincipal(QWidget, Ui_ventanaPrincipal):
    def __init__(self, servicios):
        super().__init__()
        self._servicios = servicios
        
        self.setupUi(self)
        self.configuracion()
    
    def configuracion(self):
        self.ventanas.setCurrentWidget(self.paginaIniciarSesion)
        
        self.botonAcceder.setShortcut("Return")
        self.botonAcceder.clicked.connect(self.iniciar_sesion)
        
        self.botonManualUsuarioSeccionIniciarSesion.clicked.connect(self.ver_manual_usuario)
    
    def ver_manual_usuario(self):
        try:
            RUTA_MANUAL_GENERADO = obtener_ruta_manual_usuario()
            self.mostrar_mensaje_info(f"Se generó el manual de usuario en la ruta {RUTA_MANUAL_GENERADO} en caso de querer consultar más tarde.")
        except Exception as error:
            self.mostrar_mensaje_error(f"Error al generar el manual de usuario: {error}")
    
    def iniciar_sesion(self):
        try:
            nombre_usuario = self.inputNombreUsuario.text()
            clave_usuario = self.inputClaveUsuario.text()
            
            usuario_servicio = self._servicios["usuario_servicio"]
            usuario_pudo_auntenticarse = usuario_servicio.iniciar_sesion(nombre_usuario, clave_usuario)
            self.ir_pagina_app()
                
            self.inputNombreUsuario.clear()
            self.inputClaveUsuario.clear()
        except ValidacionError as error:
            self.mostrar_mensaje_error("\n".join(error.errores))
    
    def ir_pagina_app(self):
        # Verifico si la ventana_app ya se creó, en caso de que
        # si exista una instancia, se reutiliza y no se vuelve a crear con la app en ejecución
        if not(hasattr(self, "ventana_app")):
            from vistas.vistas_python.VentanaApp import VentanaApp
            self.ventana_app = VentanaApp(self)
        
        self.ventanas.setCurrentWidget(self.paginaApp)
        self.setWindowTitle("App")
        
        self.deFiltroFecha.setDate(QDate.currentDate())
        self.deFecha.setDate(QDate.currentDate())
    
    def mostrar_mensaje_error(self, mensaje: str):
        QMessageBox.critical(self, "Error", mensaje)
    
    def mostrar_mensaje_info(self, mensaje: str):
        QMessageBox.information(self, "Éxito", mensaje)