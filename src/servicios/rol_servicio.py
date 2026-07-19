from typing import Optional

from modelos.rol_modelo import RolModelo
from repositorios.rol_repositorio import RolRepositorio


class RolServicio:
    def __init__(self, rol_repositorio: RolRepositorio):
        self._rol_repositorio = rol_repositorio
    
    def obtener_por_id(self, rol_id: int) -> Optional[RolModelo]:
        return self._rol_repositorio.obtener_por_id(rol_id)
    
    def obtener_por_tipo_rol(self, tipo_rol: str) -> Optional[RolModelo]:
        return self._rol_repositorio.obtener_por_tipo_rol(tipo_rol)