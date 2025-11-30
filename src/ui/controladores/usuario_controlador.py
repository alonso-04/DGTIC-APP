import json
from dominio.entidades.usuario import Usuario
from dominio.excepciones import UsuarioValidacionError
from dominio.excepciones import RolValidacionError
from utilidades.hasher import hashear_contenido
from configuraciones.rutas import obtener_ruta_sesion_json

RUTA_SESION_JSON = obtener_ruta_sesion_json() 


class UsuarioControlador:
    def __init__(
        self,
        registrar_usuario,
        listar_usuarios,
        actualizar_info_usuario,
        eliminar_usuario,
        sesion_usuario,
        listar_roles
    ):
        self.registrar_usuario = registrar_usuario
        self.listar_usuarios = listar_usuarios
        self.actualizar_info_usuario = actualizar_info_usuario
        self.eliminar_usuario = eliminar_usuario
        self.sesion_usuario = sesion_usuario
        self.listar_roles = listar_roles
    
    
    # MÉTODOS PARA LOS USUARIOS
    
    def iniciar_sesion_controlador(self, nombre_usuario: str, clave_usuario: str):
        usuario_id = self.sesion_usuario.iniciar_sesion(nombre_usuario, clave_usuario)
        
        if (usuario_id):
            self.sesion_usuario.cargar_sesion(nombre_usuario, clave_usuario)
            return True
        return False
    
    def cerrar_sesion_controlador(self):
        self.sesion_usuario.cerrar_sesion()
    
    def usuario_es_admin(self):
        with open(RUTA_SESION_JSON, "r") as sesion_usuario_json:
            data = json.load(sesion_usuario_json)
            
            if ("usuario_id" in data):
                USUARIO_ID_LOGEADO = data["usuario_id"]
                ROL_ID_ADMIN = 1
                
                rol_id_usuario = self.listar_usuarios.obtener_por_id(USUARIO_ID_LOGEADO).rol_id
                
                if (rol_id_usuario == ROL_ID_ADMIN):
                    return True
                return False
    
    def registrar_usuario_controlador(self, nombre_usuario: str, tipo_rol: str, clave_usuario: str):
        try:
            if (tipo_rol):
                rol_id = self.listar_roles.obtener_por_tipo_rol(tipo_rol).rol_id
            
            nuevo_usuario = Usuario(
                nombre_usuario = nombre_usuario,
                clave_usuario = clave_usuario,
                rol_id = rol_id
            )
            
            self.registrar_usuario.ejecutar(nuevo_usuario)
        except UsuarioValidacionError as error:
            raise error
        except RolValidacionError as error:
            raise error
        except Exception as error:
            raise error
    
    def filtrar_todos_usuarios_controlador(self):
        try:
            usuarios = self.listar_usuarios.obtener_todos()
            
            lista_dict_usuarios = []
            
            for usuario in usuarios:
                tipo_rol = self.listar_roles.obtener_por_id(usuario.rol_id).tipo_rol
                
                elemento = {
                    "usuario_id": usuario.usuario_id,
                    "rol_id": usuario.rol_id,
                    "nombre_usuario": usuario.nombre_usuario,
                    "tipo_rol": tipo_rol,
                    "clave_usuario": usuario.clave_usuario
                }
                
                lista_dict_usuarios.append(elemento)
            
            return lista_dict_usuarios
        except UsuarioValidacionError as error:
            raise error
    
    def seleccionar_usuario_controlador(self, usuario_id: int):
        try:
            nombre_usuario = self.listar_usuarios.obtener_por_id(usuario_id).nombre_usuario
            tipo_rol = self.listar_usuarios.obtener_por_id(usuario_id).tipo_rol
            clave_usuario = self.listar_usuarios.obtener_por_id(usuario_id).clave_usuario
            
            dict_usuario = {
                "nombre_usuario": nombre_usuario,
                "tipo_rol": tipo_rol,
                "clave_usuario": clave_usuario
            }
            
            return dict_usuario
        except UsuarioValidacionError as error:
            raise error
    
    def actualizar_info_usuario_controlador(self, usuario_id: int, usuario_id_logeado: int, nuevo_nombre_usuario: str, nuevo_tipo_rol: str, nueva_clave_usuario: str):
        try:
            if (nuevo_tipo_rol):
                nuevo_rol_id = self.listar_roles.obtener_por_tipo_rol(nuevo_tipo_rol).rol_id
            
            clave_anterior_usuario = self.listar_usuarios.obtener_por_id(usuario_id).clave_usuario
            clave_nueva_usuario = nueva_clave_usuario
            
            if not(clave_anterior_usuario == clave_nueva_usuario):
                nueva_clave_usuario_hasheada = hashear_contenido(nueva_clave_usuario)
            else:
                nueva_clave_usuario_hasheada = clave_anterior_usuario
            
            nuevos_datos = {
                "rol_id": nuevo_rol_id,
                "nombre_usuario": nuevo_nombre_usuario,
                "clave_usuario": nueva_clave_usuario_hasheada
            }
            
            self.actualizar_info_usuario.ejecutar(usuario_id, usuario_id_logeado, nuevos_datos)
        except UsuarioValidacionError as error:
            raise error
    
    def eliminar_usuario_controlador(self, usuario_id: int):
        try:
            with open(RUTA_SESION_JSON, "r") as sesion_usuario_json:
                data = json.load(sesion_usuario_json)

                if ("usuario_id" in data):
                    USUARIO_ID_LOGEADO = data["usuario_id"]
                    
                    self.eliminar_usuario.ejecutar(usuario_id, USUARIO_ID_LOGEADO)
        except UsuarioValidacionError as error:
            raise error