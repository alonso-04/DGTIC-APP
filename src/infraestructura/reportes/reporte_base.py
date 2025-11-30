from abc import ABC, abstractmethod
from typing import List, Any


class ReporteBase(ABC):
    @abstractmethod
    def exportar(self, datos: List) -> Any:
        pass