from sqlalchemy.orm import Session
from dominio.entidades.rol import Rol
from dominio.puertos.rol_puerto import RolPuerto
from infraestructura.modelos.rol_modelo import RolModelo
from typing import Optional, Generator


class RolAdaptador(RolPuerto):
    def __init__(self, sesion: Session):
        self._sesion = sesion
    
    def obtener_todos(self) -> Generator[Rol, None, None]:
        roles_modelo = self._sesion.query(RolModelo).yield_per(10)
        
        for rol in roles_modelo:
            yield Rol(
                rol_id = rol.rol_id,
                tipo_rol = rol.tipo_rol
            )
    
    def obtener_por_id(self, rol_id: int) -> Optional[Rol]:
        rol_modelo = self._sesion.query(RolModelo).filter_by(rol_id = rol_id).first()
        
        if (rol_modelo):
            return Rol(
                rol_id = rol_modelo.rol_id,
                tipo_rol = rol_modelo.tipo_rol
            )
        return None
    
    def obtener_por_tipo_rol(self, tipo_rol: str) -> Optional[Rol]:
        rol_modelo = self._sesion.query(RolModelo).filter_by(tipo_rol = tipo_rol).first()
        
        if (rol_modelo):
            return Rol(
                rol_id = rol_modelo.rol_id,
                tipo_rol = rol_modelo.tipo_rol
            )
        return None