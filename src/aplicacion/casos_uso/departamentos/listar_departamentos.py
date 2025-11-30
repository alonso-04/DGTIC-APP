from dominio.entidades.departamento import Departamento
from dominio.excepciones import DepartamentoValidacionError
from aplicacion.unidad_trabajo.unidad_trabajo_base import UnidadTrabajo
from aplicacion.unidad_trabajo.sqlalchemy_unidad_trabajo import SQLAlchemyUnidadTrabajo
from typing import Optional, Generator


class ListarDepartamentos:
    def __init__(self, unidad_trabajo: UnidadTrabajo):
        self.unidad_trabajo = unidad_trabajo
    
    def obtener_todos(self) -> Generator[Departamento, None, None]:
        with self.unidad_trabajo() as unidad_trabajo:
            departamentos = unidad_trabajo.departamento.obtener_todos()
            return departamentos
    
    def obtener_por_id(self, departamento_id: int) -> Optional[Departamento]:
        with self.unidad_trabajo() as unidad_trabajo:
            try:
                errores = []
                
                departamento = unidad_trabajo.departamento.obtener_por_id(departamento_id)
                
                if not (departamento):
                    errores.append("Este departamento no existe.")
                
                if (errores):
                    raise DepartamentoValidacionError(errores)
                
                return departamento
            except DepartamentoValidacionError as error:
                raise error
    
    def obtener_por_nombre(self, nombre_departamento: str) -> Optional[Departamento]:
        with self.unidad_trabajo() as unidad_trabajo:
            try:
                errores = []
                
                departamento = unidad_trabajo.departamento.obtener_por_nombre(nombre_departamento)
                
                if not(departamento):
                    errores.append("Este departamento no existe.")
                
                if (errores):
                    raise DepartamentoValidacionError(errores)
                
                return departamento
            except DepartamentoValidacionError as error:
                raise error


if __name__ == "__main__":
    try:
        unidad_trabajo = SQLAlchemyUnidadTrabajo()
        listar_departamentos = ListarDepartamentos(unidad_trabajo)
        
        """for departamento in listar_departamentos.obtener_todos():
            print(departamento.nombre_departamento)"""
        
        #departamento = listar_departamentos.obtener_por_id(3)
        #print(departamento.nombre_departamento)
        
        departamento = listar_departamentos.obtener_por_nombre("1X10")
        print(departamento.departamento_id)
    except DepartamentoValidacionError as error:
        print("\n".join(error.errores))
    except Exception as error:
        print(f"ERROR INESPERADO: {error}")