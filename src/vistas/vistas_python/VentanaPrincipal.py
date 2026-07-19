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
    
    def cargar_completer_departamento(self):
        departamento_servicio = self._servicios["departamento_servicio"]
        departamentos = departamento_servicio.obtener_todos()
        
        nombres_departamentos = []
        
        if (departamentos):
            for departamento in departamentos:
                nombres_departamentos.append(departamento.nombre_departamento)

        if not(nombres_departamentos):
            completer_departamentos = QCompleter([])
        else:
            completer_departamentos = QCompleter(nombres_departamentos)
            
        completer_departamentos.setCaseSensitivity(Qt.CaseInsensitive)
        completer_departamentos.setFilterMode(Qt.MatchContains)
        completer_departamentos.setCompletionMode(QCompleter.PopupCompletion)
            
        self.inputDepartamento.setCompleter(completer_departamentos)
        self.inputFiltroDepartamento.setCompleter(completer_departamentos)
        self.inputBuscarDepartamento.setCompleter(completer_departamentos)
    
    def cargar_completer_tipos_servicio(self):
        tipos_servicio_tecnico_servicio = self._servicios["tipo_servicio_tecnico_servicio"]
        tipos_servicio = tipos_servicio_tecnico_servicio.obtener_todos()
        
        nombres_tipo_servicio = []
        
        if (tipos_servicio):
            for tipo_servicio in tipos_servicio:
                nombres_tipo_servicio.append(tipo_servicio.tipo_servicio_prestado)
        
        if not(nombres_tipo_servicio):
            completer_tipos_servicio = QCompleter([])
        else:
            completer_tipos_servicio = QCompleter(nombres_tipo_servicio)
            
        completer_tipos_servicio.setCaseSensitivity(Qt.CaseInsensitive)
        completer_tipos_servicio.setFilterMode(Qt.MatchContains)
        completer_tipos_servicio.setCompletionMode(QCompleter.PopupCompletion)
            
        self.inputServicioPrestado.setCompleter(completer_tipos_servicio)
        self.inputFiltroServicioPrestado.setCompleter(completer_tipos_servicio)
        self.inputFiltroTipoServicio.setCompleter(completer_tipos_servicio)
    
    def cargar_completer_categorias(self):
        categoria_tipo_servicio_tecnico_servicio = self._servicios["categoria_tipo_servicio_tecnico_servicio"]
        categorias = categoria_tipo_servicio_tecnico_servicio.obtener_todos()
        
        nombres_categorias = []
        
        if (categorias):
            for categoria in categorias:
                nombres_categorias.append(categoria.nombre_categoria)
        
        if not(nombres_categorias):
            completer_categorias = QCompleter([])
        else:
            completer_categorias = QCompleter(nombres_categorias)
            
        completer_categorias.setCaseSensitivity(Qt.CaseInsensitive)
        completer_categorias.setFilterMode(Qt.MatchContains)
        completer_categorias.setCompletionMode(QCompleter.PopupCompletion)
            
        self.inputRegistrarCategoria.setCompleter(completer_categorias)
        self.inputFiltroCategoria.setCompleter(completer_categorias)
        self.inputFiltroSeccionCategoriaTipoServicio.setCompleter(completer_categorias)