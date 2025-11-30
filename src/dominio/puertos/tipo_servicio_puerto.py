from abc import ABC, abstractmethod
from typing import Generator, Optional
from dominio.entidades.tipo_servicio import TipoServicio


class TipoServicioPuerto(ABC):
    @abstractmethod
    def registrar(self, tipo_servicio: TipoServicio) -> None:
        pass
    
    @abstractmethod
    def obtener_todos(self) -> Generator[TipoServicio, None, None]:
        pass
    
    @abstractmethod
    def obtener_por_id(self, tipo_servicio_id: int) -> Optional[TipoServicio]:
        pass
    
    @abstractmethod
    def actualizar(self, tipo_servicio: TipoServicio) -> None:
        pass
    
    @abstractmethod
    def eliminar(self, tipo_servicio: TipoServicio) -> None:
        pass