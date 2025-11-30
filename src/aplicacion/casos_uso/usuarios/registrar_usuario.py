from dominio.entidades.usuario import Usuario
from dominio.excepciones import UsuarioValidacionError
from aplicacion.unidad_trabajo.unidad_trabajo_base import UnidadTrabajo
from aplicacion.unidad_trabajo.sqlalchemy_unidad_trabajo import SQLAlchemyUnidadTrabajo
from utilidades.hasher import hashear_contenido


class RegistrarUsuario:
    def __init__(self, unidad_trabajo: UnidadTrabajo):
        self.unidad_trabajo = unidad_trabajo
    
    def ejecutar(self, usuario: Usuario) -> None:
        with self.unidad_trabajo() as unidad_trabajo:
            try:
                errores = []
                
                nuevo_usuario = Usuario(
                    rol_id = usuario.rol_id,
                    nombre_usuario = usuario.nombre_usuario,
                    clave_usuario = usuario.clave_usuario
                )
                
                nombre_usuario_existe = unidad_trabajo.usuario.obtener_por_nombre_usuario(nuevo_usuario.nombre_usuario)
                
                if (nombre_usuario_existe):
                    errores.append("Este nombre de usuario ya existe.")
                
                errores_entidad = nuevo_usuario._validar_campos()
                errores.extend(errores_entidad)
                
                nuevo_usuario.clave_usuario = hashear_contenido(usuario.clave_usuario)
                
                if (errores):
                    raise UsuarioValidacionError(errores)
                
                unidad_trabajo.usuario.registrar(nuevo_usuario)
                unidad_trabajo.flush()
                unidad_trabajo.commit()
            except UsuarioValidacionError as error:
                unidad_trabajo.rollback()
                raise error
            except Exception as error:
                unidad_trabajo.rollback()
                raise error


if __name__ == "__main__":
    try:
        unidad_trabajo = SQLAlchemyUnidadTrabajo()
        registrar_usuario = RegistrarUsuario(unidad_trabajo)
        
        usuario = Usuario(
            rol_id = 2,
            nombre_usuario = "njd-luis",
            clave_usuario = "untitled"
        )
        
        registrar_usuario.ejecutar(usuario)
        print("Se registró el usuario correctamente")
    except UsuarioValidacionError as error:
        print("\n".join(error.errores))
    except Exception as error:
        print(error)