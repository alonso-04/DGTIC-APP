from abc import ABC, abstractmethod


class RespaldoBase(ABC):
    @abstractmethod
    def exportar(self):
        pass
    
    @abstractmethod
    def importar(self):
        pass