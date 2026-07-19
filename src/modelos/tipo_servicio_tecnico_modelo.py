from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from configuraciones.conexion  import Base


class TipoServicioTecnicoModelo(Base):
    __tablename__ = "tb_tipos_servicio"
    
    tipo_servicio_id = Column(Integer, primary_key = True, autoincrement = True)
    categoria_tipo_servicio_id = Column(Integer, ForeignKey("tb_categorias_tipo_servicio.categoria_tipo_servicio_id", ondelete = "RESTRICT", onupdate = "CASCADE"), nullable = False)
    tipo_servicio_prestado = Column(String(120), unique = True, nullable = False)
    
    servicio = relationship("ServicioTecnicoModelo", back_populates = "tipo_servicio")
    categoria_tipo_servicio = relationship("CategoriaTipoServicioTecnicoModelo", back_populates = "tipo_servicio")