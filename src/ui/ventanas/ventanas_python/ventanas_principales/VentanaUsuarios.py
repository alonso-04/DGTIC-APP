import json
from PyQt5.QtCore import QDate
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QHeaderView, QDialog
from typing import Dict
from ui.ventanas.ventanas_python.ventanas_principales.VentanaPrincipal import VentanaPrincipal
from ui.ventanas.ventanas_python.ventanas_info.VentanaInfoUsuario import VentanaInfoUsuario
from dominio.excepciones import UsuarioValidacionError
from configuraciones.rutas import obtener_ruta_sesion_json

RUTA_SESION_JSON = obtener_ruta_sesion_json()


class VentanaUsuarios:
    def __init__(self, ventana_principal: VentanaPrincipal):
        super().__init__()
        self.ventana_principal = ventana_principal
        
        # CONTROLADORES
        self.usuario_controlador = self.ventana_principal.usuario_controlador
        
        # FUNCIONES Y ELEMENTOS DE UTILIDAD
        self.mostrar_mensaje_error = self.ventana_principal.mostrar_mensaje_error
        self.mostrar_mensaje_info = self.ventana_principal.mostrar_mensaje_info
        self.esta_vacio = self.ventana_principal.esta_vacio
        self.botonRefrescarUsuarios = self.ventana_principal.botonRefrescarUsuarios
        
        # SECCIÓN DE REGISTRAR
        self.inputRegistrarNombreUsuario = self.ventana_principal.inputRegistrarNombreUsuario
        self.cbRolesRegistrarUsuario = self.ventana_principal.cbRolesRegistrarUsuario
        self.inputRegistrarClaveUsuario = self.ventana_principal.inputRegistrarClaveUsuario
        self.botonRegistrarUsuario = self.ventana_principal.botonRegistrarUsuario
        
        
        # SECCIÓN DE LA TABLA DE USUARIOS
        self.tvUsuarios = self.ventana_principal.tvUsuarios
        self.usuario_data = []
        
        
        # BOTONES INFERIORES
        self.botonRegresarSeccionUsuarios = self.ventana_principal.botonRegresarSeccionUsuarios
        
        self.configurar()
    
    def configurar(self):
        self.botonRefrescarUsuarios.clicked.connect(self.refrescar_pagina_usuarios)
        self.botonRegresarSeccionUsuarios.clicked.connect(self.ir_pagina_app)
        self.tvUsuarios.clicked.connect(self.seleccionar_usuario)
        self.botonRegistrarUsuario.clicked.connect(self.registrar_nuevo_usuario)
        
        self.filtrar_todos_usuarios()
    
    def refrescar_pagina_usuarios(self):
        self.filtrar_todos_usuarios()
    
    def ir_pagina_app(self):
        self.ventana_principal.ventanas.setCurrentWidget(self.ventana_principal.paginaApp)
        self.ventana_principal.setWindowTitle("App")
        self.ventana_principal.deFiltroFecha.setDate(QDate.currentDate())
        self.ventana_principal.deFecha.setDate(QDate.currentDate())
    
    def registrar_nuevo_usuario(self):
        try:
            nombre_usuario = self.inputRegistrarNombreUsuario.text()
            tipo_rol = self.cbRolesRegistrarUsuario.currentText()
            clave_usuario = self.inputRegistrarClaveUsuario.text()
            
            if (self.esta_vacio(nombre_usuario)):
                nombre_usuario = None
            
            if (self.esta_vacio(clave_usuario)):
                clave_usuario = ""
            
            self.usuario_controlador.registrar_usuario_controlador(
                nombre_usuario,
                tipo_rol,
                clave_usuario
            )
            
            self.inputRegistrarNombreUsuario.clear()
            self.inputRegistrarClaveUsuario.clear()
            
            self.filtrar_todos_usuarios()
        except UsuarioValidacionError as error:
            self.mostrar_mensaje_error("\n".join(error.errores))
    
    def filtrar_todos_usuarios(self):
        try:
            usuarios = self.usuario_controlador.filtrar_todos_usuarios_controlador()
            self.usuario_data = usuarios
            
            if not(usuarios):
                self.usuario_data = []
                return
            
            modelo_datos = QStandardItemModel(len(usuarios), 2)
            modelo_datos.setHorizontalHeaderLabels([
                "Nombre de usuario",
                "Tipo de rol"
            ])
            
            for fila, usuario in enumerate(usuarios):
                items = [
                    QStandardItem(str(usuario["nombre_usuario"])),
                    QStandardItem(str(usuario["tipo_rol"]))
                ]
                
                for columna, item in enumerate(items):
                    modelo_datos.setItem(fila, columna, item)
            
            self.tvUsuarios.setModel(modelo_datos)
        except UsuarioValidacionError as error:
            self.usuario_data = []
        finally:
            header = self.tvUsuarios.horizontalHeader()
            header.setSectionResizeMode(QHeaderView.Stretch)

    def seleccionar_usuario(self, indice):
        fila_seleccionada = indice.row()
        
        if ((fila_seleccionada >= 0) and (fila_seleccionada < len(self.usuario_data))):
            usuario_seleccionado = self.usuario_data[fila_seleccionada]
            self.mostrar_ventana_info_usuario(usuario_seleccionado)
    
    def mostrar_ventana_info_usuario(self, usuario_data: Dict):
        try:
            ventana_info_usuario = VentanaInfoUsuario(
                usuario_data = usuario_data,
                usuario_controlador = self.usuario_controlador
            )
            
            USUARIO_ID_LOGEADO = self.obtener_usuario_id_logeado()
            USUARIO_ID_SELECICONADO = usuario_data["usuario_id"]
            ROL_USUARIO_SELECCIONADO = usuario_data["rol_id"]
            
            if (((USUARIO_ID_LOGEADO != USUARIO_ID_SELECICONADO) and (ROL_USUARIO_SELECCIONADO == 1)) and (USUARIO_ID_LOGEADO != 1)):
                self.mostrar_mensaje_error("No puedes modificar o eliminar la info de otro usuario Administrador.")
            else:
                resultado = ventana_info_usuario.exec_()
                
                if (resultado == QDialog.Accepted):
                    self.filtrar_todos_usuarios()
        except Exception as error:
            self.mostrar_mensaje_error(f"Error al mostrar la ventana de info de usuario: {error}")
    
    def obtener_usuario_id_logeado(self) -> int:
        with open(RUTA_SESION_JSON, "r") as sesion_usuario_json:
            data = json.load(sesion_usuario_json)
            
            if ("usuario_id" in data):
                USUARIO_ID_LOGEADO = data["usuario_id"]
            
            return USUARIO_ID_LOGEADO