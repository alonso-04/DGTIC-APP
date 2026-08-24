from typing import Optional, Generator, Tuple
from sqlalchemy import text

from configuraciones.excepciones import NoEncontradoError
from modelos.comuna_modelo import ComunaModelo


class ComunaRepositorio:
    def __init__(self, bd):
        self._bd = bd
    
    def registrar(self, comuna: ComunaModelo) -> None:
        with self._bd.sesion() as sesion:
            sesion.add(comuna)
    
    def obtener_todos(self) -> Generator[ComunaModelo, None, None]:
        with self._bd.sesion() as sesion:
            comunas_modelo = sesion.query(ComunaModelo).yield_per(100)
            
            for comuna in comunas_modelo:
                yield comuna
    
    def obtener_por_id(self, comuna_id: int) -> Optional[ComunaModelo]:
        with self._bd.sesion() as sesion:
            comuna_modelo = sesion.query(ComunaModelo).filter_by(comuna_id = comuna_id).first()
            
            if not(comuna_modelo):
                raise NoEncontradoError(["Esta comuna no existe"])
            
            return comuna_modelo
    
    def obtener_por_comuna(self, nombre_comuna: str) -> Optional[ComunaModelo]:
        with self._bd.sesion() as sesion:
            comuna_modelo = sesion.query(ComunaModelo).filter_by(nombre_comuna = nombre_comuna).first()
            
            if not(comuna_modelo):
                raise NoEncontradoError(["Esta comuna no existe"])
            
            return comuna_modelo
    
    def obtener_por_comuna_o_todos(self, nombre_comuna: Optional[str]) -> Generator[Tuple, None, None]:
        with self._bd.sesion() as sesion:
            consulta = """
                SELECT
                    comuna_id,
                    nombre_comuna
                FROM tb_comunas
            """
            
            parametros = {}
            condiciones_adicionales = []
            
            if (nombre_comuna):
                condiciones_adicionales.append("nombre_comuna = :nombre_comuna")
                parametros["nombre_comuna"] = nombre_comuna
            
            if (condiciones_adicionales):
                consulta += "WHERE " + " AND ".join(condiciones_adicionales)
            
            comunas_modelo = sesion.execute(text(consulta), parametros).yield_per(100)
            for comuna in comunas_modelo:
                yield comuna
    
    def actualizar(self, comuna: ComunaModelo) -> None:
        with self._bd.sesion() as sesion:
            comuna_modelo = sesion.query(ComunaModelo).filter_by(comuna_id = comuna.comuna_id).first()
            comuna_modelo.nombre_comuna = comuna.nombre_comuna
    
    def eliminar(self, comuna: ComunaModelo) -> None:
        with self._bd.sesion() as sesion:
            comuna_modelo = sesion.query(ComunaModelo).filter_by(comuna_id = comuna.comuna_id).first()
            sesion.delete(comuna_modelo)