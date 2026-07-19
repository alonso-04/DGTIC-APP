from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from configuraciones.conexion  import Base


class CategoriaTipoServicioTecnicoModelo(Base):
    __tablename__ = "tb_categorias_tipo_servicio"
    
    categoria_tipo_servicio_id = Column(Integer, primary_key = True, autoincrement = True)
    nombre_categoria = Column(String(120), unique = True, nullable = False)
    
    tipo_servicio = relationship("TipoServicioTecnicoModelo", back_populates = "categoria_tipo_servicio")