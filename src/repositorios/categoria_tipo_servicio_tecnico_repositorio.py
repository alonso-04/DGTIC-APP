from typing import Optional, Generator, Tuple
from sqlalchemy import text

from configuraciones.excepciones import NoEncontradoError
from modelos.categoria_tipo_servicio_tecnico_modelo import CategoriaTipoServicioTecnicoModelo


class CategoriaTipoServicioTecnicoRepositorio:
    def __init__(self, bd):
        self._bd = bd
    
    def registrar(self, nombre_categoria: CategoriaTipoServicioTecnicoModelo) -> None:
        with self._bd.sesion() as sesion:
            sesion.add(nombre_categoria)
    
    def obtener_todos(self) -> Generator[CategoriaTipoServicioTecnicoModelo, None, None]:
        with self._bd.sesion() as sesion:
            categorias_tipo_servicio_modelo = sesion.query(CategoriaTipoServicioTecnicoModelo).yield_per(100)
            
            for categoria_tipo_servicio in categorias_tipo_servicio_modelo:
                yield categoria_tipo_servicio
    
    def obtener_por_id(self, categoria_tipo_servicio_id: int) -> Optional[CategoriaTipoServicioTecnicoModelo]:
        with self._bd.sesion() as sesion:
            categoria_tipo_servicio_modelo = sesion.query(CategoriaTipoServicioTecnicoModelo).filter_by(categoria_tipo_servicio_id = categoria_tipo_servicio_id).first()
            
            if not(categoria_tipo_servicio_modelo):
                raise NoEncontradoError(["Esta categoría de tipo de servicio no existe"])
            
            return categoria_tipo_servicio_modelo
    
    def obtener_por_categoria(self, nombre_categoria: str) -> Optional[CategoriaTipoServicioTecnicoModelo]:
        with self._bd.sesion() as sesion:
            categoria_tipo_servicio_modelo = sesion.query(CategoriaTipoServicioTecnicoModelo).filter_by(nombre_categoria = nombre_categoria).first()
            
            if not(categoria_tipo_servicio_modelo):
                raise NoEncontradoError(["Esta categoría de tipo de servicio no existe"])
            
            return categoria_tipo_servicio_modelo
    
    def obtener_por_categoria_o_todos(self, nombre_categoria: Optional[str]) -> Generator[Tuple, None, None]:
        with self._bd.sesion() as sesion:
            consulta = """
                SELECT
                    categoria_tipo_servicio_id,
                    nombre_categoria
                FROM tb_categorias_tipo_servicio
            """
            
            parametros = {}
            condiciones_adicionales = []
            
            if (nombre_categoria):
                condiciones_adicionales.append("nombre_categoria = :nombre_categoria")
                parametros["nombre_categoria"] = nombre_categoria
            
            if (condiciones_adicionales):
                consulta += f"WHERE {condiciones_adicionales[0]}"
            
            categorias_tipo_servicio_modelo = sesion.execute(text(consulta), parametros).yield_per(100)
            for categoria_tipo_servicio in categorias_tipo_servicio_modelo:
                yield categoria_tipo_servicio
    
    def actualizar(self, categoria_tipo_servicio: CategoriaTipoServicioTecnicoModelo) -> None:
        with self._bd.sesion() as sesion:
            categoria_tipo_servicio_modelo = sesion.query(CategoriaTipoServicioTecnicoModelo).filter_by(categoria_tipo_servicio_id = categoria_tipo_servicio.categoria_tipo_servicio_id).first()
            categoria_tipo_servicio_modelo.categoria_tipo_servicio_id = categoria_tipo_servicio.categoria_tipo_servicio_id
            categoria_tipo_servicio_modelo.nombre_categoria = categoria_tipo_servicio.nombre_categoria
    
    def eliminar(self, categoria_tipo_servicio: CategoriaTipoServicioTecnicoModelo) -> None:
        with self._bd.sesion() as sesion:
            categoria_tipo_servicio_modelo = sesion.query(CategoriaTipoServicioTecnicoModelo).filter_by(categoria_tipo_servicio_id = categoria_tipo_servicio.categoria_tipo_servicio_id).first()
            sesion.delete(categoria_tipo_servicio_modelo)