from sqlalchemy.orm import Session
from dominio.entidades.departamento import Departamento
from dominio.puertos.departamento_puerto import DepartamentoPuerto
from infraestructura.modelos.departamento_modelo import DepartamentoModelo
from typing import Optional, Generator


class DepartamentoAdaptador(DepartamentoPuerto):
    def __init__(self, sesion: Session):
        self._sesion = sesion
    
    def registrar(self, departamento: Departamento) -> None:
        departamento_modelo = DepartamentoModelo(nombre_departamento = departamento.nombre_departamento)
        self._sesion.add(departamento_modelo)
    
    def obtener_todos(self) -> Generator[Departamento, None, None]:
        departamentos_modelo = self._sesion.query(DepartamentoModelo).yield_per(100)
        
        for departamento in departamentos_modelo:
            yield Departamento(
                departamento_id = departamento.departamento_id,
                nombre_departamento = departamento.nombre_departamento
            )
    
    def obtener_por_id(self, departamento_id: int) -> Optional[Departamento]:
        departamento_modelo = self._sesion.query(DepartamentoModelo).filter_by(departamento_id = departamento_id).first()
        
        if (departamento_modelo):
            return Departamento(
                departamento_id = departamento_modelo.departamento_id,
                nombre_departamento = departamento_modelo.nombre_departamento
            )
        return None
    
    def obtener_por_nombre(self, nombre_departamento: str) -> Optional[Departamento]:
        departamento_modelo = self._sesion.query(DepartamentoModelo).filter_by(nombre_departamento = nombre_departamento).first()
        
        if (departamento_modelo):
            return Departamento(
                departamento_id = departamento_modelo.departamento_id,
                nombre_departamento = departamento_modelo.nombre_departamento
            )
        return None
    
    def actualizar(self, departamento: Departamento) -> None:
        departamento_modelo = self._sesion.query(DepartamentoModelo).filter_by(departamento_id = departamento.departamento_id).first()
        
        if not(departamento_modelo):
            raise ValueError("Este departamento no existe.")
        
        departamento_modelo.nombre_departamento = departamento.nombre_departamento
    
    def eliminar(self, departamento: Departamento) -> None:
        departamento_modelo = self._sesion.query(DepartamentoModelo).filter_by(departamento_id = departamento.departamento_id).first()
        
        if not(departamento_modelo):
            raise ValueError("Este departamento no existe.")
        
        self._sesion.delete(departamento_modelo)