from typing import Dict
from PyQt5.QtWidgets import QMessageBox, QLineEdit
from PyQt5.QtCore import QDate
from PyQt5.QtGui import QIcon

from utilidades.gui import UiBase
from configuraciones.excepciones import ValidacionError
from configuraciones.rutas import obtener_ruta_manual_usuario


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
    
    def ver_manual_usuario(self):
        try:
            RUTA_MANUAL_GENERADO = obtener_ruta_manual_usuario()
            self.mostrar_mensaje_info(f"Se generó el manual de usuario en la ruta {RUTA_MANUAL_GENERADO} en caso de querer consultar más tarde.")
        except Exception as error:
            self.mostrar_mensaje_error(f"Error al generar el manual de usuario: {error}")
    
    def iniciar_sesion(self):
        try:
            nombre_usuario = self.ui.txt_ingresar_nombre_usuario.text()
            clave_usuario = self.ui.txt_ingresar_clave_usuario.text()
            
            usuario_servicio = self._servicios["usuario_servicio"]
            usuario_pudo_auntenticarse = usuario_servicio.iniciar_sesion(nombre_usuario, clave_usuario)
            self.ir_pagina_app()
                
            self.ui.txt_ingresar_nombre_usuario.clear()
            self.ui.txt_ingresar_clave_usuario.clear()
        except ValidacionError as error:
            self.mostrar_mensaje_error("\n".join(error.errores))
    
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
        # Verifico si la ventana_app ya se creó, en caso de que
        # si exista una instancia, se reutiliza y no se vuelve a crear con la app en ejecución
        if not(hasattr(self, "ventana_app")):
            from vistas.vistas_python.VentanaApp import VentanaApp
            self.ventana_app = VentanaApp(self)
            self.cargar_estilos("estilos_ventana_app.qss", self.ui.paginaApp)
        
        self.ui.ventanas.setCurrentWidget(self.ui.paginaApp)
        self.ui.setWindowTitle("App")
        
        self.ui.de_filtro_fecha_servicio.setDate(QDate.currentDate())
        self.ui.de_fecha_servicio.setDate(QDate.currentDate())
    
    def mostrar_mensaje_error(self, mensaje: str):
        QMessageBox.critical(self.ui, "Error", mensaje)
    
    def mostrar_mensaje_info(self, mensaje: str):
        QMessageBox.information(self.ui, "Éxito", mensaje)