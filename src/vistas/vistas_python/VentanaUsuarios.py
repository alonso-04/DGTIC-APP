from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import QHeaderView, QDialog

from modelos.usuario_modelo import UsuarioModelo
from utilidades.gui import UiBase, registrar_campos, limpiar_campos, obtener_modelo_datos_y_data
from vistas.vistas_python.VentanaPrincipal import VentanaPrincipal
from configuraciones.excepciones import ValidacionError, NoEncontradoError, LogicaError


class VentanaUsuarios(UiBase):
    def __init__(self, ventana_principal: VentanaPrincipal):
        super().__init__()
        self.ventana_principal = ventana_principal
        self.ui = ventana_principal.ui
        self._servicios = self.ventana_principal._servicios
        
        
        # DATA DE LOS USUARIOS
        self.usuario_data = []
        
        self.configurar()
    
    def configurar(self):
        self.ui.btn_refrescar_pagina_ventana_usuarios.clicked.connect(self.refrescar_pagina_usuarios)
        self.ui.btn_manual_usuario_ventana_usuarios.clicked.connect(self.ver_manual_usuario)
        self.ui.btn_regresar_ventana_usuarios.clicked.connect(self.ir_pagina_app)
        self.ui.btn_registrar_usuario.clicked.connect(self.registrar_nuevo_usuario)
        
        self.ui.tabla_usuarios.clicked.connect(self.seleccionar_usuario)
        self.configurar_tabla(self.ui.tabla_usuarios)
        
        self.filtrar_todos_usuarios()
    
    def refrescar_pagina_usuarios(self):
        self.filtrar_todos_usuarios()
    
    def ir_pagina_app(self):
        self.ui.ventanas.setCurrentWidget(self.ui.paginaApp)
        self.ui.setWindowTitle("App")
        self.ui.de_filtro_fecha_servicio.setDate(QDate.currentDate())
        self.ui.de_fecha_servicio.setDate(QDate.currentDate())
    
    def registrar_nuevo_usuario(self):
        try:
            campos_a_registrar = [
                (self.ui.txt_nombre_usuario, "nombre_usuario"),
                (self.ui.txt_clave_usuario, "clave_usuario"),
                (self.ui.cb_rol_usuario, "tipo_rol")
            ]
            
            registrar_campos(self._servicios["usuario_servicio"], campos_a_registrar, "usuario")
            limpiar_campos([
                self.ui.txt_nombre_usuario,
                self.ui.txt_clave_usuario
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
        nombres_columnas = ["nombre_usuario", "rol.tipo_rol"]
        
        modelo_datos, registros = obtener_modelo_datos_y_data(
            self._servicios["usuario_servicio"].obtener_todos,
            nombres_labels,
            nombres_columnas
        )
        
        self.usuario_data = registros
        self.ui.tabla_usuarios.setModel(modelo_datos)
            
        header = self.ui.tabla_usuarios.horizontalHeader()
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
                usuario_data,
                self._servicios,
                "VentanaInfoUsuario.ui",
                "estilos_ventanas_info.qss"
            )
            
        USUARIO_ID_LOGEADO = self._servicios["usuario_servicio"].obtener_usuario_id_logeado()
        USUARIO_ID_SELECICONADO = usuario_data.usuario_id
        ROL_USUARIO_SELECCIONADO = usuario_data.rol_id
            
        if (((USUARIO_ID_LOGEADO != USUARIO_ID_SELECICONADO) and (ROL_USUARIO_SELECCIONADO == 1)) and (USUARIO_ID_LOGEADO != 1)):
            self.mostrar_mensaje_error("No puedes modificar o eliminar la info de otro usuario Administrador.")
        else:
            self.ventana_info_usuario.actualizar_data_recibida(usuario_data)
            resultado = self.ventana_info_usuario.ui.exec_()
                
            if (resultado == QDialog.Accepted):
                self.filtrar_todos_usuarios()