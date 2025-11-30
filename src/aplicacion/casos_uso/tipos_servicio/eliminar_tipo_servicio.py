from dominio.excepciones import TipoServicioValidacionError
from aplicacion.unidad_trabajo.unidad_trabajo_base import UnidadTrabajo
from aplicacion.unidad_trabajo.sqlalchemy_unidad_trabajo import SQLAlchemyUnidadTrabajo


class EliminarTipoServicio:
    def __init__(self, unidad_trabajo: UnidadTrabajo):
        self.unidad_trabajo = unidad_trabajo
    
    def ejecutar(self, tipo_servicio_id: int) -> None:
        with self.unidad_trabajo() as unidad_trabajo:
            try:
                errores = []
                
                tipo_servicio_a_eliminar = unidad_trabajo.tipo_servicio.obtener_por_id(tipo_servicio_id)
                
                if not(tipo_servicio_a_eliminar):
                    errores.append("Este tipo de servicio no existe.")
                
                servicios_asociados = list(unidad_trabajo.servicio.obtener_por_tipo_servicio_id(tipo_servicio_id))
                
                if (servicios_asociados):
                    errores.append("Este tipo de servicio está asociado a 1 o más servicios y no se puede eliminar.")
                
                if (errores):
                    raise TipoServicioValidacionError(errores)
                
                unidad_trabajo.tipo_servicio.eliminar(tipo_servicio_a_eliminar)
                unidad_trabajo.flush()
                unidad_trabajo.commit()
            except TipoServicioValidacionError as error:
                unidad_trabajo.rollback()
                raise error
            except Exception as error:
                unidad_trabajo.rollback()
                raise error


if __name__ == "__main__":
    try:
        unidad_trabajo = SQLAlchemyUnidadTrabajo
        eliminar_tipo_servicio = EliminarTipoServicio(unidad_trabajo)
        
        eliminar_tipo_servicio.ejecutar(2)
        print("Se eliminó el tipo de servicio correctamente.")
    except TipoServicioValidacionError as error:
        print("\n".join(error.errores))
    except Exception as error:
        print(error)