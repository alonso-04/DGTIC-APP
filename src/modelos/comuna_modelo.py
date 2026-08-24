from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from configuraciones.conexion  import Base


class ComunaModelo(Base):
    __tablename__ = "tb_comunas"
    
    comuna_id = Column(Integer, primary_key = True, autoincrement = True)
    nombre_comuna = Column(String(100), unique = True, nullable = False)
    
    servicio = relationship("ServicioTecnicoModelo", back_populates = "comuna")