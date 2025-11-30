import json
from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5.QtCore import Qt
from typing import Dict
from ui.ventanas.ventanas_pyuic.VentanaInfoUsuarioPyuic import Ui_VentanaInfoUsuario
from dominio.excepciones import UsuarioValidacionError
from configuraciones.rutas import obtener_ruta_sesion_json

RUTA_SESION_JSON = obtener_ruta_sesion_json()


class VentanaInfoUsuario(QDialog, Ui_VentanaInfoUsuario):
    def __init__(self, usuario_data: Dict, usuario_controlador):
        super().__init__()
        self.setupUi(self)
        
        self.setWindowFlags(
            Qt.WindowSystemMenuHint |
            Qt.WindowTitleHint |
            Qt.WindowCloseButtonHint
        )
        
        self.usuario_data = usuario_data
        self.usuario_controlador = usuario_controlador
        
        self.configuracion()
        self.cargar_datos()
    
    def configuracion(self):
        self.botonAcualizarInfoUsuario.clicked.connect(self.actualizar_info_usuario)
        self.botonEliminarUsuario.clicked.connect(self.eliminar_usuario)
        self.botonCancelarInfoUsuario.clicked.connect(self.reject)
    
    def obtener_usuario_id_logeado(self) -> int:
        with open(RUTA_SESION_JSON, "r") as sesion_usuario_json:
            data = json.load(sesion_usuario_json)
            
            if ("usuario_id" in data):
                USUARIO_ID_LOGEADO = data["usuario_id"]
            
            return USUARIO_ID_LOGEADO
    
    def cargar_datos(self):
        self.inputInfoNombreUsuario.setText(self.usuario_data["nombre_usuario"])
        self.cbInfoTipoRol.setCurrentText(self.usuario_data["tipo_rol"])
        self.cbInfoTipoRol.setEnabled(False)
        
        USUARIO_ID_INFO = self.usuario_data["usuario_id"]
        USUARIO_ID_LOGEADO = self.obtener_usuario_id_logeado()
        
        USUARIO_ADMIN_DEFECTO = (USUARIO_ID_LOGEADO == 1)
        USUARIO_NO_ES_SI_MISMO = (USUARIO_ID_LOGEADO != USUARIO_ID_INFO)
        
        if ((USUARIO_ADMIN_DEFECTO) and (USUARIO_NO_ES_SI_MISMO)):
            self.cbInfoTipoRol.setEnabled(True)
    
    def actualizar_info_usuario(self):
        try:
            usuario_id = self.usuario_data["usuario_id"]
            USUARIO_ID_LOGEADO = self.obtener_usuario_id_logeado()
            
            nuevo_nombre_usuario = self.inputInfoNombreUsuario.text()
            nuevo_tipo_rol = self.cbInfoTipoRol.currentText()
            
            nueva_clave_usuario_texto_plano = self.inputInfoClaveUsuario.text()
            
            if (self.esta_vacio(nueva_clave_usuario_texto_plano)):
                nueva_clave_usuario_texto_plano = self.usuario_data["clave_usuario"]
            
            self.usuario_controlador.actualizar_info_usuario_controlador(
                usuario_id,
                USUARIO_ID_LOGEADO,
                nuevo_nombre_usuario,
                nuevo_tipo_rol,
                nueva_clave_usuario_texto_plano
            )
            
            QMessageBox.information(self, "Éxito", "La información del usuario se ha actualizado correctamente.")
            self.accept()
        except UsuarioValidacionError as error:
            QMessageBox.critical(self, "Error", "\n".join(error.errores))
        except Exception as error:
            QMessageBox.critical(self, "Error", f"{error}")
    
    def eliminar_usuario(self):
        mensaje_confirmacion = QMessageBox.question(
            self,
            "Confirmar eliminación",
            "¿Estás seguro de que quieres eliminar este usuario?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if (mensaje_confirmacion == QMessageBox.Yes):
            try:
                usuario_id = self.usuario_data["usuario_id"]
                self.usuario_controlador.eliminar_usuario_controlador(usuario_id)
                
                QMessageBox.information(self, "Éxito", "Se eliminó el usuario correctamente.")
                self.accept()
            except UsuarioValidacionError as error:
                QMessageBox.critical(self, "Error", f"\n".join(error.errores))
            except Exception as error:
                QMessageBox.critical(self, "Error", f"{error}")
    
    def esta_vacio(self, campo: str) -> bool:
        if not(campo):
            return True
        
        if (campo):
            campo_sin_espacios = campo.replace(" ", "")
            
            if (len(campo_sin_espacios) == 0):
                return True
        
        return False