from datetime import date
from dominio.entidades.servicio import Servicio
from dominio.excepciones import ServicioValidacionError
from aplicacion.unidad_trabajo.unidad_trabajo_base import UnidadTrabajo
from aplicacion.unidad_trabajo.sqlalchemy_unidad_trabajo import SQLAlchemyUnidadTrabajo
from typing import Optional, Generator, List, Tuple


class ListarServicios:
    def __init__(self, unidad_trabajo: UnidadTrabajo):
        self.unidad_trabajo = unidad_trabajo
    
    def obtener_todos(self) -> Optional[Generator[Servicio, None, None]]:
        with self.unidad_trabajo() as unidad_trabajo:
            servicios = unidad_trabajo.servicio.obtener_todos()
            return servicios
    
    def obtener_por_id(self, servicio_id: int) -> Optional[Servicio]:
        with self.unidad_trabajo() as unidad_trabajo:
            try:
                errores = []
                
                servicio = unidad_trabajo.servicio.obtener_por_id(servicio_id)
                
                if not(servicio):
                    errores.append("Este servicio no existe.")
                
                if (errores):
                    raise ServicioValidacionError(errores)
                
                return servicio
            except ServicioValidacionError as error:
                raise error
            except Exception as error:
                raise error
    
    def obtener_por_departamento_id(self, departamento_id: int) -> Optional[Generator[Servicio, None, None]]:
        with self.unidad_trabajo() as unidad_trabajo:
            try:
                errores = []
                
                servicios = list(unidad_trabajo.servicio.obtener_por_departamento_id(departamento_id))
                
                if not(servicios):
                    errores.append("No hay servicios hechos por ese departamento.")
                
                if (errores):
                    raise ServicioValidacionError(errores)
                
                return servicios
            except ServicioValidacionError as error:
                raise error
            except Exception as error:
                raise error
    
    def obtener_por_tipo_servicio_id(self, tipo_servicio_id: int) -> Optional[Generator[Servicio, None, None]]:
        with self.unidad_trabajo() as unidad_trabajo:
            try:
                errores = []
                
                servicios = list(unidad_trabajo.servicio.obtener_por_tipo_servicio_id(tipo_servicio_id))
                
                if not(servicios):
                    errores.append("No hay servicios hechos por ese tipo de servicio.")
                
                if (errores):
                    raise ServicioValidacionError(errores)
                
                return servicios
            except ServicioValidacionError as error:
                raise error
            except Exception as error:
                raise error
    
    def obtener_por_mes_anio(self, mes_anio: str) -> Optional[Generator[List[Tuple], None, None]]:
        with self.unidad_trabajo() as unidad_trabajo:
            try:
                errores = []
                
                servicios_resultado = list(unidad_trabajo.servicio.obtener_por_mes_anio(mes_anio))
                
                if not(servicios_resultado):
                    errores.append("No hay servicios en este mes y año.")
                
                if (errores):
                    raise ServicioValidacionError(errores)
                
                return servicios_resultado
            except ServicioValidacionError as error:
                raise error
            except Exception as error:
                raise error
    
    def obtener_por_rango_fecha(self, fecha_desde: date, fecha_hasta: date) -> Optional[Generator[List[Tuple], None, None]]:
        with self.unidad_trabajo() as unidad_trabajo:
            try:
                errores = []
                
                servicios_resultado = list(unidad_trabajo.servicio.obtener_por_rango_fecha(fecha_desde, fecha_hasta))
                
                if not (servicios_resultado):
                    errores.append("No hay servicios dentro de ese rango.")
                
                if (fecha_desde > fecha_hasta):
                    errores.append("La fecha de inicio no puede ser mayor que la fecha de fin.")
                
                if (errores):
                    raise ServicioValidacionError(errores)
                
                return servicios_resultado
            except ServicioValidacionError as error:
                raise error
            except Exception as error:
                raise error
    
    def obtener_por_anio(self, anio: str) -> Optional[Generator[List[Tuple], None, None]]:
        with self.unidad_trabajo() as unidad_trabajo:
            try:
                errores = []
                
                servicios_resultado = list(unidad_trabajo.servicio.obtener_por_anio(anio))
                
                if not(servicios_resultado):
                    errores.append("No hay servicios realizados en este año.")
                
                if (errores):
                    raise ServicioValidacionError(errores)
                
                return servicios_resultado
            except ServicioValidacionError as error:
                raise error
            except Exception as error:
                raise error
    
    def obtener_por_fecha_o_departamento_o_tipo_servicio(self, fecha_servicio: date, nombre_departamento: Optional[str] = None, tipo_servicio_prestado: str = None) -> Generator[List[Tuple], None, None]:
        with self.unidad_trabajo() as unidad_trabajo:
            try:
                errores = []
                
                servicios_resultado = list(unidad_trabajo.servicio.obtener_por_fecha_o_departamento_o_tipo_servicio(fecha_servicio, nombre_departamento, tipo_servicio_prestado))
                
                if not(servicios_resultado):
                    errores.append("No hay servicios hechos por ese departamento, fecha o tipo de servicio.")
                
                if (errores):
                    raise ServicioValidacionError(errores)
                
                return servicios_resultado
            except ServicioValidacionError as error:
                raise error
            except Exception as error:
                raise error
    
    def obtener_conteo_tipos_servicios_realizados(self, mes_anio: str) -> Generator[List[Tuple], None, None]:
        with self.unidad_trabajo() as unidad_trabajo:
            try:                
                conteo_resultado = list(unidad_trabajo.servicio.obtener_conteo_tipos_servicios_realizados(mes_anio))
                return conteo_resultado
            except Exception as error:
                raise error
    
    def obtener_conteo_tipos_servicios_realizados_por_rango_fecha(self, fecha_desde: date, fecha_hasta: date) -> Generator[List[Tuple], None, None]:
        with self.unidad_trabajo() as unidad_trabajo:
            try:
                conteo_resultado = list(unidad_trabajo.servicio.obtener_conteo_tipos_servicios_realizados_por_rango_fecha(fecha_desde, fecha_hasta))
                return conteo_resultado
            except Exception as error:
                raise error
    
    def obtener_conteo_tipos_servicios_realizados_por_anio(self, anio: str) -> Generator[List[Tuple], None, None]:
        with self.unidad_trabajo() as unidad_trabajo:
            try:
                conteo_resultado = list(unidad_trabajo.servicio.obtener_conteo_tipos_servicios_realizados_por_anio(anio))
                return conteo_resultado
            except Exception as error:
                raise error
    
    def obtener_conteo_servicios_x_departamento(self, mes_anio: str) -> Generator[List[Tuple], None, None]:
        with self.unidad_trabajo() as unidad_trabajo:
            try:
                conteo_resultado = list(unidad_trabajo.servicio.obtener_conteo_servicios_x_departamento(mes_anio))
                return conteo_resultado
            except Exception as error:
                raise error
    
    def obtener_conteo_servicios_x_departamento_por_rango_fecha(self, fecha_desde: date, fecha_hasta: date):
        with self.unidad_trabajo() as unidad_trabajo:
            try:
                conteo_resultado = list(unidad_trabajo.servicio.obtener_conteo_servicios_x_departamento_por_rango_fecha(fecha_desde, fecha_hasta))
                return conteo_resultado
            except Exception as error:
                raise error
    
    def obtener_conteo_servicios_x_departamento_por_anio(self, anio: str):
        with self.unidad_trabajo() as unidad_trabajo:
            try:
                conteo_resultado = list(unidad_trabajo.servicio.obtener_conteo_servicios_x_departamento_por_anio(anio))
                return conteo_resultado
            except Exception as error:
                raise error


