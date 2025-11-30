from abc import ABC, abstractmethod
from typing import Generator, Optional
from dominio.entidades.usuario import Usuario


class UsuarioPuerto(ABC):
    @abstractmethod
    def registrar(self, usuario: Usuario) -> None:
        pass
    
    @abstractmethod
    def obtener_todos(self) -> Generator[Usuario, None, None]:
        pass
    
    @abstractmethod
    def obtener_por_id(self, usuario_id: int) -> Optional[Usuario]:
        pass
    
    @abstractmethod
    def actualizar(self, usuario: Usuario) -> None:
        pass
    
    @abstractmethod
    def eliminar(self, usuario: Usuario) -> None:
        pass