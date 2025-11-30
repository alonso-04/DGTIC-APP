from abc import ABC, abstractmethod
from typing import Generator, Optional
from dominio.entidades.departamento import Departamento


class DepartamentoPuerto(ABC):
    @abstractmethod
    def registrar(self, departamento: Departamento) -> None:
        pass
    
    @abstractmethod
    def obtener_todos(self) -> Generator[Departamento, None, None]:
        pass
    
    @abstractmethod
    def obtener_por_id(self, departamento_id: int) -> Optional[Departamento]:
        pass
    
    @abstractmethod
    def actualizar(self, departamento: Departamento) -> None:
        pass
    
    @abstractmethod
    def eliminar(self, departamento: Departamento) -> None:
        pass