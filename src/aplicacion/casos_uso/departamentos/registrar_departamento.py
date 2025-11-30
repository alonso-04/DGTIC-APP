from dominio.entidades.departamento import Departamento
from dominio.excepciones import DepartamentoValidacionError
from aplicacion.unidad_trabajo.unidad_trabajo_base import UnidadTrabajo
from aplicacion.unidad_trabajo.sqlalchemy_unidad_trabajo import SQLAlchemyUnidadTrabajo


class RegistrarDepartamento:
    def __init__(self, unidad_trabajo: UnidadTrabajo):
        self.unidad_trabajo = unidad_trabajo
    
    def ejecutar(self, departamento: Departamento) -> None:
        with self.unidad_trabajo() as unidad_trabajo:
            try:
                errores = []
                    
                nuevo_departamento = Departamento(nombre_departamento = departamento.nombre_departamento)
                departamento_existe = unidad_trabajo.departamento.obtener_por_nombre(
                    nuevo_departamento.nombre_departamento
                )
                    
                if (departamento_existe):
                    errores.append("Este departamento ya existe.")
                else:
                    errores_entidad = nuevo_departamento._validar_campos()
                    errores.extend(errores_entidad)
                    
                if (errores):
                    raise DepartamentoValidacionError(errores)
                    
                unidad_trabajo.departamento.registrar(nuevo_departamento)
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
        registrar_departamento = RegistrarDepartamento(unidad_trabajo)
        
        # departamento = Departamento("") Dirá que No puede estar vacío
        departamento = Departamento("RECURSOS HUMANOS") # Dirá que ya existe (si ya se ejecutó una vez)
        
        registrar_departamento.ejecutar(departamento)
        print("Se registró el departamento correctamente.")
    except DepartamentoValidacionError as error:
        print("\n".join(error.errores))
    except Exception as error:
        print(f"ERROR INESPERADO: {error}")