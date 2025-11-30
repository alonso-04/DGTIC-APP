from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from infraestructura.conexiones.conexion import Base


class UsuarioModelo(Base):
    __tablename__ = "tb_usuarios"
    
    usuario_id = Column(Integer, primary_key = True, autoincrement = True)
    rol_id = Column(Integer, ForeignKey("tb_roles.rol_id", ondelete = "RESTRICT", onupdate = "CASCADE"), nullable = False)
    nombre_usuario = Column(String(12), unique = True, nullable = False)
    clave_usuario = Column(String(12), nullable = False)
    
    rol = relationship("RolModelo", back_populates = "usuario")