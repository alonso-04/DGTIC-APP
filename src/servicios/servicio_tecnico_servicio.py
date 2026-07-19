from typing import List, Optional, Tuple, Dict
from datetime import date
from sqlalchemy.exc import SQLAlchemyError

from configuraciones.excepciones import ValidacionError, LogicaError, NoEncontradoError
from modelos.servicio_tecnico_modelo import ServicioTecnicoModelo
from repositorios.servicio_tecnico_repositorio import ServicioTecnicoRepositorio
from repositorios.departamento_repositorio import DepartamentoRepositorio
from repositorios.tipo_servicio_tecnico_repositorio import TipoServicioTecnicoRepositorio


class ServicioTecnicoServicio:
    def __init__(
        self, 
        servicio_tecnico_repositorio: ServicioTecnicoRepositorio, 
        departamento_repositorio: DepartamentoRepositorio,
        tipo_servicio_tecnico_repositorio: TipoServicioTecnicoRepositorio
    ):
        self._servicio_tecnico_repositorio = servicio_tecnico_repositorio
        self._departamento_repositorio = departamento_repositorio
        self._tipo_servicio_tecnico_repositorio = tipo_servicio_tecnico_repositorio
    
    def _validar_campos_servicio_tecnico(
        self,
        nombre_departamento_limpio: str,
        falla_presenta_limpio: str,
        tipo_servicio_prestado_limpio: str,
        nombres_tecnicos_limpio: str,
        descripcion_limpio: Optional[str],
        observaciones_adicionales_limpio: Optional[str]
    ) -> List[str]:
        errores = []
        
        # Validar el nombre del departamento
        if not(nombre_departamento_limpio):
            errores.append("Departamento: Debe elegir un departamento.")
        
        # Validar el tipo de servicio prestado
        if not (tipo_servicio_prestado_limpio):
            errores.append("Tipo de servicio: Debe elegir un tipo de servicio.")
        
        # Validar la falla que presenta
        if not(falla_presenta_limpio):
            errores.append("Falla que presenta: No puede estar vacío.")
        elif (len(falla_presenta_limpio) > 150):
            errores.append("Falla que presenta: No puede contener más de 150 caracteres.")
        
        #  Validar el nombre del técnico
        if not(nombres_tecnicos_limpio):
            errores.append("Nombre del técnico: No puede estar vacío.")
        elif (len(nombres_tecnicos_limpio) > 250):
            errores.append("Nombre del técnico: No puede contener más de 250 caracteres.")
        
        # Validando la descripción
        if (descripcion_limpio is not None):
            if (len(descripcion_limpio) > 255):
                errores.append("Descripción: No puede contener más de 255 caracteres.")
        
        #  Validar las observaciones adicionales
        if (observaciones_adicionales_limpio is not None):
            if (len(observaciones_adicionales_limpio) > 255):
                errores.append("Observaciones adicionales: No puede contener más de 255 caracteres.")
        
        return errores
    
    def registrar(
        self,
        nombre_departamento: str,
        fecha_servicio: date,
        falla_presenta: str,
        tipo_servicio_prestado: str,
        nombres_tecnicos: str,
        cantidad: int,
        descripcion: Optional[str],
        observaciones_adicionales: Optional[str]
    ) -> None:
        nombre_departamento_limpio = nombre_departamento.strip() if nombre_departamento else ""
        falla_presenta_limpio = falla_presenta.strip() if falla_presenta else ""
        tipo_servicio_prestado_limpio = tipo_servicio_prestado.strip() if tipo_servicio_prestado else ""
        nombres_tecnicos_limpio = nombres_tecnicos.strip() if nombres_tecnicos else ""
        descripcion_limpio = descripcion.strip() if descripcion else None
        observaciones_adicionales_limpio = observaciones_adicionales.strip() if observaciones_adicionales else None
        
        errores = self._validar_campos_servicio_tecnico(
            nombre_departamento_limpio,
            falla_presenta_limpio,
            tipo_servicio_prestado_limpio,
            nombres_tecnicos_limpio,
            descripcion_limpio,
            observaciones_adicionales_limpio
        )
        
        if (errores):
            raise ValidacionError(errores)
        
        departamento = self._departamento_repositorio.obtener_por_nombre(nombre_departamento_limpio)
        tipo_servicio = self._tipo_servicio_tecnico_repositorio.obtener_por_tipo_servicio(tipo_servicio_prestado_limpio)
        try:
            nuevo_servicio_tecnico = ServicioTecnicoModelo(
                departamento_id = departamento.departamento_id,
                fecha_servicio = fecha_servicio,
                falla_presenta = falla_presenta_limpio,
                tipo_servicio_id = tipo_servicio.tipo_servicio_id,
                nombres_tecnicos = nombres_tecnicos_limpio,
                cantidad = cantidad,
                descripcion = descripcion_limpio,
                observaciones_adicionales = observaciones_adicionales_limpio
            )
            self._servicio_tecnico_repositorio.registrar(nuevo_servicio_tecnico)
        except NoEncontradoError as error:
            raise error
        except SQLAlchemyError as error:
            raise LogicaError([f"Error técnico en la base datos al registrar: {str(error)}"])
    
    def obtener_por_id(self, servicio_id: int) -> Optional[ServicioTecnicoModelo]:
        return self._servicio_tecnico_repositorio.obtener_por_id(servicio_id)
    
    def obtener_por_departamento_id(self, departamento_id: int) -> List[ServicioTecnicoModelo]:
        return list(self._servicio_tecnico_repositorio.obtener_por_departamento_id(departamento_id))
    
    def obtener_por_tipo_servicio_id(self, tipo_servicio_id: int) -> List[ServicioTecnicoModelo]:
        return list(self._servicio_tecnico_repositorio.obtener_por_tipo_servicio_id(tipo_servicio_id))
    
    def obtener_por_mes_anio(self, mes_anio: str, tipo_servicio_prestado: Optional[str]) -> List[Tuple]:
        servicios = list(self._servicio_tecnico_repositorio.obtener_por_mes_anio(mes_anio, tipo_servicio_prestado))
        if not(servicios):
            raise NoEncontradoError(["No hay servicios en este mes y año."])
        
        return servicios
    
    def obtener_por_rango_fecha(self, fecha_desde: date, fecha_hasta: date, tipo_servicio_prestado: Optional[str]) -> List[Tuple]:
        if (fecha_desde > fecha_hasta):
            raise ValidacionError(["La fecha de inicio no puede ser mayor que la fecha de fin."])
        
        servicios = list(self._servicio_tecnico_repositorio.obtener_por_rango_fecha(fecha_desde, fecha_hasta, tipo_servicio_prestado))
        if not(servicios):
            raise NoEncontradoError(["No hay servicios dentro de este rango de fecha."])
        
        
        return servicios
    
    def obtener_por_anio(self, anio: str, tipo_servicio_prestado: Optional[str])-> List[Tuple]:
        servicios = list(self._servicio_tecnico_repositorio.obtener_por_anio(anio, tipo_servicio_prestado))
        if not(servicios):
            raise NoEncontradoError(["No hay servicios en este año."])
        
        return servicios
    
    def obtener_por_fecha_o_departamento_o_tipo_servicio(
        self, 
        fecha_servicio: date, 
        nombre_departamento: Optional[str], 
        tipo_servicio_prestado: Optional[str]
    ) -> List[Tuple]:
        servicios = list(self._servicio_tecnico_repositorio.obtener_por_fecha_o_departamento_o_tipo_servicio(fecha_servicio, nombre_departamento, tipo_servicio_prestado))
        if not(servicios):
            raise NoEncontradoError(["No hay servicios por esta fecha, departamento o tipo de servicio"])
        
        return servicios
    
    def obtener_conteo_tipos_servicios_realizados(self, mes_anio: str, tipo_servicio_prestado: Optional[str]) -> List[Tuple]:
        return list(self._servicio_tecnico_repositorio.obtener_conteo_tipos_servicios_realizados(mes_anio, tipo_servicio_prestado))
    
    def obtener_conteo_tipos_servicios_realizados_por_rango_fecha(
        self, 
        fecha_desde: date, 
        fecha_hasta: date, 
        tipo_servicio_prestado: Optional[str]
    ) -> List[Tuple]:
        return list(self._servicio_tecnico_repositorio.obtener_conteo_tipos_servicios_realizados_por_rango_fecha(fecha_desde, fecha_hasta, tipo_servicio_prestado))
    
    def obtener_conteo_tipos_servicios_realizados_por_anio(self, anio: str, tipo_servicio_prestado: Optional[str]) -> List[Tuple]:
        return list(self._servicio_tecnico_repositorio.obtener_conteo_tipos_servicios_realizados_por_anio(anio, tipo_servicio_prestado))
    
    def obtener_conteo_servicios_x_departamento(self, mes_anio: str, tipo_servicio_prestado: Optional[str]) -> List[Tuple]:
        return list(self._servicio_tecnico_repositorio.obtener_conteo_servicios_x_departamento(mes_anio, tipo_servicio_prestado))
    
    def obtener_conteo_servicios_x_departamento_por_rango_fecha(
        self, 
        fecha_desde: date, 
        fecha_hasta: date, 
        tipo_servicio_prestado: Optional[str]
    ) -> List[Tuple]:
        return list(self._servicio_tecnico_repositorio.obtener_conteo_servicios_x_departamento_por_rango_fecha(fecha_desde, fecha_hasta, tipo_servicio_prestado))
    
    def obtener_conteo_servicios_x_departamento_por_anio(self, anio: str, tipo_servicio_prestado: Optional[str]) -> List[Tuple]:
        return list(self._servicio_tecnico_repositorio.obtener_conteo_servicios_x_departamento_por_anio(anio, tipo_servicio_prestado))
    
    def obtener_conteo_agrupado_servicios_x_departamento(self, mes_anio: str, tipo_servicio_prestado: Optional[str]) -> List[Tuple]:
        return list(self._servicio_tecnico_repositorio.obtener_conteo_agrupado_servicios_x_departamento(mes_anio, tipo_servicio_prestado))
    
    def obtener_conteo_agrupado_servicios_x_departamento_por_rango_fecha(
        self, 
        fecha_desde: date, 
        fecha_hasta: date, 
        tipo_servicio_prestado: Optional[str]
    ) -> List[Tuple]:
        return list(self._servicio_tecnico_repositorio.obtener_conteo_agrupado_servicios_x_departamento_por_rango_fecha(fecha_desde, fecha_hasta, tipo_servicio_prestado))
    
    def obtener_conteo_agrupado_servicios_x_departamento_por_anio(self, anio: str, tipo_servicio_prestado: Optional[str]) -> List[Tuple]:
        return list(self._servicio_tecnico_repositorio.obtener_conteo_agrupado_servicios_x_departamento_por_anio(anio, tipo_servicio_prestado))
    
    def obtener_tipo_reporte_a_generar(
        self,
        tipo_reporte_a_generar: Optional[str] = None,
        mes_anio: Optional[str] = None,
        fecha_desde: Optional[date] = None,
        fecha_hasta: Optional[date] = None,
        anio: Optional[str] = None,
        tipo_servicio_prestado: Optional[str] = None
    ) -> Dict:
        servicios_realizados = None
        conteo_tipos_servicio = None
        conteo_tipos_servicio_x_departamento = None
        conteo_agrupado_servicios_x_departamento = None
        
        if (tipo_reporte_a_generar == "MENSUAL"):
            servicios_realizados = self.obtener_por_mes_anio(mes_anio, tipo_servicio_prestado)
            conteo_tipos_servicio = self.obtener_conteo_tipos_servicios_realizados(mes_anio, tipo_servicio_prestado)
            conteo_tipos_servicio_x_departamento = self.obtener_conteo_servicios_x_departamento(mes_anio, tipo_servicio_prestado)
            conteo_agrupado_servicios_x_departamento = self.obtener_conteo_agrupado_servicios_x_departamento(mes_anio, tipo_servicio_prestado)
        elif (tipo_reporte_a_generar == "RANGO_FECHA"):
            servicios_realizados = self.obtener_por_rango_fecha(fecha_desde, fecha_hasta, tipo_servicio_prestado)
            conteo_tipos_servicio = self.obtener_conteo_tipos_servicios_realizados_por_rango_fecha(fecha_desde, fecha_hasta, tipo_servicio_prestado)
            conteo_tipos_servicio_x_departamento = self.obtener_conteo_servicios_x_departamento_por_rango_fecha(fecha_desde, fecha_hasta, tipo_servicio_prestado)
            conteo_agrupado_servicios_x_departamento = self.obtener_conteo_agrupado_servicios_x_departamento_por_rango_fecha(fecha_desde, fecha_hasta, tipo_servicio_prestado)
        elif (tipo_reporte_a_generar == "ANUAL"):
            servicios_realizados = self.obtener_por_anio(anio, tipo_servicio_prestado)
            conteo_tipos_servicio = self.obtener_conteo_tipos_servicios_realizados_por_anio(anio, tipo_servicio_prestado)
            conteo_tipos_servicio_x_departamento = self.obtener_conteo_servicios_x_departamento_por_anio(anio, tipo_servicio_prestado)
            conteo_agrupado_servicios_x_departamento = self.obtener_conteo_agrupado_servicios_x_departamento_por_anio(anio, tipo_servicio_prestado)
        
        return {
            "servicios_realizados": servicios_realizados,
            "conteo_tipos_servicio": conteo_tipos_servicio,
            "conteo_tipos_servicio_x_departamento": conteo_tipos_servicio_x_departamento,
            "conteo_agrupado_servicios_x_departamento": conteo_agrupado_servicios_x_departamento
        }
    
    def actualizar(
        self,
        servicio_id: int,
        nuevo_departamento: str,
        nuevo_fecha_servicio: date,
        nuevo_falla_presenta: str,
        nuevo_tipo_servicio: str,
        nuevo_nombres_tecnicos: str,
        nuevo_cantidad: int,
        nuevo_descripcion: Optional[str],
        nuevo_observaciones_adicionales: Optional[str]
    ) -> None:
        nuevo_departamento_limpio = nuevo_departamento.strip() if nuevo_departamento else ""
        nuevo_falla_presenta_limpio = nuevo_falla_presenta.strip() if nuevo_falla_presenta else ""
        nuevo_tipo_servicio_prestado_limpio = nuevo_tipo_servicio.strip() if nuevo_tipo_servicio else ""
        nuevo_nombres_tecnicos_limpio = nuevo_nombres_tecnicos.strip() if nuevo_nombres_tecnicos else ""
        nuevo_descripcion_limpio = nuevo_descripcion.strip() if nuevo_descripcion else None
        nuevo_observaciones_adicionales_limpio = nuevo_observaciones_adicionales.strip() if nuevo_observaciones_adicionales else None
        
        errores = self._validar_campos_servicio_tecnico(
            nuevo_departamento_limpio,
            nuevo_falla_presenta_limpio,
            nuevo_tipo_servicio_prestado_limpio,
            nuevo_nombres_tecnicos_limpio,
            nuevo_descripcion_limpio,
            nuevo_observaciones_adicionales_limpio
        )
        
        if (errores):
            raise ValidacionError(errores)
        
        nuevo_departamento = self._departamento_repositorio.obtener_por_nombre(nuevo_departamento_limpio)
        nuevo_tipo_servicio = self._tipo_servicio_tecnico_repositorio.obtener_por_tipo_servicio(nuevo_tipo_servicio_prestado_limpio)
        try:
            servicio_tecnico_actualizado = ServicioTecnicoModelo(
                servicio_id = servicio_id,
                departamento_id = nuevo_departamento.departamento_id,
                fecha_servicio = nuevo_fecha_servicio,
                falla_presenta = nuevo_falla_presenta_limpio,
                tipo_servicio_id = nuevo_tipo_servicio.tipo_servicio_id,
                nombres_tecnicos = nuevo_nombres_tecnicos_limpio,
                cantidad = nuevo_cantidad,
                descripcion = nuevo_descripcion_limpio,
                observaciones_adicionales = nuevo_observaciones_adicionales_limpio
            )
            self._servicio_tecnico_repositorio.actualizar(servicio_tecnico_actualizado)
        except NoEncontradoError as error:
            raise error
        except SQLAlchemyError as error:
            raise LogicaError([f"Error técnico en la base datos al actualizar: {str(error)}"])
    
    def eliminar(self, servicio_id: int) -> None:
        try:
            servicio_a_eliminar = ServicioTecnicoModelo(servicio_id = servicio_id)
            self._servicio_tecnico_repositorio.eliminar(servicio_a_eliminar)
        except NoEncontradoError as error:
            raise error
        except SQLAlchemyError as error:
            raise LogicaError([f"Error técnico en la base datos al eliminar: {str(error)}"])