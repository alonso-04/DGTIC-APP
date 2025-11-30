from dominio.excepciones import DepartamentoValidacionError
from aplicacion.unidad_trabajo.unidad_trabajo_base import UnidadTrabajo
from aplicacion.unidad_trabajo.sqlalchemy_unidad_trabajo import SQLAlchemyUnidadTrabajo
from typing import Dict


class ActualizarInfoDepartamento:
    def __init__(self, unidad_trabajo: UnidadTrabajo):
        self.unidad_trabajo = unidad_trabajo
    
    def ejecutar(self, departamento_id: int, nuevos_datos: Dict) -> None:
        with self.unidad_trabajo() as unidad_trabajo:
            try:
                errores = []
                
                departamento_a_actualizar = unidad_trabajo.departamento.obtener_por_id(departamento_id)
                
                if not(departamento_a_actualizar):
                    errores.append("Este departamento no existe.")
                
                if (departamento_a_actualizar):
                    nuevo_nombre_departamento = nuevos_datos.get("nombre_departamento",departamento_a_actualizar.nombre_departamento)
                    
                    departamento_ya_existe = unidad_trabajo.departamento.obtener_por_nombre(nuevo_nombre_departamento)
                    
                    if ((departamento_ya_existe is not None) and (departamento_ya_existe.departamento_id != departamento_a_actualizar.departamento_id)):
                        errores.append("Este departamento ya existe.")
                    
                    departamento_a_actualizar.nombre_departamento = nuevo_nombre_departamento
                    errores_entidad = departamento_a_actualizar._validar_campos()
                    errores.extend(errores_entidad)
                
                if (errores):
                    raise DepartamentoValidacionError(errores)
                
                unidad_trabajo.departamento.actualizar(departamento_a_actualizar)
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
        actualizar_info_departamento = ActualizarInfoDepartamento(unidad_trabajo)
        
        nuevos_datos = {
            "nombre_departamento": "1X14"
        }
        
        actualizar_info_departamento.ejecutar(1, nuevos_datos)
        print("Se actualizaron los datos del departamento correctamente.")
    except DepartamentoValidacionError as error:
        print("\n".join(error.errores))
    except ValueError as error:
        print(error)
    except Exception as error:
        print(f"ERROR INESPERADO: {error}")