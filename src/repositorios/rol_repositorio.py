from typing import Optional

from configuraciones.excepciones import NoEncontradoError
from modelos.rol_modelo import RolModelo


class RolRepositorio:
    def __init__(self, bd):
        self._bd = bd
    
    def obtener_por_id(self, rol_id: int) -> Optional[RolModelo]:
        with self._bd.sesion() as sesion:
            rol_modelo = sesion.query(RolModelo).filter_by(rol_id = rol_id).first()
            
            if not(rol_modelo):
                raise NoEncontradoError(["Este rol no existe"])
            
            return rol_modelo
    
    def obtener_por_tipo_rol(self, tipo_rol: str) -> Optional[RolModelo]:
        with self._bd.sesion() as sesion:
            rol_modelo = sesion.query(RolModelo).filter_by(tipo_rol = tipo_rol).first()
            
            if not(rol_modelo):
                raise NoEncontradoError(["Este rol no existe"])
            
            return rol_modelo