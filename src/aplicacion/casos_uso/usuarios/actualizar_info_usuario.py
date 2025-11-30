from dominio.excepciones import UsuarioValidacionError
from aplicacion.unidad_trabajo.unidad_trabajo_base import UnidadTrabajo
from aplicacion.unidad_trabajo.sqlalchemy_unidad_trabajo import SQLAlchemyUnidadTrabajo
from typing import Dict


class ActualizarInfoUsuario:
    def __init__(self, unidad_trabajo: UnidadTrabajo):
        self.unidad_trabajo = unidad_trabajo
    
    def ejecutar(self, usuario_id: int, usuario_id_logeado: int, nuevos_datos: Dict) -> None:
        with self.unidad_trabajo() as unidad_trabajo:
            try:
                errores = []
                
                usuario_a_actualizar = unidad_trabajo.usuario.obtener_por_id(usuario_id)
                rol_usuario_a_actualizar = usuario_a_actualizar.rol_id
                
                if not(usuario_a_actualizar):
                    errores.append("Este usuario no existe.")
                
                rol_existe = unidad_trabajo.rol.obtener_por_id(nuevos_datos.get("rol_id"))
                
                if not(rol_existe):
                    errores.append("Este rol no existe.")
                
                USUARIO_NO_ES_SI_MISMO = (usuario_id_logeado != usuario_id)
                USUARIO_ADMIN_DEFECTO = (usuario_id_logeado == 1)
                USUARIO_ACTUALIZAR_ES_ADMIN = (rol_usuario_a_actualizar == 1)
                
                if (((usuario_id_logeado != USUARIO_ADMIN_DEFECTO) and (USUARIO_ACTUALIZAR_ES_ADMIN)) and (USUARIO_NO_ES_SI_MISMO)):
                    errores.append("No puedes modificar la info de un Administrador.")
                
                if (usuario_a_actualizar):
                    usuario_a_actualizar.rol_id = nuevos_datos.get("rol_id", usuario_a_actualizar.rol_id)
                    usuario_a_actualizar.nombre_usuario = nuevos_datos.get("nombre_usuario", usuario_a_actualizar.nombre_usuario)
                    usuario_a_actualizar.clave_usuario = nuevos_datos.get("clave_usuario", usuario_a_actualizar.clave_usuario)
                    
                    errores_entidad = usuario_a_actualizar._validar_campos()
                    errores.extend(errores_entidad)
                
                if (errores):
                    raise UsuarioValidacionError(errores)
                
                unidad_trabajo.usuario.actualizar(usuario_a_actualizar)
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
        actualizar_info_usuario = ActualizarInfoUsuario(unidad_trabajo)
        
        nuevos_datos = {
            "rol_id": 1,
            "nombre_usuario": "alonchad",
            "clave_usuario": "qteimporta"
        }
        
        actualizar_info_usuario.ejecutar(1, nuevos_datos)
        print("Se actualizaron los datos del usuario correctamente.")
    except UsuarioValidacionError as error:
        print("\n".join(error.errores))
    except Exception as error:
        print(error)