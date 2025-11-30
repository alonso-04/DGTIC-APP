from datetime import date
from sqlalchemy import text
from sqlalchemy.orm import Session
from dominio.entidades.servicio import Servicio
from dominio.puertos.servicio_puerto import ServicioPuerto
from infraestructura.modelos.servicio_modelo import ServicioModelo
from typing import Optional, Generator, List, Tuple


class ServicioAdaptador(ServicioPuerto):
    def __init__(self, sesion: Session):
        self._sesion = sesion
    
    def registrar(self, servicio: Servicio) -> None:
        servicio_modelo = ServicioModelo(
            departamento_id = servicio.departamento_id,
            fecha_servicio = servicio.fecha_servicio,
            falla_presenta = servicio.falla_presenta,
            tipo_servicio_id = servicio.tipo_servicio_id,
            nombres_tecnicos = servicio.nombres_tecnicos,
            observaciones_adicionales = servicio.observaciones_adicionales
        )
        
        self._sesion.add(servicio_modelo)
    
    def obtener_todos(self) -> Optional[Generator[Servicio, None, None]]:
        servicios_modelo = self._sesion.query(ServicioModelo).yield_per(100)
        
        for servicio in servicios_modelo:
            yield Servicio(
                servicio_id = servicio.servicio_id,
                fecha_servicio = servicio.fecha_servicio,
                falla_presenta = servicio.falla_presenta,
                nombres_tecnicos = servicio.nombres_tecnicos,
                departamento_id = servicio.departamento_id,
                tipo_servicio_id = servicio.tipo_servicio_id,
                observaciones_adicionales = servicio.observaciones_adicionales
            )
    
    def obtener_por_id(self, servicio_id: int) -> Optional[Servicio]:
        servicio_modelo = self._sesion.query(ServicioModelo).filter_by(servicio_id = servicio_id).first()
        
        if (servicio_modelo):
            return Servicio(
                servicio_id = servicio_modelo.servicio_id,
                fecha_servicio = servicio_modelo.fecha_servicio,
                falla_presenta = servicio_modelo.falla_presenta,
                nombres_tecnicos = servicio_modelo.nombres_tecnicos,
                departamento_id = servicio_modelo.departamento_id,
                tipo_servicio_id = servicio_modelo.tipo_servicio_id,
                observaciones_adicionales = servicio_modelo.observaciones_adicionales
            )
        return None
    
    def obtener_por_departamento_id(self, departamento_id: int) -> Optional[Generator[Servicio, None, None]]:
        servicios_modelo = self._sesion.query(ServicioModelo).filter_by(departamento_id = departamento_id).yield_per(100)
        
        for servicio in servicios_modelo:
            yield Servicio(
                fecha_servicio = servicio.fecha_servicio,
                falla_presenta = servicio.falla_presenta,
                nombres_tecnicos = servicio.nombres_tecnicos,
                departamento_id = servicio.departamento_id,
                tipo_servicio_id = servicio.tipo_servicio_id,
                servicio_id = servicio.servicio_id,
                observaciones_adicionales = servicio.observaciones_adicionales
            )
        return None
    
    def obtener_por_tipo_servicio_id(self, tipo_servicio_id: int) -> Optional[Generator[Servicio, None, None]]:
        servicios_modelo = self._sesion.query(ServicioModelo).filter_by(tipo_servicio_id = tipo_servicio_id).yield_per(100)
        
        for servicio in servicios_modelo:
            yield Servicio(
                fecha_servicio = servicio.fecha_servicio,
                falla_presenta = servicio.falla_presenta,
                nombres_tecnicos = servicio.nombres_tecnicos,
                departamento_id = servicio.departamento_id,
                tipo_servicio_id = servicio.tipo_servicio_id,
                servicio_id = servicio.servicio_id,
                observaciones_adicionales = servicio.observaciones_adicionales
            )
        return None
    
    def obtener_por_mes_anio(self, mes_anio: str) -> Optional[Generator[List[Tuple], None, None]]:
        mes, anio = mes_anio.split("-")
        mes = int(mes)
        anio = int(anio)
        
        consulta = """
            SELECT
                servicio_id,
                departamento_id,
                tipo_servicio_id,
                nombre_departamento,
                DATE_FORMAT(fecha_servicio, '%m-%Y') AS mes_anio,
                fecha_servicio,
                falla_presenta,
                tipo_servicio_prestado,
                nombres_tecnicos,
                observaciones_adicionales
            FROM vw_servicios_prestados
            WHERE MONTH(fecha_servicio) = :mes
            AND YEAR(fecha_servicio)  = :anio;
        """
        
        parametros = {
            "mes": mes,
            "anio": anio
        }
        
        servicios_modelo = self._sesion.execute(text(consulta), parametros).yield_per(100)
        
        for servicio in servicios_modelo:
            yield servicio
        return None
    
    def obtener_por_fecha_o_departamento_o_tipo_servicio(self, fecha_servicio: date, nombre_departamento: Optional[str] = None, tipo_servicio_prestado: str = None) -> Optional[Generator[List[Tuple], None, None]]:
        consulta = """
            SELECT
                servicio_id,
                departamento_id,
                tipo_servicio_id,
                nombre_departamento,
                fecha_servicio,
                falla_presenta,
                tipo_servicio_prestado,
                nombres_tecnicos,
                observaciones_adicionales
            FROM vw_servicios_prestados
            WHERE fecha_servicio = :fecha_servicio
        """
        parametros = {"fecha_servicio": fecha_servicio}
        
        condiciones_adicionales = []
        
        if (nombre_departamento):
            condiciones_adicionales.append("nombre_departamento = :nombre_departamento")
            parametros["nombre_departamento"] = nombre_departamento
        
        if (tipo_servicio_prestado):
            condiciones_adicionales.append("tipo_servicio_prestado = :tipo_servicio_prestado")
            parametros["tipo_servicio_prestado"] = tipo_servicio_prestado
        
        if (condiciones_adicionales):
            consulta += " AND " + " AND ".join(condiciones_adicionales)
        
        servicios_modelo = self._sesion.execute(text(consulta), parametros).yield_per(100)
        
        for servicio in servicios_modelo:
            yield servicio
        return None
    
    def obtener_conteo_tipos_servicios_realizados(self, mes_anio: str) -> Optional[Generator[List[Tuple], None, None]]:
        mes, anio = mes_anio.split("-")
        mes = int(mes)
        anio = int(anio)
        
        consulta = """
            SELECT
                tipo_servicio_prestado,
                COUNT(*) AS cantidad
            FROM vw_servicios_prestados
            WHERE MONTH(fecha_servicio) = :mes
            AND YEAR(fecha_servicio) = :anio
            GROUP BY tipo_servicio_prestado;
        """
        
        parametros = {
            "mes": mes,
            "anio": anio
        }
        
        conteo_servicios_modelo = self._sesion.execute(text(consulta), parametros).yield_per(100)
        
        for conteo_servicio in conteo_servicios_modelo:
            yield conteo_servicio
        return None
    
    def obtener_conteo_servicios_x_departamento(self, mes_anio: str) -> Optional[Generator[List[Tuple], None, None]]:
        mes, anio = mes_anio.split("-")
        mes = int(mes)
        anio = int(anio)
        
        consulta = """
            SELECT
                nombre_departamento,
                tipo_servicio_prestado,
                COUNT(*) AS cantidad
            FROM vw_servicios_prestados
            WHERE MONTH(fecha_servicio) = :mes
            AND YEAR(fecha_servicio) = :anio
            GROUP BY nombre_departamento, tipo_servicio_prestado;
        """
        parametros = {
            "mes": mes,
            "anio": anio
        }
        
        conteo_servicios_modelo = self._sesion.execute(text(consulta), parametros).yield_per(100)
        
        for conteo_servicio in conteo_servicios_modelo:
            yield conteo_servicio
        return None
    
    def actualizar(self, servicio: Servicio) -> None:
        servicio_modelo = self._sesion.query(ServicioModelo).filter_by(servicio_id = servicio.servicio_id).first()
        
        if not(servicio_modelo):
            raise ValueError("Este servicio no existe.")
        
        servicio_modelo.departamento_id = servicio.departamento_id
        servicio_modelo.fecha_servicio = servicio.fecha_servicio
        servicio_modelo.falla_presenta = servicio.falla_presenta
        servicio_modelo.tipo_servicio_id = servicio.tipo_servicio_id
        servicio_modelo.nombres_tecnicos = servicio.nombres_tecnicos
        servicio_modelo.observaciones_adicionales = servicio.observaciones_adicionales
    
    def eliminar(self, servicio: Servicio) -> None:
        servicio_modelo = self._sesion.query(ServicioModelo).filter_by(servicio_id = servicio.servicio_id).first()
        
        if not(servicio_modelo):
            raise ValueError("Este servicio no existe.")
        
        self._sesion.delete(servicio_modelo)