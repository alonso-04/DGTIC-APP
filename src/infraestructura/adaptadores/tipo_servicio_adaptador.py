from sqlalchemy.orm import Session
from dominio.entidades.tipo_servicio import TipoServicio
from dominio.puertos.tipo_servicio_puerto import TipoServicioPuerto
from infraestructura.modelos.tipo_servicio_modelo import TipoServicioModelo
from typing import Optional, Generator


class TipoServicioAdaptador(TipoServicioPuerto):
    def __init__(self, sesion: Session):
        self._sesion = sesion
    
    def registrar(self, tipo_servicio: TipoServicio) -> None:
        tipo_servicio_modelo = TipoServicioModelo(
            tipo_servicio_prestado = tipo_servicio.tipo_servicio_prestado
        )
        
        self._sesion.add(tipo_servicio_modelo)
    
    def obtener_todos(self) -> Generator[TipoServicio, None, None]:
        tipos_servicio_modelo = self._sesion.query(TipoServicioModelo).yield_per(100)
        
        for tipo_servicio in tipos_servicio_modelo:
            yield TipoServicio(
                tipo_servicio_id = tipo_servicio.tipo_servicio_id,
                tipo_servicio_prestado = tipo_servicio.tipo_servicio_prestado
            )
    
    def obtener_por_id(self, tipo_servicio_id: int) -> Optional[TipoServicio]:
        tipo_servicio_modelo = self._sesion.query(TipoServicioModelo).filter_by(tipo_servicio_id = tipo_servicio_id).first()
        
        if (tipo_servicio_modelo):
            return TipoServicio(
                tipo_servicio_id = tipo_servicio_modelo.tipo_servicio_id,
                tipo_servicio_prestado = tipo_servicio_modelo.tipo_servicio_prestado
            )
        return None
    
    def obtener_por_tipo_servicio(self, tipo_servicio_prestado: str) -> Optional[TipoServicio]:
        tipo_servicio_modelo = self._sesion.query(TipoServicioModelo).filter_by(tipo_servicio_prestado = tipo_servicio_prestado).first()
        
        if (tipo_servicio_modelo):
            return TipoServicio(
                tipo_servicio_id = tipo_servicio_modelo.tipo_servicio_id,
                tipo_servicio_prestado = tipo_servicio_modelo.tipo_servicio_prestado
            )
        return None
    
    def actualizar(self, tipo_servicio: TipoServicio) -> None:
        tipo_servicio_modelo = self._sesion.query(TipoServicioModelo).filter_by(tipo_servicio_id = tipo_servicio.tipo_servicio_id).first()
        
        if not(tipo_servicio_modelo):
            raise ValueError("Este tipo de servicio no existe.")
        
        tipo_servicio_modelo.tipo_servicio_id = tipo_servicio.tipo_servicio_id
        tipo_servicio_modelo.tipo_servicio_prestado = tipo_servicio.tipo_servicio_prestado
    
    def eliminar(self, tipo_servicio: TipoServicio) -> None:
        tipo_servicio_modelo = self._sesion.query(TipoServicioModelo).filter_by(tipo_servicio_id = tipo_servicio.tipo_servicio_id).first()
        
        if not(tipo_servicio_modelo):
            raise ValueError("Este tipo de servicio no existe.")
        
        self._sesion.delete(tipo_servicio_modelo)