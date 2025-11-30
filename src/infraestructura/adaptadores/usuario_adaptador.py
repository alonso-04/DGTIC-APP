import bcrypt
from sqlalchemy.orm import Session
from dominio.entidades.usuario import Usuario
from dominio.puertos.usuario_puerto import UsuarioPuerto
from infraestructura.modelos.usuario_modelo import UsuarioModelo
from typing import Optional, Generator, Dict


class UsuarioAdaptador(UsuarioPuerto):
    def __init__(self, sesion: Session):
        self._sesion = sesion
    
    def registrar(self, usuario: Usuario) -> None:
        usuario_modelo = UsuarioModelo(
            rol_id = usuario.rol_id,
            nombre_usuario = usuario.nombre_usuario,
            clave_usuario = usuario.clave_usuario
        )
        
        self._sesion.add(usuario_modelo)
    
    def obtener_todos(self) -> Generator[Usuario, None, None]:
        usuarios_modelo = self._sesion.query(UsuarioModelo).yield_per(10)
        
        for usuario in usuarios_modelo:
            yield Usuario(
                usuario_id = usuario.usuario_id,
                rol_id = usuario.rol_id,
                nombre_usuario = usuario.nombre_usuario,
                clave_usuario = usuario.clave_usuario
            )
    
    def obtener_por_id(self, usuario_id: int) -> Optional[Usuario]:
        usuario_modelo = self._sesion.query(UsuarioModelo).filter_by(usuario_id = usuario_id).first()
        
        if (usuario_modelo):
            return Usuario(
                usuario_id = usuario_modelo.usuario_id,
                rol_id = usuario_modelo.rol_id,
                nombre_usuario = usuario_modelo.nombre_usuario,
                clave_usuario = usuario_modelo.clave_usuario
            )
        return None
    
    def obtener_por_nombre_usuario(self, nombre_usuario: str) -> Optional[Usuario]:
        usuario_modelo = self._sesion.query(UsuarioModelo).filter_by(nombre_usuario = nombre_usuario).first()
        
        if (usuario_modelo):
            return Usuario(
                usuario_id = usuario_modelo.usuario_id,
                rol_id = usuario_modelo.rol_id,
                nombre_usuario = usuario_modelo.nombre_usuario,
                clave_usuario = usuario_modelo.clave_usuario
            )
        return None
    
    def autenticar_usuario(self, nombre_usuario: str, clave_usuario: str) -> Optional[Dict]:
        usuario_modelo = self._sesion.query(UsuarioModelo).filter(
            UsuarioModelo.nombre_usuario == nombre_usuario
        ).first()
        
        if (not(usuario_modelo)):
            return None
        
        clave_usuario_texto_plano = clave_usuario.encode("utf-8")
        clave_usuario_hasheado = usuario_modelo.clave_usuario.encode("utf-8")
        
        if (bcrypt.checkpw(clave_usuario_texto_plano, clave_usuario_hasheado)):
            return {
                "usuario_id": usuario_modelo.usuario_id
            }
        return None
    
    def actualizar(self, usuario: Usuario) -> None:
        usuario_modelo = self._sesion.query(UsuarioModelo).filter_by(usuario_id = usuario.usuario_id).first()
        
        if not(usuario_modelo):
            raise ValueError("Este usuario no existe.")
        
        usuario_modelo.rol_id = usuario.rol_id
        usuario_modelo.nombre_usuario = usuario.nombre_usuario
        usuario_modelo.clave_usuario = usuario.clave_usuario
    
    def eliminar(self, usuario: Usuario) -> None:
        usuario_modelo = self._sesion.query(UsuarioModelo).filter_by(usuario_id = usuario.usuario_id).first()
        
        if not(usuario_modelo):
            raise ValueError("Este usuario no existe.")
        
        self._sesion.delete(usuario_modelo)