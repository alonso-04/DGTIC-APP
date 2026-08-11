from PyQt5.QtCore import QDate
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QHeaderView, QDialog

from modelos.usuario_modelo import UsuarioModelo
from vistas.vistas_python.VentanaPrincipal import VentanaPrincipal
from vistas.utilidades_gui.registrar import registrar_campos
from vistas.utilidades_gui.limpiar_campos import limpiar_campos
from vistas.utilidades_gui.filtrar import obtener_modelo_datos_y_data
from configuraciones.excepciones import ValidacionError, NoEncontradoError, LogicaError


class VentanaUsuarios:
    def __init__(self, ventana_principal: VentanaPrincipal):
        super().__init__()
        self.ventana_principal = ventana_principal
        
        # SERVICIOS
        self._servicios = self.ventana_principal._servicios
        
        
        # FUNCIONES Y ELEMENTOS DE UTILIDAD
        self.mostrar_mensaje_error = self.ventana_principal.mostrar_mensaje_error
        self.mostrar_mensaje_info = self.ventana_principal.mostrar_mensaje_info
        self.botonRefrescarUsuarios = self.ventana_principal.botonRefrescarUsuarios
        self.cargar_manual_usuario = self.ventana_principal.ver_manual_usuario
        self.botonManualUsuarioSeccionUsuarios = self.ventana_principal.botonManualUsuarioSeccionUsuarios
        
        
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
        self.botonManualUsuarioSeccionUsuarios.clicked.connect(self.ver_manual_usuario)
        self.botonRegresarSeccionUsuarios.clicked.connect(self.ir_pagina_app)
        self.tvUsuarios.clicked.connect(self.seleccionar_usuario)
        self.botonRegistrarUsuario.clicked.connect(self.registrar_nuevo_usuario)
        
        self.filtrar_todos_usuarios()
    
    def refrescar_pagina_usuarios(self):
        self.filtrar_todos_usuarios()
    
    def ver_manual_usuario(self):
        self.cargar_manual_usuario()
    
    def ir_pagina_app(self):
        self.ventana_principal.ventanas.setCurrentWidget(self.ventana_principal.paginaApp)
        self.ventana_principal.setWindowTitle("App")
        self.ventana_principal.deFiltroFecha.setDate(QDate.currentDate())
        self.ventana_principal.deFecha.setDate(QDate.currentDate())
    
    def registrar_nuevo_usuario(self):
        try:
            campos_a_registrar = [
                (self.inputRegistrarNombreUsuario, "nombre_usuario"),
                (self.inputRegistrarClaveUsuario, "clave_usuario"),
                (self.cbRolesRegistrarUsuario, "tipo_rol")
            ]
            
            registrar_campos(self._servicios["usuario_servicio"], campos_a_registrar)
            limpiar_campos([
                self.inputRegistrarNombreUsuario,
                self.inputRegistrarClaveUsuario
            ])
            
            self.filtrar_todos_usuarios()
        except NoEncontradoError as error:
            self.mostrar_mensaje_error("\n".join(error.errores))
        except ValidacionError as error:
            self.mostrar_mensaje_error("\n".join(error.errores))
        except LogicaError as error:
            self.mostrar_mensaje_error("\n".join(error.errores))
    
    def filtrar_todos_usuarios(self):
        nombres_labels = ["Nombre de usuario", "Tipo de rol"]
        nombres_columnas = ["nombre_usuario", "tipo_rol"]
        
        modelo_datos, registros = obtener_modelo_datos_y_data(
            self._servicios["usuario_servicio"].obtener_todos,
            nombres_labels,
            nombres_columnas
        )
        
        self.usuario_data = registros
        self.tvUsuarios.setModel(modelo_datos)
            
        header = self.tvUsuarios.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)

    def seleccionar_usuario(self, indice):
        fila_seleccionada = indice.row()
        
        if ((fila_seleccionada >= 0) and (fila_seleccionada < len(self.usuario_data))):
            usuario_seleccionado = self.usuario_data[fila_seleccionada]
            self.mostrar_ventana_info_usuario(usuario_seleccionado)
    
    def mostrar_ventana_info_usuario(self, usuario_data: UsuarioModelo):
        if not(hasattr(self, "ventana_info_usuario")):
            from vistas.vistas_python.VentanaInfoUsuario import VentanaInfoUsuario
            self.ventana_info_usuario = VentanaInfoUsuario(
                usuario_data = usuario_data,
                servicios = self._servicios
            )
            
        USUARIO_ID_LOGEADO = self._servicios["usuario_servicio"].obtener_usuario_id_logeado()
        USUARIO_ID_SELECICONADO = usuario_data.usuario_id
        ROL_USUARIO_SELECCIONADO = usuario_data.rol_id
            
        if (((USUARIO_ID_LOGEADO != USUARIO_ID_SELECICONADO) and (ROL_USUARIO_SELECCIONADO == 1)) and (USUARIO_ID_LOGEADO != 1)):
            self.mostrar_mensaje_error("No puedes modificar o eliminar la info de otro usuario Administrador.")
        else:
            self.ventana_info_usuario.actualizar_data_recibida(usuario_data)
            resultado = self.ventana_info_usuario.exec_()
                
            if (resultado == QDialog.Accepted):
                self.filtrar_todos_usuarios()