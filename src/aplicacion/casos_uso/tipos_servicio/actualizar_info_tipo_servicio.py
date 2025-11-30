from dominio.excepciones import TipoServicioValidacionError
from aplicacion.unidad_trabajo.unidad_trabajo_base import UnidadTrabajo
from aplicacion.unidad_trabajo.sqlalchemy_unidad_trabajo import SQLAlchemyUnidadTrabajo
from typing import Dict


class ActualizarInfoTipoServicio:
    def __init__(self, unidad_trabajo: UnidadTrabajo):
        self.unidad_trabajo = unidad_trabajo
    
    def ejecutar(self, tipo_servicio_id: int, nuevos_datos: Dict) -> None:
        with self.unidad_trabajo() as unidad_trabajo:
            try:
                errores = []
                
                tipo_servicio_a_actualizar = unidad_trabajo.tipo_servicio.obtener_por_id(tipo_servicio_id)
                
                if not(tipo_servicio_a_actualizar):
                    errores.append("Este tipo de servicio no existe.")
                
                if (tipo_servicio_a_actualizar):
                    nuevo_tipo_servicio_prestado = nuevos_datos.get("tipo_servicio_prestado", tipo_servicio_a_actualizar.tipo_servicio_prestado)
                    
                    tipo_servicio_ya_existe = unidad_trabajo.tipo_servicio.obtener_por_tipo_servicio(nuevo_tipo_servicio_prestado)

                    if ((tipo_servicio_ya_existe is not None) and (tipo_servicio_ya_existe.tipo_servicio_id != tipo_servicio_a_actualizar.tipo_servicio_id)):
                        errores.append("Este tipo de servicio ya existe.")
                    
                    tipo_servicio_a_actualizar.tipo_servicio_prestado = nuevo_tipo_servicio_prestado
                    errores_entidad = tipo_servicio_a_actualizar._validar_campos()
                    errores.extend(errores_entidad)
                
                if (errores):
                    raise TipoServicioValidacionError(errores)
                
                unidad_trabajo.tipo_servicio.actualizar(tipo_servicio_a_actualizar)
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
        actualizar_info_tipo_servicio = ActualizarInfoTipoServicio(unidad_trabajo)
        
        nuevos_datos = {
            "tipo_servicio_prestado": "RECARGA DE TINTA A IMPRESORA"
        }
        
        actualizar_info_tipo_servicio.ejecutar(1, nuevos_datos)
        print("Se actualizó el tipo de servicio correctamente.")
    except TipoServicioValidacionError as error:
        print("\n".join(error.errores))
    except Exception as error:
        print(error)