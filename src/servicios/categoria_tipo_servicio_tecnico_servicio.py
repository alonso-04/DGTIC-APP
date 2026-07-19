from typing import List, Optional, Tuple
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from configuraciones.excepciones import ValidacionError, LogicaError, NoEncontradoError
from modelos.categoria_tipo_servicio_tecnico_modelo import CategoriaTipoServicioTecnicoModelo
from repositorios.categoria_tipo_servicio_tecnico_repositorio import CategoriaTipoServicioTecnicoRepositorio


class CategoriaTipoServicioTecnicoServicio:
    def __init__(self, categoria_tipo_servicio_tecnico_repositorio: CategoriaTipoServicioTecnicoRepositorio):
        self._categoria_tipo_servicio_tecnico_repositorio = categoria_tipo_servicio_tecnico_repositorio
    
    def registrar(self, nombre_categoria: str) -> None:
        categoria_tipo_servicio_prestado_limpio = nombre_categoria.strip() if nombre_categoria else ""
        
        if not(categoria_tipo_servicio_prestado_limpio):
            raise ValidacionError(["Categoría de tipo de servicio: No puede estar vacío."])
        
        if (len(categoria_tipo_servicio_prestado_limpio) > 120):
            raise ValidacionError(["Categoría de tipo de servicio: No puede contener más de 120 caracteres."])
        
        try:
            nuevo_categoria_tipo_servicio = CategoriaTipoServicioTecnicoModelo(nombre_categoria = categoria_tipo_servicio_prestado_limpio)
            self._categoria_tipo_servicio_tecnico_repositorio.registrar(nuevo_categoria_tipo_servicio)
        except IntegrityError:
            raise ValidacionError(["Esta categoría de tipo de servicio ya existe."])
        except SQLAlchemyError as error:
            raise LogicaError([f"Error técnico en la base datos al registrar: {str(error)}"])
    
    def obtener_todos(self) -> List[CategoriaTipoServicioTecnicoModelo]:
        return list(self._categoria_tipo_servicio_tecnico_repositorio.obtener_todos())
    
    def obtener_por_id(self, categoria_tipo_servicio_id: int) -> Optional[CategoriaTipoServicioTecnicoModelo]:
        return self._categoria_tipo_servicio_tecnico_repositorio.obtener_por_id(categoria_tipo_servicio_id)
    
    def obtener_por_categoria(self, nombre_categoria: str)-> Optional[CategoriaTipoServicioTecnicoModelo]:
        return self._categoria_tipo_servicio_tecnico_repositorio.obtener_por_categoria(nombre_categoria)
    
    def obtener_por_categoria_o_todos(self, nombre_categoria: str) -> List[Tuple]:
        categoria_tipo_servicio_prestado_limpio = nombre_categoria.strip() if nombre_categoria else ""
        categoria_tipos_servicios = list(self._categoria_tipo_servicio_tecnico_repositorio.obtener_por_categoria_o_todos(categoria_tipo_servicio_prestado_limpio))
        
        if not (categoria_tipos_servicios):
            raise NoEncontradoError(["No hay categorías de tipos de servicio"])
        
        return categoria_tipos_servicios
    
    def actualizar(self, categoria_tipo_servicio_id: int, nuevo_nombre_categoria: str) -> None:
        nuevo_nombre_categoria_limpio = nuevo_nombre_categoria.strip() if nuevo_nombre_categoria else ""
        
        if not(nuevo_nombre_categoria_limpio):
            raise ValidacionError(["Categoría de tipo de servicio: No puede estar vacío."])
        
        if (len(nuevo_nombre_categoria_limpio) > 120):
            raise ValidacionError(["Categoría de tipo de servicio: No puede contener más de 120 caracteres."])
        
        try:
            categoria_tipo_servicio_actualizado = CategoriaTipoServicioTecnicoModelo(
                categoria_tipo_servicio_id = categoria_tipo_servicio_id,
                nombre_categoria = nuevo_nombre_categoria_limpio
            )
            
            self._categoria_tipo_servicio_tecnico_repositorio.actualizar(categoria_tipo_servicio_actualizado)
        except NoEncontradoError as error:
            raise error
        except IntegrityError:
            raise ValidacionError(["Esta categoría de tipo de servicio ya existe."])
        except SQLAlchemyError:
            raise LogicaError([f"Error técnico en la base datos al actualizar: {str(error)}"])
    
    def eliminar(self, categoria_tipo_servicio_id: int) -> None:
        try:
            categoria_tipo_servicio_a_eliminar = CategoriaTipoServicioTecnicoModelo(categoria_tipo_servicio_id = categoria_tipo_servicio_id)
            self._categoria_tipo_servicio_tecnico_repositorio.eliminar(categoria_tipo_servicio_a_eliminar)
        except IntegrityError:
            raise ValidacionError(["Esta categoría de tipo de servicio está asociado a 1 o más tipos de servicio."])
        except NoEncontradoError as error:
            raise error
        except SQLAlchemyError:
            raise LogicaError([f"Error técnico en la base datos al eliminar: {str(error)}"])