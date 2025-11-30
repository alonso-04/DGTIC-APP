from dominio.entidades.tipo_servicio import TipoServicio
from dominio.excepciones import TipoServicioValidacionError
from aplicacion.unidad_trabajo.unidad_trabajo_base import UnidadTrabajo
from aplicacion.unidad_trabajo.sqlalchemy_unidad_trabajo import SQLAlchemyUnidadTrabajo


class RegistrarTipoServicio:
    def __init__(self, unidad_trabajo: UnidadTrabajo):
        self.unidad_trabajo = unidad_trabajo
    
    def ejecutar(self, tipo_servicio: TipoServicio):
        with self.unidad_trabajo() as unidad_trabajo:
            try:
                errores = []
                
                tipo_servicio_existe = unidad_trabajo.tipo_servicio.obtener_por_tipo_servicio(tipo_servicio.tipo_servicio_prestado)
                
                if (tipo_servicio_existe):
                    errores.append("Este tipo de servicio ya existe.")
                
                errores_entidad = tipo_servicio._validar_campos()
                errores.extend(errores_entidad)
                
                if (errores):
                    raise TipoServicioValidacionError(errores)
                
                unidad_trabajo.tipo_servicio.registrar(tipo_servicio)
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
        registrar_tipo_servicio = RegistrarTipoServicio(unidad_trabajo)
        
        nuevo_tipo_servicio = TipoServicio(
            tipo_servicio_prestado = None
        )
        
        registrar_tipo_servicio.ejecutar(nuevo_tipo_servicio)
        print("Se registró el tipo de servicio correctamente.")
    except TipoServicioValidacionError as error:
        print("\n".join(error.errores))
    except Exception as error:
        print(error)