from typing import List, Optional, Tuple
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from configuraciones.excepciones import ValidacionError, LogicaError, NoEncontradoError
from modelos.tipo_servicio_tecnico_modelo import TipoServicioTecnicoModelo
from repositorios.tipo_servicio_tecnico_repositorio import TipoServicioTecnicoRepositorio
from repositorios.categoria_tipo_servicio_tecnico_repositorio import CategoriaTipoServicioTecnicoRepositorio


class TipoServicioTecnicoServicio:
    def __init__(
        self, 
        tipo_servicio_tecnico_repositorio: TipoServicioTecnicoRepositorio, 
        categoria_tipo_servicio_tecnico_repositorio: CategoriaTipoServicioTecnicoRepositorio
    ):
        self._tipo_servicio_tecnico_repositorio = tipo_servicio_tecnico_repositorio
        self._categoria_tipo_servicio_tecnico_repositorio = categoria_tipo_servicio_tecnico_repositorio
    
    def registrar(self, nombre_categoria: str, tipo_servicio_prestado: str) -> None:
        errores = []
        nombre_categoria_limpio = nombre_categoria.strip() if nombre_categoria else ""
        tipo_servicio_prestado_limpio = tipo_servicio_prestado.strip() if tipo_servicio_prestado else ""
        
        # Validando la categoria de tipo de servicio
        if not(nombre_categoria_limpio):
            errores.append("Categoría de tipo de servicio: Debe elegir una categoría.")
        
        # Validando el tipo de servicio prestado
        if not(tipo_servicio_prestado_limpio):
            errores.append("Tipo de servicio: No puede estar vacío.")
        
        if (len(tipo_servicio_prestado_limpio) > 120):
            errores.append("Tipo de servicio: No puede contener más de 120 caracteres.")
        
        if (errores):
            raise ValidacionError(errores)
        
        categoria_tipo_servicio = self._categoria_tipo_servicio_tecnico_repositorio.obtener_por_categoria(nombre_categoria_limpio)
        try:
            nuevo_tipo_servicio = TipoServicioTecnicoModelo(
                categoria_tipo_servicio_id = categoria_tipo_servicio.categoria_tipo_servicio_id,
                tipo_servicio_prestado = tipo_servicio_prestado
            )
            self._tipo_servicio_tecnico_repositorio.registrar(nuevo_tipo_servicio)
        except NoEncontradoError as error:
            raise error
        except IntegrityError:
            raise ValidacionError(["Este tipo de servicio ya existe."])
        except SQLAlchemyError as error:
            raise LogicaError([f"Error técnico en la base datos al registrar: {str(error)}"])
    
    def obtener_todos(self) -> List[TipoServicioTecnicoModelo]:
        return list(self._tipo_servicio_tecnico_repositorio.obtener_todos())
    
    def obtener_por_id(self, tipo_servicio_id: int) -> Optional[TipoServicioTecnicoModelo]:
        return self._tipo_servicio_tecnico_repositorio.obtener_por_id(tipo_servicio_id)
    
    def obtener_por_tipo_servicio(self, tipo_servicio_prestado: str)-> Optional[TipoServicioTecnicoModelo]:
        return self._tipo_servicio_tecnico_repositorio.obtener_por_tipo_servicio(tipo_servicio_prestado)
    
    def obtener_por_tipo_categoria_o_todos(self, tipo_servicio_prestado: str, nombre_categoria: str) -> List[Tuple]:
        tipo_servicio_prestado_limpio = tipo_servicio_prestado.strip() if tipo_servicio_prestado else ""
        nombre_categoria_limpio = nombre_categoria.strip() if nombre_categoria else ""
        tipos_servicios = list(self._tipo_servicio_tecnico_repositorio.obtener_por_tipo_categoria_o_todos(tipo_servicio_prestado_limpio, nombre_categoria_limpio))
        
        if not (tipos_servicios):
            raise NoEncontradoError(["No hay tipos de servicio"])
        
        return tipos_servicios
    
    def actualizar(self, tipo_servicio_id: int, nuevo_categoria: str, nuevo_nombre_tipo_servicio: str) -> None:
        errores = []
        nuevo_categoria_limpio = nuevo_categoria.strip() if nuevo_categoria else ""
        nuevo_nombre_tipo_servicio_limpio = nuevo_nombre_tipo_servicio.strip() if nuevo_nombre_tipo_servicio else ""
        
        if not(nuevo_categoria_limpio):
            errores.append("Categoría de tipo de servicio: Debe elegir una categoría.")
        
        if not(nuevo_nombre_tipo_servicio_limpio):
            errores.append("Tipo de servicio: No puede estar vacío.")
        
        if (len(nuevo_nombre_tipo_servicio_limpio) > 120):
            errores.append("Tipo de servicio: No puede contener más de 120 caracteres.")
        
        if (errores):
            raise ValidacionError(errores)
        
        categoria_tipo_servicio = self._categoria_tipo_servicio_tecnico_repositorio.obtener_por_categoria(nuevo_categoria_limpio)
        try:
            tipo_servicio_actualizado = TipoServicioTecnicoModelo(
                tipo_servicio_id = tipo_servicio_id,
                categoria_tipo_servicio_id = categoria_tipo_servicio.categoria_tipo_servicio_id,
                tipo_servicio_prestado = nuevo_nombre_tipo_servicio_limpio
            )
            
            self._tipo_servicio_tecnico_repositorio.actualizar(tipo_servicio_actualizado)
        except NoEncontradoError as error:
            raise error
        except IntegrityError:
            raise ValidacionError(["Este tipo de servicio ya existe."])
        except SQLAlchemyError:
            raise LogicaError([f"Error técnico en la base datos al actualizar: {str(error)}"])
    
    def eliminar(self, tipo_servicio_id: int) -> None:
        try:
            tipo_servicio_a_eliminar = TipoServicioTecnicoModelo(tipo_servicio_id = tipo_servicio_id)
            self._tipo_servicio_tecnico_repositorio.eliminar(tipo_servicio_a_eliminar)
        except IntegrityError:
            raise ValidacionError(["Este tipo de servicio está asociado a 1 o más servicios."])
        except NoEncontradoError as error:
            raise error
        except SQLAlchemyError:
            raise LogicaError([f"Error técnico en la base datos al eliminar: {str(error)}"])