from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from infraestructura.conexiones.conexion import Base


class TipoServicioModelo(Base):
    __tablename__ = "tb_tipos_servicio"
    
    tipo_servicio_id = Column(Integer, primary_key = True, autoincrement = True)
    tipo_servicio_prestado = Column(String(120), unique = True, nullable = False)
    
    servicio = relationship("ServicioModelo", back_populates = "tipo_servicio")