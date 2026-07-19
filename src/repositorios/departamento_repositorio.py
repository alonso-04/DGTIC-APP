from typing import Optional, Generator, Tuple
from sqlalchemy import text

from configuraciones.excepciones import NoEncontradoError
from modelos.departamento_modelo import DepartamentoModelo


class DepartamentoRepositorio:
    def __init__(self, bd):
        self._bd = bd
    
    def registrar(self, departamento: DepartamentoModelo) -> None:
        with self._bd.sesion() as sesion:
            sesion.add(departamento)
    
    def obtener_todos(self) -> Generator[DepartamentoModelo, None, None]:
        with self._bd.sesion() as sesion:
            departamentos_modelo = sesion.query(DepartamentoModelo).yield_per(100)
            
            for departamento in departamentos_modelo:
                yield departamento
    
    def obtener_por_id(self, departamento_id: int) -> Optional[DepartamentoModelo]:
        with self._bd.sesion() as sesion:
            departamento_modelo = sesion.query(DepartamentoModelo).filter_by(departamento_id = departamento_id).first()
            
            if not(departamento_modelo):
                raise NoEncontradoError(["Este departamento no existe"])
            
            return departamento_modelo
    
    def obtener_por_nombre(self, nombre_departamento: str) -> Optional[DepartamentoModelo]:
        with self._bd.sesion() as sesion:
            departamento_modelo = sesion.query(DepartamentoModelo).filter_by(nombre_departamento = nombre_departamento).first()
            
            if not(departamento_modelo):
                raise NoEncontradoError(["Este departamento no existe"])
            
            return departamento_modelo
    
    def obtener_por_nombre_o_todos(self, nombre_departamento: Optional[str]) -> Generator[Tuple, None, None]:
        with self._bd.sesion() as sesion:
            consulta = """
                SELECT
                    departamento_id,
                    nombre_departamento
                FROM tb_departamentos
            """
            
            parametros = {}
            condiciones_adicionales = []
            
            if (nombre_departamento):
                condiciones_adicionales.append("nombre_departamento = :nombre_departamento")
                parametros["nombre_departamento"] = nombre_departamento
            
            if (condiciones_adicionales):
                consulta += f"WHERE {condiciones_adicionales[0]}"
            
            departamentos_modelo = sesion.execute(text(consulta), parametros).yield_per(100)
            for departamento in departamentos_modelo:
                yield departamento
    
    def actualizar(self, departamento: DepartamentoModelo) -> None:
        with self._bd.sesion() as sesion:
            departamento_modelo = sesion.query(DepartamentoModelo).filter_by(departamento_id = departamento.departamento_id).first()
            nuevo_nombre_departamento = departamento.nombre_departamento
            departamento_modelo.nombre_departamento = nuevo_nombre_departamento
    
    def eliminar(self, departamento: DepartamentoModelo) -> None:
        with self._bd.sesion() as sesion:
            departamento_modelo = sesion.query(DepartamentoModelo).filter_by(departamento_id = departamento.departamento_id).first()
            sesion.delete(departamento_modelo)