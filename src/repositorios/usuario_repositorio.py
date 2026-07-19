from typing import Optional, Generator
from sqlalchemy.orm import joinedload

from configuraciones.excepciones import NoEncontradoError
from modelos.usuario_modelo import UsuarioModelo


class UsuarioRepositorio:
    def __init__(self, bd):
        self._bd = bd
    
    def registrar(self, usuario: UsuarioModelo) -> None:
        with self._bd.sesion() as sesion:
            sesion.add(usuario)
    
    def obtener_todos(self) -> Generator[UsuarioModelo, None, None]:
        with self._bd.sesion() as sesion:
            usuarios_modelo = sesion.query(UsuarioModelo).options(joinedload(UsuarioModelo.rol)).yield_per(10)
            
            for usuario in usuarios_modelo:
                yield usuario
    
    def obtener_por_id(self, usuario_id: int) -> Optional[UsuarioModelo]:
        with self._bd.sesion() as sesion:
            usuario_modelo = sesion.query(UsuarioModelo).filter_by(usuario_id = usuario_id).first()
            
            if not(usuario_modelo):
                raise NoEncontradoError(["Este usuario no existe"])
            
            return usuario_modelo
    
    def obtener_por_nombre_usuario(self, nombre_usuario: str) -> Optional[UsuarioModelo]:
        with self._bd.sesion() as sesion:
            usuario_modelo = sesion.query(UsuarioModelo).filter_by(nombre_usuario = nombre_usuario).first()
            
            if not(usuario_modelo):
                raise NoEncontradoError(["Este usuario no existe"])
            
            return usuario_modelo
    
    def actualizar(self, usuario: UsuarioModelo) -> None:
        with self._bd.sesion() as sesion:
            usuario_modelo = sesion.query(UsuarioModelo).filter_by(usuario_id = usuario.usuario_id).first()
            usuario_modelo.rol_id = usuario.rol_id
            usuario_modelo.nombre_usuario = usuario.nombre_usuario
            usuario_modelo.clave_usuario = usuario.clave_usuario
    
    def eliminar(self, usuario: UsuarioModelo) -> None:
        with self._bd.sesion() as sesion:
            usuario_modelo = sesion.query(UsuarioModelo).filter_by(usuario_id = usuario.usuario_id).first()
            self._sesion.delete(usuario_modelo)