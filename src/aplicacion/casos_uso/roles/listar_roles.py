from dominio.entidades.rol import Rol
from dominio.excepciones import RolValidacionError
from aplicacion.unidad_trabajo.unidad_trabajo_base import UnidadTrabajo
from aplicacion.unidad_trabajo.sqlalchemy_unidad_trabajo import SQLAlchemyUnidadTrabajo
from typing import Optional, Generator


class ListarRoles:
    def __init__(self, unidad_trabajo: UnidadTrabajo):
        self.unidad_trabajo = unidad_trabajo
    
    def obtener_todos(self) -> Generator[Rol, None, None]:
        with self.unidad_trabajo() as unidad_trabajo:
            roles = unidad_trabajo.rol.obtener_todos()
            return roles
    
    def obtener_por_id(self, rol_id: int) -> Optional[Rol]:
        with self.unidad_trabajo() as unidad_trabajo:
            try:
                errores = []
                
                rol = unidad_trabajo.rol.obtener_por_id(rol_id)
                
                if not(rol):
                    errores.append("Este rol no existe.")
                
                if (errores):
                    raise RolValidacionError(errores)
                
                return rol
            except RolValidacionError as error:
                raise error
    
    def obtener_por_tipo_rol(self, tipo_rol: str) -> Optional[Rol]:
        with self.unidad_trabajo() as unidad_trabajo:
            try:
                errores = []
                
                rol = unidad_trabajo.rol.obtener_por_tipo_rol(tipo_rol)
                
                if not(rol):
                    errores.append("Este rol no existe.")
                
                if (errores):
                    raise RolValidacionError(errores)
                
                return rol
            except RolValidacionError as error:
                raise error


if __name__ == "__main__":
    try:
        unidad_trabajo = SQLAlchemyUnidadTrabajo()
        listar_roles = ListarRoles(unidad_trabajo)
        
        roles = listar_roles.obtener_todos()
        
        """for rol in roles:
            print(f"-ID ROL: {rol.rol_id}\n-TIPO DE ROL: {rol.tipo_rol} \n")"""
        
        rol = listar_roles.obtener_por_id(3)
        print(rol.tipo_rol)
    except RolValidacionError as error:
        print("\n".join(error.errores))
    except Exception as error:
        print(error)