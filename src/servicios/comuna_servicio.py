from typing import List, Optional, Tuple
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from configuraciones.excepciones import ValidacionError, LogicaError, NoEncontradoError
from modelos.comuna_modelo import ComunaModelo
from repositorios.comuna_repositorio import ComunaRepositorio


class ComunaServicio:
    def __init__(self, comuna_repositorio: ComunaRepositorio):
        self._comuna_repositorio = comuna_repositorio
    
    def registrar(self, nombre_comuna: str) -> None:
        nombre_comuna_limpio = nombre_comuna.strip() if nombre_comuna else ""
            
        if not(nombre_comuna_limpio):
            raise ValidacionError(["Nombre de la comuna: No puede estar vacío."])
            
        if (len(nombre_comuna_limpio) > 100):
            raise ValidacionError(["Nombre de la comuna: No puede contener más de 100 caracteres."])
            
        try:
            nuevo_comuna = ComunaModelo(nombre_comuna = nombre_comuna_limpio)
            self._comuna_repositorio.registrar(nuevo_comuna)
        except IntegrityError:
            raise ValidacionError(["Esta comuna ya existe."])
        except SQLAlchemyError as error:
            raise LogicaError([f"Error técnico en la base datos al registrar: {str(error)}"])
        
    def obtener_todos(self) -> List[ComunaModelo]:
        return list(self._comuna_repositorio.obtener_todos())
        
    def obtener_por_id(self, comuna_id: int) -> Optional[ComunaModelo]:
        return self._comuna_repositorio.obtener_por_id(comuna_id)
        
    def obtener_por_comuna(self, nombre_comuna: str)-> Optional[ComunaModelo]:
        return self._comuna_repositorio.obtener_por_comuna(nombre_comuna)
        
    def obtener_por_comuna_o_todos(self, nombre_comuna: str) -> List[Tuple]:
        nombre_comuna_limpio = nombre_comuna.strip() if nombre_comuna else ""
        comunas = list(self._comuna_repositorio.obtener_por_comuna_o_todos(nombre_comuna_limpio))
            
        if not (comunas):
            raise NoEncontradoError(["No hay comunas registradas."])
            
        return comunas
        
    def actualizar(self, comuna_id: int, nuevo_nombre_comuna: str) -> None:
        nuevo_nombre_comuna_limpio = nuevo_nombre_comuna.strip() if nuevo_nombre_comuna else ""
            
        if not(nuevo_nombre_comuna_limpio):
            raise ValidacionError(["Nombre de la comuna: No puede estar vacío."])
            
        if (len(nuevo_nombre_comuna_limpio) > 100):
            raise ValidacionError(["Nombre de la comuna: No puede contener más de 100 caracteres."])
            
        try:
            comuna_actualizado = ComunaModelo(
                comuna_id = comuna_id,
                nombre_comuna = nuevo_nombre_comuna_limpio
            )
            
            self._comuna_repositorio.actualizar(comuna_actualizado)
        except NoEncontradoError as error:
            raise error
        except IntegrityError:
            raise ValidacionError(["Esta comuna ya existe."])
        except SQLAlchemyError:
            raise LogicaError([f"Error técnico en la base datos al actualizar: {str(error)}"])
        
    def eliminar(self, comuna_id: int) -> None:
        try:
            comuna_a_eliminar = ComunaModelo(comuna_id = comuna_id)
            self._comuna_repositorio.eliminar(comuna_a_eliminar)
        except IntegrityError:
            raise ValidacionError(["Esta comuna está asociado a 1 o más servicios."])
        except NoEncontradoError as error:
            raise error
        except SQLAlchemyError:
            raise LogicaError([f"Error técnico en la base datos al eliminar: {str(error)}"])