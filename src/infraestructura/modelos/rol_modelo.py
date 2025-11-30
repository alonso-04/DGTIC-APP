from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from infraestructura.conexiones.conexion import Base


class RolModelo(Base):
    __tablename__ = "tb_roles"
    
    rol_id = Column(Integer, primary_key = True, autoincrement = True)
    tipo_rol = Column(String(15), nullable = False)
    
    usuario = relationship("UsuarioModelo", back_populates = "rol", cascade = "save-update, merge")