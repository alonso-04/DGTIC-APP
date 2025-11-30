from dominio.entidades.tipo_servicio import TipoServicio
from dominio.excepciones import TipoServicioValidacionError
from aplicacion.unidad_trabajo.unidad_trabajo_base import UnidadTrabajo
from aplicacion.unidad_trabajo.sqlalchemy_unidad_trabajo import SQLAlchemyUnidadTrabajo
from typing import Optional, Generator


class ListarTiposServicio:
    def __init__(self, unidad_trabajo = UnidadTrabajo):
        self.unidad_trabajo = unidad_trabajo
    
    def obtener_todos(self) -> Generator[TipoServicio, None, None]:
        with self.unidad_trabajo() as unidad_trabajo:
            tipos_servicio = unidad_trabajo.tipo_servicio.obtener_todos()
            return tipos_servicio
    
    def obtener_por_id(self, tipo_servicio_id: int) -> Optional[TipoServicio]:
        with self.unidad_trabajo() as unidad_trabajo:
            try:
                errores = []
                
                tipo_servicio = unidad_trabajo.tipo_servicio.obtener_por_id(tipo_servicio_id)
                
                if not(tipo_servicio):
                    errores.append("Este tipo de servicio no existe.")
                
                if (errores):
                    raise TipoServicioValidacionError(errores)
                
                return tipo_servicio
            except TipoServicioValidacionError as error:
                raise error
    
    def obtener_por_tipo_servicio(self, tipo_servicio_prestado: str) -> Optional[TipoServicio]:
        with self.unidad_trabajo() as unidad_trabajo:
            try:
                errores = []
                
                tipo_servicio = unidad_trabajo.tipo_servicio.obtener_por_tipo_servicio(tipo_servicio_prestado)
                
                if not(tipo_servicio):
                    errores.append("Este tipo de servicio no existe.")
                
                if (errores):
                    raise TipoServicioValidacionError(errores)
                
                return tipo_servicio
            except TipoServicioValidacionError as error:
                raise error


if __name__ == "__main__":
    try:
        unidad_trabajo = SQLAlchemyUnidadTrabajo
        listar_tipos_servicio = ListarTiposServicio(unidad_trabajo)
        
        """for tipo_servicio in listar_tipos_servicio.obtener_todos():
            print(tipo_servicio.tipo_servicio_prestado)"""
        
        tipo_servicio = listar_tipos_servicio.obtener_por_id(2)
        print(tipo_servicio.tipo_servicio_prestado)
        
        tipo_servicio = listar_tipos_servicio.obtener_por_tipo_servicio("CONFIGURACIÓN DE IMPRESORA")
        print(tipo_servicio.tipo_servicio_id)
    except TipoServicioValidacionError as error:
        print("\n".join(error.errores))
    except Exception as error:
        print(error)