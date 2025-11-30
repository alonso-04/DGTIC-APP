from dominio.entidades.usuario import Usuario
from dominio.excepciones import UsuarioValidacionError
from aplicacion.unidad_trabajo.unidad_trabajo_base import UnidadTrabajo
from aplicacion.unidad_trabajo.sqlalchemy_unidad_trabajo import SQLAlchemyUnidadTrabajo
from typing import Optional, Generator


class ListarUsuarios:
    def __init__(self, unidad_trabajo: UnidadTrabajo):
        self.unidad_trabajo = unidad_trabajo
    
    def obtener_todos(self) -> Generator[Usuario, None, None]:
        with self.unidad_trabajo() as unidad_trabajo:
            usuarios = unidad_trabajo.usuario.obtener_todos()
            return usuarios
    
    def obtener_por_id(self, usuario_id: int) -> Optional[Usuario]:
        with self.unidad_trabajo() as unidad_trabajo:
            try:
                errores = []
                
                usuario = unidad_trabajo.usuario.obtener_por_id(usuario_id)

                if not(usuario):
                    errores.append("Este usuario no existe.")
                
                if (errores):
                    raise UsuarioValidacionError(errores)
                
                return usuario
            except UsuarioValidacionError as error:
                raise error
        
    def obtener_por_nombre_usuario(self, nombre_usuario: str) -> Optional[Usuario]:
        with self.unidad_trabajo() as unidad_trabajo:
            try:
                errores = []
                
                usuario = unidad_trabajo.usuario.obtener_por_nombre_usuario(nombre_usuario)
                
                if not(usuario):
                    errores.append("Usuario: Este usuario no existe.")
                
                if (errores):
                    raise UsuarioValidacionError(errores)
                
                return usuario
            except UsuarioValidacionError as error:
                raise error


if __name__ == "__main__":
    try:
        unidad_trabajo = SQLAlchemyUnidadTrabajo()
        listar_usuarios = ListarUsuarios(unidad_trabajo)
        
        """usuarios = listar_usuarios.obtener_todos()
        
        for usuario in usuarios:
            print(usuario.nombre_usuario)"""
        
        """usuario = listar_usuarios.obtener_por_id(4)
        print(usuario.nombre_usuario)"""
        
        usuario = listar_usuarios.obtener_por_nombre_usuario("alonso124")
        print(usuario.nombre_usuario)
    
    except UsuarioValidacionError as error:
        print("\n".join(error.errores))
    except Exception as error:
        print(error)