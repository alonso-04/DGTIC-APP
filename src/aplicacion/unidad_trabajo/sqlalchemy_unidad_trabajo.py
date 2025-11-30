from infraestructura.conexiones.conexion import bd
from infraestructura.adaptadores.departamento_adaptador import DepartamentoAdaptador
from infraestructura.adaptadores.servicio_adaptador import ServicioAdaptador
from infraestructura.adaptadores.rol_adaptador import RolAdaptador
from infraestructura.adaptadores.usuario_adaptador import UsuarioAdaptador
from infraestructura.adaptadores.tipo_servicio_adaptador import TipoServicioAdaptador
from aplicacion.unidad_trabajo.unidad_trabajo_base import UnidadTrabajo


ADAPTADORES = {
    "departamento": DepartamentoAdaptador,
    "tipo_servicio": TipoServicioAdaptador,
    "servicio": ServicioAdaptador,
    "rol": RolAdaptador,
    "usuario": UsuarioAdaptador
}


class SQLAlchemyUnidadTrabajo(UnidadTrabajo):
    def __init__(self):
        self._session = None
        self._adaptadores = {}
    
    def __enter__(self):
        self._session = bd.crear_sesion()
        return self
    
    def __exit__(self, *args):
        self._session.close()
    
    def commit(self):
        self._session.commit()
    
    def rollback(self):
        self._session.rollback()
    
    def flush(self):
        self._session.flush()
    
    def __getattr__(self, nombre: str):
        if (nombre in ADAPTADORES):
            if (nombre not in self._adaptadores):
                ClaseAdaptador = ADAPTADORES[nombre]
                self._adaptadores[nombre] = ClaseAdaptador(self._session)
            return self._adaptadores[nombre]
        
        raise AttributeError(f"El repositorio '{nombre}' no está definido en la Unidad de Trabajo.")