from dominio.excepciones import UsuarioValidacionError
from aplicacion.unidad_trabajo.unidad_trabajo_base import UnidadTrabajo
from aplicacion.unidad_trabajo.sqlalchemy_unidad_trabajo import SQLAlchemyUnidadTrabajo


class EliminarUsuario:
    def __init__(self, unidad_trabajo: UnidadTrabajo):
        self.unidad_trabajo = unidad_trabajo
    
    def ejecutar(self, usuario_id: int, usuario_id_logeado: int) -> None:
        with self.unidad_trabajo() as unidad_trabajo:
            try:
                errores = []
                
                usuario_a_eliminar = unidad_trabajo.usuario.obtener_por_id(usuario_id)
                rol_usuario_a_eliminar = usuario_a_eliminar.rol_id
                ROL_ID_ADMIN = 1
                
                if (usuario_id == 1):
                    errores.append("Este usuario administrador no puede eliminarse porque es el predeterminado del sistema.")
                
                if (usuario_id_logeado == usuario_id):
                    errores.append("No puedes eliminarte a ti mismo.")
                
                if ((usuario_id != usuario_id_logeado) and (rol_usuario_a_eliminar == ROL_ID_ADMIN) and (usuario_id_logeado != 1)):
                    errores.append("No puedes eliminar a un usuario Administrador.")
                
                if (errores):
                    raise UsuarioValidacionError(errores)
                
                unidad_trabajo.usuario.eliminar(usuario_a_eliminar)
                unidad_trabajo.flush()
                unidad_trabajo.commit()
            except UsuarioValidacionError as error:
                unidad_trabajo.rollback()
                raise error
            except Exception:
                unidad_trabajo.rollback()


if __name__ == "__main__":
    try:
        unidad_trabajo = SQLAlchemyUnidadTrabajo()
        eliminar_usuario = EliminarUsuario(unidad_trabajo)
        
        #eliminar_usuario.ejecutar(4)
        print("Se eliminó el usuario correctamente.")
    except UsuarioValidacionError as error:
        print("\n".join(error.errores))
    except Exception as error:
        print(error)