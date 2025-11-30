from dominio.excepciones import DepartamentoValidacionError
from aplicacion.unidad_trabajo.unidad_trabajo_base import UnidadTrabajo
from aplicacion.unidad_trabajo.sqlalchemy_unidad_trabajo import SQLAlchemyUnidadTrabajo


class EliminarDepartamento:
    def __init__(self, unidad_trabajo: UnidadTrabajo):
        self.unidad_trabajo = unidad_trabajo
    
    def ejecutar(self, departamento_id: int) -> None:
        with self.unidad_trabajo() as unidad_trabajo:
            try:
                errores = []
                
                departamento_a_eliminar = unidad_trabajo.departamento.obtener_por_id(departamento_id)
                
                if not(departamento_a_eliminar):
                    errores.append("Este departamento no existe.")
                
                servicios_asociados = list(unidad_trabajo.servicio.obtener_por_departamento_id(departamento_id))
                
                if (servicios_asociados):
                    errores.append("Este departamento está asociado a 1 o más servicios y no se puede eliminar.")
                
                if (errores):
                    raise DepartamentoValidacionError(errores)
                
                unidad_trabajo.departamento.eliminar(departamento_a_eliminar)
                unidad_trabajo.flush()
                unidad_trabajo.commit()
            except DepartamentoValidacionError as error:
                unidad_trabajo.rollback()
                raise error
            except Exception:
                unidad_trabajo.rollback()


if __name__ == "__main__":
    try:
        unidad_trabajo = SQLAlchemyUnidadTrabajo()
        eliminar_departamento = EliminarDepartamento(unidad_trabajo)
        
        #eliminar_departamento.ejecutar(3)  No se puede eliminar porque está asociado a 1 o más servicios
        eliminar_departamento.ejecutar(2)
        print("Se eliminó el departamento correctamente.")
    except DepartamentoValidacionError as error:
        print("\n".join(error.errores))
    except Exception as error:
        print(f"ERROR INESPERADO: {error}")