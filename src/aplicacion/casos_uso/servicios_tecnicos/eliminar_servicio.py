from dominio.excepciones import ServicioValidacionError
from aplicacion.unidad_trabajo.unidad_trabajo_base import UnidadTrabajo
from aplicacion.unidad_trabajo.sqlalchemy_unidad_trabajo import SQLAlchemyUnidadTrabajo


class EliminarServicio:
    def __init__(self, unidad_trabajo: UnidadTrabajo):
        self.unidad_trabajo = unidad_trabajo
    
    def ejecutar(self, servicio_id: int) -> None:
        with self.unidad_trabajo() as unidad_trabajo:
            try:
                servicio_a_eliminar = unidad_trabajo.servicio.obtener_por_id(servicio_id)
                
                unidad_trabajo.servicio.eliminar(servicio_a_eliminar)
                unidad_trabajo.flush()
                unidad_trabajo.commit()
            except Exception:
                unidad_trabajo.rollback()
                raise error


if __name__ == "__main__":
    try:
        unidad_trabajo = SQLAlchemyUnidadTrabajo()
        eliminar_servicio = EliminarServicio(unidad_trabajo)
        
        eliminar_servicio.ejecutar(5)
        print("Se eliminó el servicio correctamente.")
    except ServicioValidacionError as error:
        print("\n".join(error.errores))
    except Exception as error:
        print(error)