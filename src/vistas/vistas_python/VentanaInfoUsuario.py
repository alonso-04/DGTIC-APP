from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import Qt

from modelos.usuario_modelo import UsuarioModelo
from utilidades.gui import UiBase
from configuraciones.excepciones import ValidacionError, NoEncontradoError, LogicaError


class VentanaInfoUsuario(UiBase):
    def __init__(self, usuario_data: UsuarioModelo, servicios, nombre_archivo_ui: str, nombre_archivo_estilos: str):
        super().__init__(nombre_archivo_ui, nombre_archivo_estilos)
        
        self.ui.setWindowFlags(
            Qt.WindowSystemMenuHint |
            Qt.WindowTitleHint |
            Qt.WindowCloseButtonHint
        )
        
        self.usuario_data = usuario_data
        self._servicios = servicios
        
        self.cargar_botones()
        self.configuracion()
    
    def configuracion(self):
        self.btn_actualizar.clicked.connect(self.actualizar_info_usuario)
        self.btn_eliminar.clicked.connect(self.eliminar_usuario)
        self.btn_cancelar.clicked.connect(self.ui.reject)
    
    def actualizar_data_recibida(self, data_recibida: UsuarioModelo):
        self.usuario_data = data_recibida
        self.cargar_datos()
    
    def cargar_datos(self):
        self.ui.txt_nombre_usuario.setText(self.usuario_data.nombre_usuario)
        self.ui.cb_rol_usuario.setCurrentText(self.usuario_data.rol.tipo_rol)
        self.ui.cb_rol_usuario.setEnabled(False)
        
        USUARIO_ID_INFO = self.usuario_data.usuario_id
        USUARIO_ID_LOGEADO = self._servicios["usuario_servicio"].obtener_usuario_id_logeado()
        
        USUARIO_ADMIN_DEFECTO = (USUARIO_ID_LOGEADO == 1)
        USUARIO_NO_ES_SI_MISMO = (USUARIO_ID_LOGEADO != USUARIO_ID_INFO)
        
        if ((USUARIO_ADMIN_DEFECTO) and (USUARIO_NO_ES_SI_MISMO)):
            self.ui.cb_rol_usuario.setEnabled(True)
    
    def actualizar_info_usuario(self):
        try:
            usuario_id = self.usuario_data.usuario_id
            USUARIO_ID_LOGEADO = self._servicios["usuario_servicio"].obtener_usuario_id_logeado()
            
            nuevo_nombre_usuario = self.ui.txt_nombre_usuario.text()
            nuevo_tipo_rol = self.ui.cb_rol_usuario.currentText()
            nueva_clave_usuario = self.ui.txt_clave_usuario.text()
            
            self._servicios["usuario_servicio"].actualizar(
                usuario_id,
                USUARIO_ID_LOGEADO,
                nuevo_tipo_rol,
                nuevo_nombre_usuario,
                nueva_clave_usuario
            )
            
            self.mostrar_mensaje_info("La información del usuario se ha actualizado correctamente.")
            self.ui.txt_clave_usuario.clear()
            self.ui.accept()
        except NoEncontradoError as error:
            self.mostrar_mensaje_error("\n".join(error.errores))
        except ValidacionError as error:
            self.mostrar_mensaje_error("\n".join(error.errores))
        except LogicaError as error:
            self.mostrar_mensaje_error("\n".join(error.errores))
    
    def eliminar_usuario(self):
        mensaje_confirmacion = QMessageBox.question(
            self.ui,
            "Confirmar eliminación",
            "¿Estás seguro de que quieres eliminar este usuario?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if (mensaje_confirmacion == QMessageBox.Yes):
            try:
                usuario_id = self.usuario_data.usuario_id
                self._servicios["usuario_servicio"].eliminar(usuario_id)
                
                self.mostrar_mensaje_info("Se eliminó el usuario correctamente.")
                self.ui.accept()
            except NoEncontradoError as error:
                self.mostrar_mensaje_error("\n".join(error.errores))
            except ValidacionError as error:
                self.mostrar_mensaje_error("\n".join(error.errores))
            except LogicaError as error:
                self.mostrar_mensaje_error("\n".join(error.errores))