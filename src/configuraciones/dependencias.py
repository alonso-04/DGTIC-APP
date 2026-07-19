from typing import Dict

from configuraciones.conexion import bd

from repositorios.departamento_repositorio import DepartamentoRepositorio
from repositorios.rol_repositorio import RolRepositorio
from repositorios.servicio_tecnico_repositorio import ServicioTecnicoRepositorio
from repositorios.tipo_servicio_tecnico_repositorio import TipoServicioTecnicoRepositorio
from repositorios.categoria_tipo_servicio_tecnico_repositorio import CategoriaTipoServicioTecnicoRepositorio
from repositorios.usuario_repositorio import UsuarioRepositorio

from servicios.departamento_servicio import DepartamentoServicio
from servicios.rol_servicio import RolServicio
from servicios.servicio_tecnico_servicio import ServicioTecnicoServicio
from servicios.tipo_servicio_tecnico_servicio import TipoServicioTecnicoServicio
from servicios.categoria_tipo_servicio_tecnico_servicio import CategoriaTipoServicioTecnicoServicio
from servicios.usuario_servicio import UsuarioServicio


class ContenedorDependencias:
    def __init__(self):
        self._bd = bd
        
        self._departamento_repositorio = DepartamentoRepositorio(self._bd)
        self._rol_repositorio = RolRepositorio(self._bd)
        self._servicio_tecnico_repositorio = ServicioTecnicoRepositorio(self._bd)
        self._categoria_tipo_servicio_tecnico_repositorio = CategoriaTipoServicioTecnicoRepositorio(self._bd)
        self._tipo_servicio_tecnico_repositorio = TipoServicioTecnicoRepositorio(self._bd)
        self._usuario_repositorio = UsuarioRepositorio(self._bd)
        
        self._departamento_servicio = DepartamentoServicio(self._departamento_repositorio)
        self._rol_servicio = RolServicio(self._rol_repositorio)
        
        self._servicio_tecnico_servicio = ServicioTecnicoServicio(
            self._servicio_tecnico_repositorio, 
            self._departamento_repositorio, 
            self._tipo_servicio_tecnico_repositorio
        )
        
        self._tipo_servicio_tecnico_servicio = TipoServicioTecnicoServicio(
            self._tipo_servicio_tecnico_repositorio, 
            self._categoria_tipo_servicio_tecnico_repositorio
        )
        
        self._categoria_tipo_servicio_tecnico_servicio = CategoriaTipoServicioTecnicoServicio(self._categoria_tipo_servicio_tecnico_repositorio)
        
        self._usuario_servicio = UsuarioServicio(self._usuario_repositorio, self._rol_repositorio)
    
    def obtener_servicios(self) -> Dict:
        return {
            "departamento_servicio": self._departamento_servicio,
            "rol_servicio": self._rol_servicio,
            "servicio_tecnico_servicio": self._servicio_tecnico_servicio,
            "tipo_servicio_tecnico_servicio": self._tipo_servicio_tecnico_servicio,
            "categoria_tipo_servicio_tecnico_servicio": self._categoria_tipo_servicio_tecnico_servicio,
            "usuario_servicio": self._usuario_servicio
        }

contenedor_dependencias = ContenedorDependencias()

if __name__ == "__main__":
    servicios = contenedor_dependencias.obtener_servicios()
    
    todos_departamentos = servicios["departamento_servicio"].obtener_todos()
    for departamento in todos_departamentos:
        print(f"ID: {departamento.departamento_id} | NOMBRE: {departamento.nombre_departamento}")