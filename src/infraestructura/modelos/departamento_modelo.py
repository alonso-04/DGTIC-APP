from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from infraestructura.conexiones.conexion import Base


class DepartamentoModelo(Base):
    __tablename__ = "tb_departamentos"
    
    departamento_id = Column(Integer, primary_key = True, autoincrement = True)
    nombre_departamento = Column(String(120), nullable = False, unique = True)
    
    servicio = relationship("ServicioModelo", back_populates = "departamento", cascade = "save-update, merge")