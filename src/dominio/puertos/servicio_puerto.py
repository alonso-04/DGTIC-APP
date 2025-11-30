from abc import ABC, abstractmethod
from typing import Generator, Optional, List, Tuple
from dominio.entidades.servicio import Servicio


class ServicioPuerto(ABC):
    @abstractmethod
    def registrar(self, servicio: Servicio) -> None:
        pass
    
    @abstractmethod
    def obtener_todos(self) -> Generator[List[Tuple], None, None]:
        pass
    
    @abstractmethod
    def obtener_por_id(self, servicio_id: int) -> Optional[List[Tuple]]:
        pass
    
    @abstractmethod
    def actualizar(self, servicio: Servicio) -> None:
        pass
    
    @abstractmethod
    def eliminar(self, servicio: Servicio) -> None:
        pass