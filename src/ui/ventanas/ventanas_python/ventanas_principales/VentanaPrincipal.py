import sys
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox, QCompleter
from PyQt5.QtCore import QDate, Qt
from ui.ventanas.ventanas_pyuic.VentanaPrincipalPyuic import Ui_ventanaPrincipal
from dominio.excepciones import UsuarioValidacionError


class VentanaPrincipal(QWidget, Ui_ventanaPrincipal):
    def __init__(self, usuario_controlador, servicio_controlador):
        super().__init__()
        self.usuario_controlador = usuario_controlador
        self.servicio_controlador = servicio_controlador
        
        self.setupUi(self)
        self.configuracion()
    
    def configuracion(self):
        self.ventanas.setCurrentWidget(self.paginaIniciarSesion)
        self.botonAcceder.clicked.connect(self.iniciar_sesion)
    
    def iniciar_sesion(self):
        try:
            nombre_usuario = self.inputNombreUsuario.text()
            clave_usuario = self.inputClaveUsuario.text()
            
            if (self.usuario_controlador.iniciar_sesion_controlador(nombre_usuario, clave_usuario)):
                self.ir_pagina_app()
                
                self.inputNombreUsuario.clear()
                self.inputClaveUsuario.clear()
        except UsuarioValidacionError as error:
            self.mostrar_mensaje_error("\n".join(error.errores))
    
    def ir_pagina_app(self):
        self.ventanas.setCurrentWidget(self.paginaApp)
        self.setWindowTitle("App")
        
        self.deFiltroFecha.setDate(QDate.currentDate())
        self.deFecha.setDate(QDate.currentDate())
        
        self.botonBuscarServicios.click()
    
    def mostrar_mensaje_error(self, mensaje: str):
        QMessageBox.critical(self, "Error", mensaje)
    
    def mostrar_mensaje_info(self, mensaje: str):
        QMessageBox.information(self, "Éxito", mensaje)
    
    def esta_vacio(self, campo: str) -> bool:
        if not(campo):
            return True
        
        if (campo):
            campo_sin_espacios = campo.replace(" ", "")
            
            if (len(campo_sin_espacios) == 0):
                return True
        
        return False
    
    def cargar_completer_departamento(self):
        departamentos = self.servicio_controlador.filtrar_todos_departamentos_controlador()
        nombres_departamentos = []
        
        if (departamentos):
            for departamento in departamentos:
                nombres_departamentos.append(departamento["nombre_departamento"])

        if (nombres_departamentos):
            completer_departamentos = QCompleter(nombres_departamentos)
            completer_departamentos.setCaseSensitivity(Qt.CaseInsensitive)
            completer_departamentos.setFilterMode(Qt.MatchContains)
            completer_departamentos.setCompletionMode(QCompleter.PopupCompletion)
            
            self.inputDepartamento.setCompleter(completer_departamentos)
            self.inputFiltroDepartamento.setCompleter(completer_departamentos)
            self.inputBuscarDepartamento.setCompleter(completer_departamentos)
    
    def cargar_completer_tipos_servicio(self):
        tipos_servicio = self.servicio_controlador.filtrar_todos_tipos_servicio_controlador()
        nombres_tipo_servicio = []
        
        if (tipos_servicio):
            for tipo_servicio in tipos_servicio:
                nombres_tipo_servicio.append(tipo_servicio["tipo_servicio_prestado"])
        
        if (tipos_servicio):
            completer_tipos_servicio = QCompleter(nombres_tipo_servicio)
            completer_tipos_servicio.setCaseSensitivity(Qt.CaseInsensitive)
            completer_tipos_servicio.setFilterMode(Qt.MatchContains)
            completer_tipos_servicio.setCompletionMode(QCompleter.PopupCompletion)
            
            self.inputServicioPrestado.setCompleter(completer_tipos_servicio)
            self.inputFiltroServicioPrestado.setCompleter(completer_tipos_servicio)
            self.inputFiltroTipoServicio.setCompleter(completer_tipos_servicio)