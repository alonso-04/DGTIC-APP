import bcrypt
import json
import re
from typing import List, Optional
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from utilidades.hasher import hashear_contenido
from configuraciones.excepciones import ValidacionError, LogicaError, NoEncontradoError
from configuraciones.rutas import obtener_ruta_sesion_json
from modelos.usuario_modelo import UsuarioModelo
from repositorios.usuario_repositorio import UsuarioRepositorio
from repositorios.rol_repositorio import RolRepositorio

RUTA_SESION_JSON = obtener_ruta_sesion_json()


class UsuarioServicio:
    def __init__(self, usuario_repositorio: UsuarioRepositorio, rol_repositorio: RolRepositorio):
        self._usuario_repositorio = usuario_repositorio
        self._rol_repositorio = rol_repositorio
    
    # Métodos de validación, persistencia y obtención de datos
    def _validar_campos_usuario(self, nombre_usuario: str, clave_usuario: str) -> List[str]:
        errores = []
        
        # Validando el nombre de usuario
        if not(nombre_usuario):
            errores.append("Nombre de usuario: No puede estar vacío.")
        elif (len(nombre_usuario) > 12):
            errores.append("Nombre de usuario: No puede contener más de 12 caracteres.")
        elif (re.search(r"\s", nombre_usuario)):
            errores.append("Nombre de usuario: No debe contener espacios.")
        
        # Validando la contraseña
        if not(clave_usuario):
            errores.append("Contraseña: No puede estar vacío.")
        elif (len(clave_usuario) > 12):
            errores.append("Contraseña: No puede contener más de 12 caracteres.")
        elif (re.search(r"\s", clave_usuario)):
            errores.append("Contraseña: No debe contener espacios.")
        
        return errores
    
    def registrar(self, tipo_rol: str, nombre_usuario: str, clave_usuario: str) -> None:
        nombre_usuario_limpio = nombre_usuario.strip() if nombre_usuario else ""
        clave_usuario_limpio = clave_usuario.strip() if clave_usuario else ""
        
        errores = self._validar_campos_usuario(nombre_usuario_limpio, clave_usuario_limpio)
        
        if (errores):
            raise ValidacionError(errores)
        
        clave_usuario_hasheado = hashear_contenido(clave_usuario_limpio)
        rol_id = self._rol_repositorio.obtener_por_tipo_rol(tipo_rol).rol_id
        try:
            nuevo_usuario = UsuarioModelo(
                rol_id = rol_id,
                nombre_usuario = nombre_usuario_limpio,
                clave_usuario = clave_usuario_hasheado
            )
            self._usuario_repositorio.registrar(nuevo_usuario)
        except IntegrityError:
            raise ValidacionError(["Nombre de usuario: Este nombre de usuario ya existe."])
        except SQLAlchemyError as error:
            raise LogicaError([f"Error técnico en la base datos al registrar: {str(error)}"])
    
    def obtener_todos(self) -> List[UsuarioModelo]:
        return list(self._usuario_repositorio.obtener_todos())
    
    def obtener_por_id(self, usuario_id: int) -> Optional[UsuarioModelo]:
        return self._usuario_repositorio.obtener_por_id(usuario_id)
    
    def obtener_por_nombre_usuario(self, nombre_usuario: str) -> Optional[UsuarioModelo]:
        return self._usuario_repositorio.obtener_por_nombre_usuario(nombre_usuario)
    
    def actualizar(self, usuario_id: int, usuario_id_logeado: int, nuevo_tipo_rol: str, nuevo_nombre_usuario: str, nuevo_clave_usuario: str) -> None:
        errores = []
        
        nuevo_nombre_usuario_limpio = nuevo_nombre_usuario.strip() if nuevo_nombre_usuario else ""
        nuevo_clave_usuario_limpio = nuevo_clave_usuario.strip() if nuevo_clave_usuario else ""
        
        usuario_a_actualizar = self._usuario_repositorio.obtener_por_id(usuario_id)
        rol_id_usuario_a_actualizar = usuario_a_actualizar.rol_id
        nuevo_rol_id_usuario = self._rol_repositorio.obtener_por_tipo_rol(nuevo_tipo_rol).rol_id
        
        # Validando el nombre de usuario
        if not(nuevo_nombre_usuario_limpio):
            errores.append("Nombre de usuario: No puede estar vacío.")
        elif (len(nuevo_nombre_usuario_limpio) > 12):
            errores.append("Nombre de usuario: No puede contener más de 12 caracteres.")
        elif (re.search(r"\s", nuevo_nombre_usuario_limpio)):
            errores.append("Nombre de usuario: No debe contener espacios.")
        
        # Validando la contraseña
        if (nuevo_clave_usuario_limpio):
            if (len(nuevo_clave_usuario_limpio) > 12):
                errores.append("Contraseña: No puede contener más de 12 caracteres.")
            elif (re.search(r"\s", nuevo_clave_usuario_limpio)):
                errores.append("Contraseña: No debe contener espacios.")
        
        USUARIO_NO_ES_SI_MISMO = (usuario_id_logeado != usuario_id)
        USUARIO_ADMIN_DEFECTO = 1
        USUARIO_ACTUALIZAR_ES_ADMIN = (rol_id_usuario_a_actualizar == 1)
        
        # Validando que el usuario que no sea Administrador por defecto no pueda modificar la info de otros Administradores
        if (((usuario_id_logeado != USUARIO_ADMIN_DEFECTO) and (USUARIO_ACTUALIZAR_ES_ADMIN)) and (USUARIO_NO_ES_SI_MISMO)):
            errores.append("No puedes modificar la info de un Administrador.")
        
        if (errores):
            raise ValidacionError(errores)
        
        # Validando si el usuario escribió otra contraseña que se hashee
        # sino, que no la vuelva a hashear y mantiene la contraseña que ya tiene
        if (nuevo_clave_usuario_limpio):
            nuevo_clave_hasheada_usuario = hashear_contenido(nuevo_clave_usuario_limpio)
        else:
            nuevo_clave_hasheada_usuario = usuario_a_actualizar.clave_usuario
        
        try:
            usuario_actualizado = UsuarioModelo(
                usuario_id = usuario_id,
                rol_id = nuevo_rol_id_usuario,
                nombre_usuario = nuevo_nombre_usuario_limpio,
                clave_usuario = nuevo_clave_hasheada_usuario
            )
            self._usuario_repositorio.actualizar(usuario_actualizado)
        except NoEncontradoError as error:
            raise error
        except IntegrityError:
            raise ValidacionError(["Nombre de usuario: Este nombre de usuario ya existe."])
        except SQLAlchemyError as error:
            raise LogicaError([f"Error técnico en la base datos al actualizar: {str(error)}"])
    
    def eliminar(self, usuario_id: int) -> None:
        errores = []
        
        usuario_a_eliminar = self._usuario_repositorio.obtener_por_id(usuario_id)
        usuario_id_logeado = self.obtener_usuario_id_logeado()
        rol_id_usuario_a_eliminar = usuario_a_eliminar.rol_id
            
        USUARIO_ES_ADMIN_DEFECTO = 1
        ROL_ID_ADMIN = 1
        USUARIO_NO_ES_SI_MISMO = (usuario_id_logeado != usuario_id)
        USUARIO_ES_ADMIN = (rol_id_usuario_a_eliminar == ROL_ID_ADMIN)
            
        if (usuario_id == USUARIO_ES_ADMIN_DEFECTO):
            errores.append("Este usuario administrador no puede eliminarse porque es el predeterminado del sistema.")
            
        if (usuario_id_logeado == usuario_id):
            errores.append("No puedes eliminarte a ti mismo.")
            
        if ((USUARIO_NO_ES_SI_MISMO) and (USUARIO_ES_ADMIN) and not(USUARIO_ES_ADMIN_DEFECTO)):
            errores.append("No puedes eliminar a un usuario Administrador.")
        
        if (errores):
            raise ValidacionError(errores)
        
        try:
            self._usuario_repositorio.eliminar(usuario_a_eliminar)
        except NoEncontradoError as error:
            raise error
        except SQLAlchemyError as error:
            raise LogicaError([f"Error técnico en la base datos al eliminar: {str(error)}"])
    
    # Métodos para la sesión del usuario
    def obtener_usuario_id_logeado(self) -> int:
        with open(RUTA_SESION_JSON, "r") as sesion_usuario_json:
            data = json.load(sesion_usuario_json)
            
            if ("usuario_id" in data):
                USUARIO_ID_LOGEADO = data["usuario_id"]
            
            return USUARIO_ID_LOGEADO
    
    def usuario_es_admin(self) -> bool:
        try:
            usuario_id_logeado = self.obtener_usuario_id_logeado()
            usuario = self._usuario_repositorio.obtener_por_id(usuario_id_logeado)
            es_admin = True if (usuario.rol_id == 1) else False
            return es_admin
        except NoEncontradoError:
            return False
    
    def autenticar_usuario(self, nombre_usuario: str, clave_usuario: str) -> Optional[int]:
        nombre_usuario_limpio = nombre_usuario.strip() if nombre_usuario else ""
        clave_usuario_limpio = clave_usuario.strip() if clave_usuario else ""
        
        try:
            usuario_a_auntenticar = self._usuario_repositorio.obtener_por_nombre_usuario(nombre_usuario_limpio)
            clave_usuario_texto_plano = clave_usuario_limpio.encode("utf-8")
            clave_usuario_hasheado = usuario_a_auntenticar.clave_usuario.encode("utf-8")

            if (bcrypt.checkpw(clave_usuario_texto_plano, clave_usuario_hasheado)):
                return {"usuario_id": usuario_a_auntenticar.usuario_id}
            
            return None
        except NoEncontradoError:
            return None
    
    def iniciar_sesion(self, nombre_usuario: str, clave_usuario: str) -> None:
        usuario_id = self.autenticar_usuario(nombre_usuario, clave_usuario)
            
        if not(usuario_id):
            raise ValidacionError(["El usuario y/o contraseña son incorrectos."])
        
        with open(RUTA_SESION_JSON, "w") as sesion_usuario_json:
            json.dump(usuario_id, sesion_usuario_json, indent = 4)
    
    def cerrar_sesion(self) -> None:
        try:
            with open(RUTA_SESION_JSON, "r") as sesion_usuario_json:
                data = json.load(sesion_usuario_json)
                
                if ("usuario_id" in data):
                    data["usuario_id"] = None
                
                with open(RUTA_SESION_JSON, "w") as sesion_usuario_json:
                    json.dump(data, sesion_usuario_json, indent = 4)
        except FileNotFoundError as error:
            with open(RUTA_SESION_JSON, "w") as sesion_usuario_json:
                json.dump({"usuario_id": None}, sesion_usuario_json, indent = 4)
        except json.JSONDecodeError as error:
            raise error