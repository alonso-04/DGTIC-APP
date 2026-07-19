from typing import List, Optional, Tuple
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from configuraciones.excepciones import ValidacionError, LogicaError, NoEncontradoError
from modelos.departamento_modelo import DepartamentoModelo
from repositorios.departamento_repositorio import DepartamentoRepositorio


class DepartamentoServicio:
    def __init__(self, departamento_repositorio: DepartamentoRepositorio):
        self._departamento_repositorio = departamento_repositorio
    
    def registrar(self, nombre_departamento: str) -> None:
        nombre_departamento_limpio = nombre_departamento.strip() if nombre_departamento else ""
        
        if not(nombre_departamento_limpio):
            raise ValidacionError(["Nombre del Departamento: No puede estar vacío."])
        
        if (len(nombre_departamento_limpio) > 120):
            raise ValidacionError(["Nombre del Departamento: No puede contener más de 120 caracteres."])
        
        try:
            nuevo_departamento = DepartamentoModelo(nombre_departamento = nombre_departamento_limpio)
            self._departamento_repositorio.registrar(nuevo_departamento)
        except IntegrityError:
            raise ValidacionError(["Este departamento ya existe."])
        except SQLAlchemyError as error:
            raise LogicaError([f"Error técnico en la base datos al registrar: {str(error)}"])
    
    def obtener_todos(self) -> List[DepartamentoModelo]:
        return list(self._departamento_repositorio.obtener_todos())
    
    def obtener_por_id(self, departamento_id: int) -> Optional[DepartamentoModelo]:
        return self._departamento_repositorio.obtener_por_id(departamento_id)
    
    def obtener_por_nombre(self, nombre_departamento: str) -> Optional[DepartamentoModelo]:
        return self._departamento_repositorio.obtener_por_nombre(nombre_departamento)
    
    def obtener_por_nombre_o_todos(self, nombre_departamento: str) -> List[Tuple]:
        nombre_departamento_limpio = nombre_departamento.strip() if nombre_departamento else ""
        departamentos = list(self._departamento_repositorio.obtener_por_nombre_o_todos(nombre_departamento_limpio))
        
        if not(departamentos):
            raise NoEncontradoError(["No hay departamentos"])
        
        return departamentos
    
    def actualizar(self, departamento_id: int, nuevo_nombre_departamento: str) -> None:
        nuevo_nombre_departamento_limpio = nuevo_nombre_departamento.strip() if nuevo_nombre_departamento else ""
            
        if not(nuevo_nombre_departamento_limpio):
            raise ValidacionError(["Nombre del Departamento: No puede estar vacío."])
            
        if (len(nuevo_nombre_departamento_limpio) > 120):
            raise ValidacionError(["Nombre del Departamento: No puede contener más de 120 caracteres."])
            
        try:
            departamento_actualizado = DepartamentoModelo(
                departamento_id = departamento_id,
                nombre_departamento = nuevo_nombre_departamento_limpio
            )
                
            self._departamento_repositorio.actualizar(departamento_actualizado)
        except NoEncontradoError as error:
            raise error
        except IntegrityError:
            raise ValidacionError(["Este departamento ya existe"])
        except SQLAlchemyError as error:
            raise LogicaError([f"Error técnico en la base de datos al actualizar: {str(error)}"])
    
    def eliminar(self, departamento_id: int) -> None:
        try:
            departamento_a_eliminar = DepartamentoModelo(departamento_id = departamento_id)
            self._departamento_repositorio.eliminar(departamento_a_eliminar)
        except IntegrityError:
            raise ValidacionError(["Este departamento está asociado a 1 o más servicios."])
        except NoEncontradoError as error:
            raise error
        except SQLAlchemyError as error:
            raise LogicaError([F"Error técnico en la base de datos al eliminar: {str(error)}"])