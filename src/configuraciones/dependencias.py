from typing import Dict

from configuraciones.conexion import bd
import repositorios as repo
import servicios as serv


class ContenedorDependencias:
    def __init__(self):
        self._bd = bd
        self._instancias = {}
    
    def _crear_si_falta(self, nombre, fabrica):
        if nombre not in self._instancias:
            self._instancias[nombre] = fabrica()
        return self._instancias[nombre]
    
    def obtener_servicios(self) -> Dict:
        departamento_repositorio = self._crear_si_falta("departamento_repositorio", lambda: repo.DepartamentoRepositorio(self._bd))
        rol_repositorio = self._crear_si_falta("rol_repositorio", lambda: repo.RolRepositorio(self._bd))
        servicio_tecnico_repositorio = self._crear_si_falta("servicio_tecnico_repositorio", lambda: repo.ServicioTecnicoRepositorio(self._bd))
        categoria_tipo_servicio_repositorio = self._crear_si_falta("categoria_tipo_servicio_repositorio", lambda: repo.CategoriaTipoServicioTecnicoRepositorio(self._bd))
        tipo_servicio_repositorio = self._crear_si_falta("tipo_servicio_repositorio", lambda: repo.TipoServicioTecnicoRepositorio(self._bd))
        comuna_repositorio = self._crear_si_falta("comuna_repositorio", lambda: repo.ComunaRepositorio(self._bd))
        usuario_repositorio = self._crear_si_falta("usuario_repositorio", lambda: repo.UsuarioRepositorio(self._bd))
        
        return {
            "departamento_servicio": self._crear_si_falta("departamento_servicio", lambda: serv.DepartamentoServicio(departamento_repositorio)),
            "rol_servicio": self._crear_si_falta("rol_servicio", lambda: serv.RolServicio(rol_repositorio)),
            "servicio_tecnico_servicio": self._crear_si_falta(
                "servicio_tecnico_servicio", 
                lambda: serv.ServicioTecnicoServicio(
                    servicio_tecnico_repositorio, 
                    departamento_repositorio, 
                    tipo_servicio_repositorio, 
                    comuna_repositorio
                )),
            "tipo_servicio_tecnico_servicio": self._crear_si_falta(
                "tipo_servicio_tecnico_servicio", 
                lambda: serv.TipoServicioTecnicoServicio(tipo_servicio_repositorio, categoria_tipo_servicio_repositorio)),
            "comuna_servicio": self._crear_si_falta("comuna_servicio", lambda: serv.ComunaServicio(comuna_repositorio)),
            "categoria_tipo_servicio_tecnico_servicio": self._crear_si_falta(
                "categoria_tipo_servicio_tecnico_servicio", 
                lambda: serv.CategoriaTipoServicioTecnicoServicio(categoria_tipo_servicio_repositorio)),
            "usuario_servicio": self._crear_si_falta("usuario_servicio", lambda: serv.UsuarioServicio(usuario_repositorio, rol_repositorio))
        }

contenedor_dependencias = ContenedorDependencias()

if __name__ == "__main__":
    servicios = contenedor_dependencias.obtener_servicios()
    
    todos_departamentos = servicios["departamento_servicio"].obtener_todos()
    for departamento in todos_departamentos:
        print(f"ID: {departamento.departamento_id} | NOMBRE: {departamento.nombre_departamento}")