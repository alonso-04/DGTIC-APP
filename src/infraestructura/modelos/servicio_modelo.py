from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from infraestructura.conexiones.conexion import Base


class ServicioModelo(Base):
    __tablename__ = "tb_servicios"
    
    servicio_id = Column(Integer, primary_key = True, autoincrement = True)
    departamento_id = Column(Integer, ForeignKey("tb_departamentos.departamento_id", ondelete = "RESTRICT", onupdate = "CASCADE"), nullable = False)
    fecha_servicio = Column(Date)
    falla_presenta = Column(String(150), nullable = False)
    tipo_servicio_id = Column(Integer, ForeignKey("tb_tipos_servicio.tipo_servicio_id", ondelete = "RESTRICT", onupdate = "CASCADE"), nullable = False)
    nombres_tecnicos = Column(String(250), nullable = False)
    observaciones_adicionales = Column(String(255), nullable = True)
    
    departamento = relationship("DepartamentoModelo", back_populates = "servicio")
    tipo_servicio = relationship("TipoServicioModelo", back_populates = "servicio")