from dominio.excepciones import ServicioValidacionError
from aplicacion.unidad_trabajo.unidad_trabajo_base import UnidadTrabajo
from aplicacion.unidad_trabajo.sqlalchemy_unidad_trabajo import SQLAlchemyUnidadTrabajo
from typing import Dict
from datetime import date


class ActualizarInfoServicio:
    def __init__(self, unidad_trabajo: UnidadTrabajo):
        self.unidad_trabajo = unidad_trabajo
    
    def ejecutar(self, servicio_id: int, nuevos_datos: Dict) -> None:
        with self.unidad_trabajo() as unidad_trabajo:
            try:
                errores = []
                
                servicio_a_actualizar = unidad_trabajo.servicio.obtener_por_id(servicio_id)
                
                if (servicio_a_actualizar):
                    servicio_a_actualizar.fecha_servicio = nuevos_datos.get("fecha_servicio", servicio_a_actualizar.fecha_servicio)
                    servicio_a_actualizar.falla_presenta = nuevos_datos.get("falla_presenta", servicio_a_actualizar.falla_presenta)
                    servicio_a_actualizar.tipo_servicio_id = nuevos_datos.get("tipo_servicio_id", servicio_a_actualizar.tipo_servicio_id)
                    servicio_a_actualizar.nombres_tecnicos = nuevos_datos.get("nombres_tecnicos", servicio_a_actualizar.nombres_tecnicos)
                    servicio_a_actualizar.observaciones_adicionales = nuevos_datos.get("observaciones_adicionales", servicio_a_actualizar.observaciones_adicionales)
                    servicio_a_actualizar.departamento_id = nuevos_datos.get("departamento_id", servicio_a_actualizar.departamento_id)
                    
                    errores_entidad = servicio_a_actualizar._validar_campos()
                    errores.extend(errores_entidad)
                
                if (errores):
                    raise ServicioValidacionError(errores)
                
                unidad_trabajo.servicio.actualizar(servicio_a_actualizar)
                unidad_trabajo.flush()
                unidad_trabajo.commit()
            except ServicioValidacionError as error:
                unidad_trabajo.rollback()
                raise error
            except Exception as error:
                unidad_trabajo.rollback()
                raise error


if __name__ == "__main__":
    try:
        unidad_trabajo = SQLAlchemyUnidadTrabajo
        actualizar_info_servicio = ActualizarInfoServicio(unidad_trabajo)
        
        nuevos_datos = {
            "departamento_id": 4,
            "fecha_servicio": date.today(),
            "falla_presenta": "NO IMPRIME",
            "tipo_servicio_id": 1,
            "nombres_tecnicos": "GABRIEL"
        }
        
        actualizar_info_servicio.ejecutar(4, nuevos_datos)
        print("Se actualizó la info del servicio correctamente.")
    except ServicioValidacionError as error:
        print("\n".join(error.errores))
    except Exception as error:
        print(error)