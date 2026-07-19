from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5.QtCore import Qt

from modelos.usuario_modelo import UsuarioModelo
from vistas.vistas_pyuic.VentanaInfoUsuarioPyuic import Ui_VentanaInfoUsuario
from configuraciones.excepciones import ValidacionError, NoEncontradoError, LogicaError


class VentanaInfoUsuario(QDialog, Ui_VentanaInfoUsuario):
    def __init__(self, usuario_data: UsuarioModelo, servicios):
        super().__init__()
        self.setupUi(self)
        
        self.setWindowFlags(
            Qt.WindowSystemMenuHint |
            Qt.WindowTitleHint |
            Qt.WindowCloseButtonHint
        )
        
        self.usuario_data = usuario_data
        self._servicios = servicios
        
        self.configuracion()
    
    def configuracion(self):
        self.botonAcualizarInfoUsuario.clicked.connect(self.actualizar_info_usuario)
        self.botonEliminarUsuario.clicked.connect(self.eliminar_usuario)
        self.botonCancelarInfoUsuario.clicked.connect(self.reject)
    
    def actualizar_data_recibida(self, data_recibida: UsuarioModelo):
        self.usuario_data = data_recibida
        self.cargar_datos()
    
    def cargar_datos(self):
        self.inputInfoNombreUsuario.setText(self.usuario_data.nombre_usuario)
        self.cbInfoTipoRol.setCurrentText(self.usuario_data.rol.tipo_rol)
        self.cbInfoTipoRol.setEnabled(False)
        
        USUARIO_ID_INFO = self.usuario_data.usuario_id
        USUARIO_ID_LOGEADO = self._servicios["usuario_servicio"].obtener_usuario_id_logeado()
        
        USUARIO_ADMIN_DEFECTO = (USUARIO_ID_LOGEADO == 1)
        USUARIO_NO_ES_SI_MISMO = (USUARIO_ID_LOGEADO != USUARIO_ID_INFO)
        
        if ((USUARIO_ADMIN_DEFECTO) and (USUARIO_NO_ES_SI_MISMO)):
            self.cbInfoTipoRol.setEnabled(True)
    
    def actualizar_info_usuario(self):
        try:
            usuario_id = self.usuario_data.usuario_id
            USUARIO_ID_LOGEADO = self._servicios["usuario_servicio"].obtener_usuario_id_logeado()
            
            nuevo_nombre_usuario = self.inputInfoNombreUsuario.text()
            nuevo_tipo_rol = self.cbInfoTipoRol.currentText()
            nueva_clave_usuario = self.inputInfoClaveUsuario.text()
            
            self._servicios["usuario_servicio"].actualizar(
                usuario_id,
                USUARIO_ID_LOGEADO,
                nuevo_tipo_rol,
                nuevo_nombre_usuario,
                nueva_clave_usuario
            )
            
            QMessageBox.information(self, "Éxito", "La información del usuario se ha actualizado correctamente.")
            self.inputInfoClaveUsuario.clear()
            self.accept()
        except ValidacionError as error:
            QMessageBox.critical(self, "Error", "\n".join(error.errores))
        except LogicaError as error:
            QMessageBox.critical(self, "Error", "\n".join(error.errores))
    
    def eliminar_usuario(self):
        mensaje_confirmacion = QMessageBox.question(
            self,
            "Confirmar eliminación",
            "¿Estás seguro de que quieres eliminar este usuario?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if (mensaje_confirmacion == QMessageBox.Yes):
            try:
                usuario_id = self.usuario_data.usuario_id
                self._servicios["usuario_servicio"].eliminar(usuario_id)
                
                QMessageBox.information(self, "Éxito", "Se eliminó el usuario correctamente.")
                self.accept()
            except NoEncontradoError as error:
                QMessageBox.critical(self, "Error", f"\n".join(error.errores))
            except ValidacionError as error:
                QMessageBox.critical(self, "Error", f"\n".join(error.errores))
            except LogicaError as error:
                QMessageBox.critical(self, "Error", "\n".join(error.errores))