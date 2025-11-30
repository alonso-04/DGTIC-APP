from dominio.entidades.servicio import Servicio
from dominio.excepciones import ServicioValidacionError
from aplicacion.unidad_trabajo.unidad_trabajo_base import UnidadTrabajo
from aplicacion.unidad_trabajo.sqlalchemy_unidad_trabajo import SQLAlchemyUnidadTrabajo
from datetime import date


class RegistrarServicio:
    def __init__(self, unidad_trabajo: UnidadTrabajo):
        self.unidad_trabajo = unidad_trabajo
    
    def ejecutar(self, servicio: Servicio) -> None:
        with self.unidad_trabajo() as unidad_trabajo:
            try:
                errores = []
                
                errores_entidad = servicio._validar_campos()
                errores.extend(errores_entidad)
                
                if (errores):
                    raise ServicioValidacionError(errores)
                
                unidad_trabajo.servicio.registrar(servicio)
                unidad_trabajo.flush()
                unidad_trabajo.commit()
            except ServicioValidacionError as error:
                unidad_trabajo.rollback()
                raise error
            except Exception:
                unidad_trabajo.rollback()


if __name__ == "__main__":
    try:
        unidad_trabajo = SQLAlchemyUnidadTrabajo()
        registrar_servicio = RegistrarServicio(unidad_trabajo)
        
        servicio = Servicio(
            departamento_id = 1,
            fecha_servicio = date.today(),
            falla_presenta = "NO RECONOCE LAS IMPRESORAS OTRA VEZ.",
            servicio_prestado = "DESINSTALAR Y REINSTALAR EL CONTROLADOR DE IMPRESORA.",
            nombres_tecnicos = "GABRIEL, LUIS, CRISTIAN"
        )
        
        registrar_servicio.ejecutar(servicio)
        print("El servicio se registró correctamente.")
    except ServicioValidacionError as error:
        print("\n".join(error.errores))
    except Exception as error:
        print(error)