if __name__ == "__main__":
    try:
        unidad_trabajo = SQLAlchemyUnidadTrabajo
        listar_servicios = ListarServicios(unidad_trabajo)
        
        """for servicio in listar_servicios.obtener_todos():
            print(f"- ID DEPARTAMENTO: {servicio.departamento_id} \n- FECHA SERVICIO: {servicio.fecha_servicio} \n- FALLA QUE PRESENTA: {servicio.falla_presenta} \n- SERVICIO PRESTADO: {servicio.servicio_prestado} \n- NOMBRES DE LOS TÉCNICOS: {servicio.nombres_tecnicos} \n")"""
        
        servicio = listar_servicios.obtener_por_id(2)
        """print(f"- ID DEPARTAMENTO: {servicio.departamento_id} \n- FECHA SERVICIO: {servicio.fecha_servicio} \n- FALLA QUE PRESENTA: {servicio.falla_presenta} \n- SERVICIO PRESTADO: {servicio.servicio_prestado} \n- NOMBRES DE LOS TÉCNICOS: {servicio.nombres_tecnicos} \n")"""
        
        """servicios = listar_servicios.obtener_por_departamento_id(12)
        for servicio in servicios:
            print(f"- ID DEPARTAMENTO: {servicio.departamento_id} \n- FECHA SERVICIO: {servicio.fecha_servicio} \n- FALLA QUE PRESENTA: {servicio.falla_presenta} \n- SERVICIO PRESTADO: {servicio.servicio_prestado} \n- NOMBRES DE LOS TÉCNICOS: {servicio.nombres_tecnicos} \n")"""
        
        # Para especificar el departamento pasarle el nombre_departamento
        servicios = listar_servicios.obtener_por_fecha_o_departamento_o_tipo_servicio(
            fecha_servicio = date(2025, 9, 1),
            nombre_departamento = "1X1OM"
        )
        for servicio in servicios:
            print(f"- NOMBRE DEPARTAMENTO: {servicio[3]} \n- FECHA SERVICIO: {servicio[4]} \n- FALLA QUE PRESENTA: {servicio[5]} \n- SERVICIO PRESTADO: {servicio[6]} \n- NOMBRES DE LOS TÉCNICOS: {servicio[7]} \n")
    except ServicioValidacionError as error:
        print("\n".join(error.errores))
    except Exception as error:
        print(error)