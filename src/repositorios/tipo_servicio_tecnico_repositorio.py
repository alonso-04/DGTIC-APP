from typing import Optional, Generator, Tuple
from sqlalchemy import text

from configuraciones.excepciones import NoEncontradoError
from modelos.tipo_servicio_tecnico_modelo import TipoServicioTecnicoModelo


class TipoServicioTecnicoRepositorio:
    def __init__(self, bd):
        self._bd = bd
    
    def registrar(self, tipo_servicio: TipoServicioTecnicoModelo) -> None:
        with self._bd.sesion() as sesion:
            sesion.add(tipo_servicio)
    
    def obtener_todos(self) -> Generator[TipoServicioTecnicoModelo, None, None]:
        with self._bd.sesion() as sesion:
            tipos_servicio_modelo = sesion.query(TipoServicioTecnicoModelo).yield_per(100)
            
            for tipo_servicio in tipos_servicio_modelo:
                yield tipo_servicio
    
    def obtener_por_id(self, tipo_servicio_id: int) -> Optional[TipoServicioTecnicoModelo]:
        with self._bd.sesion() as sesion:
            tipo_servicio_modelo = sesion.query(TipoServicioTecnicoModelo).filter_by(tipo_servicio_id = tipo_servicio_id).first()
            
            if not(tipo_servicio_modelo):
                raise NoEncontradoError(["Este tipo de servicio no existe"])
            
            return tipo_servicio_modelo
    
    def obtener_por_tipo_servicio(self, tipo_servicio_prestado: str) -> Optional[TipoServicioTecnicoModelo]:
        with self._bd.sesion() as sesion:
            tipo_servicio_modelo = sesion.query(TipoServicioTecnicoModelo).filter_by(tipo_servicio_prestado = tipo_servicio_prestado).first()
            
            if not(tipo_servicio_modelo):
                raise NoEncontradoError(["Este tipo de servicio no existe"])
            
            return tipo_servicio_modelo
    
    def obtener_por_tipo_categoria_o_todos(self, tipo_servicio_prestado: Optional[str], nombre_categoria: Optional[str]) -> Generator[Tuple, None, None]:
        with self._bd.sesion() as sesion:
            consulta = """
                SELECT
                    tipos_servicio.tipo_servicio_id,
                    tipos_servicio.tipo_servicio_prestado,
                    categorias_tipo_servicio.nombre_categoria
                FROM tb_tipos_servicio tipos_servicio
                INNER JOIN tb_categorias_tipo_servicio categorias_tipo_servicio ON tipos_servicio.categoria_tipo_servicio_id = categorias_tipo_servicio.categoria_tipo_servicio_id
            """
            
            parametros = {}
            condiciones_adicionales = []
            
            if (tipo_servicio_prestado):
                condiciones_adicionales.append("tipos_servicio.tipo_servicio_prestado = :tipo_servicio_prestado")
                parametros["tipo_servicio_prestado"] = tipo_servicio_prestado
            
            if (nombre_categoria):
                condiciones_adicionales.append("categorias_tipo_servicio.nombre_categoria = :nombre_categoria")
                parametros["nombre_categoria"] = nombre_categoria
            
            if (condiciones_adicionales):
                consulta += "WHERE " + " AND ".join(condiciones_adicionales)
            
            tipos_servicios_modelo = sesion.execute(text(consulta), parametros).yield_per(100)
            for tipo_servicio in tipos_servicios_modelo:
                yield tipo_servicio
    
    def actualizar(self, tipo_servicio: TipoServicioTecnicoModelo) -> None:
        with self._bd.sesion() as sesion:
            tipo_servicio_modelo = sesion.query(TipoServicioTecnicoModelo).filter_by(tipo_servicio_id = tipo_servicio.tipo_servicio_id).first()
            tipo_servicio_modelo.categoria_tipo_servicio_id = tipo_servicio.categoria_tipo_servicio_id
            tipo_servicio_modelo.tipo_servicio_prestado = tipo_servicio.tipo_servicio_prestado
    
    def eliminar(self, tipo_servicio: TipoServicioTecnicoModelo) -> None:
        with self._bd.sesion() as sesion:
            tipo_servicio_modelo = sesion.query(TipoServicioTecnicoModelo).filter_by(tipo_servicio_id = tipo_servicio.tipo_servicio_id).first()
            sesion.delete(tipo_servicio_modelo)