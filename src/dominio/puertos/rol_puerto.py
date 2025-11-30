from abc import ABC, abstractmethod
from typing import Generator, Optional
from dominio.entidades.rol import Rol


class RolPuerto(ABC):
    @abstractmethod
    def obtener_todos(self) -> Generator[Rol, None, None]:
        pass
    
    @abstractmethod
    def obtener_por_id(self, rol_id: int) -> Optional[Rol]:
        pass