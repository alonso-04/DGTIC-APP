from abc import ABC, abstractmethod


class BaseDatos(ABC):
    @abstractmethod
    def obtener_fabrica_sesiones(self):
        pass
    
    @abstractmethod
    def crear_sesion(self):
        pass