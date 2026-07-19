from typing import Optional, Generator, Tuple
from datetime import date
from sqlalchemy import text

from configuraciones.excepciones import NoEncontradoError
from modelos.servicio_tecnico_modelo import ServicioTecnicoModelo


class ServicioTecnicoRepositorio:
    def __init__(self, bd):
        self._bd = bd
    
    def registrar(self, servicio: ServicioTecnicoModelo) -> None:
        with self._bd.sesion() as sesion:
            sesion.add(servicio)
    
    def obtener_por_id(self, servicio_id: int) -> Optional[ServicioTecnicoModelo]:
        with self._bd.sesion() as sesion:
            servicio_modelo = sesion.query(ServicioTecnicoModelo).filter_by(servicio_id = servicio_id).first()
            
            if not(servicio_modelo):
                raise NoEncontradoError(["Este servicio técnico no existe"])
            
            return servicio_modelo
    
    def obtener_por_departamento_id(self, departamento_id: int) -> Generator[ServicioTecnicoModelo, None, None]:
        with self._bd.sesion() as sesion:
            servicios_modelo = sesion.query(ServicioTecnicoModelo).filter_by(departamento_id = departamento_id).yield_per(100)
            
            for servicio in servicios_modelo:
                yield servicio
    
    def obtener_por_tipo_servicio_id(self, tipo_servicio_id: int) -> Generator[ServicioTecnicoModelo, None, None]:
        with self._bd.sesion() as sesion:
            servicios_modelo = sesion.query(ServicioTecnicoModelo).filter_by(tipo_servicio_id = tipo_servicio_id).yield_per(100)
            
            for servicio in servicios_modelo:
                yield servicio
    
    def obtener_por_mes_anio(self, mes_anio: str, tipo_servicio_prestado: Optional[str] = None) -> Generator[Tuple, None, None]:
        with self._bd.sesion() as sesion:
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
                    descripcion,
                    cantidad,
                    observaciones_adicionales
                FROM vw_servicios_prestados
                WHERE MONTH(fecha_servicio) = :mes
                AND YEAR(fecha_servicio)  = :anio
            """
            
            parametros = {
                "mes": mes,
                "anio": anio
            }
            
            condiciones_adicionales = []
            
            if (tipo_servicio_prestado):
                condiciones_adicionales.append("tipo_servicio_prestado = :tipo_servicio_prestado")
                parametros["tipo_servicio_prestado"] = tipo_servicio_prestado
            
            if (condiciones_adicionales):
                consulta += " AND " + " AND ".join(condiciones_adicionales)
            
            consulta += " ORDER BY fecha_servicio"
            
            servicios_modelo = sesion.execute(text(consulta), parametros).yield_per(100)
            
            for servicio in servicios_modelo:
                yield servicio
    
    def obtener_por_rango_fecha(self, fecha_desde: date, fecha_hasta: date, tipo_servicio_prestado: Optional[str] = None) -> Generator[Tuple, None, None]:
        with self._bd.sesion() as sesion:
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
                    descripcion,
                    cantidad,
                    observaciones_adicionales
                FROM vw_servicios_prestados
                WHERE fecha_servicio BETWEEN :fecha_desde AND :fecha_hasta
            """
            
            parametros = {
                "fecha_desde": fecha_desde,
                "fecha_hasta": fecha_hasta
            }
            
            condiciones_adicionales = []
            
            if (tipo_servicio_prestado):
                condiciones_adicionales.append("tipo_servicio_prestado = :tipo_servicio_prestado")
                parametros["tipo_servicio_prestado"] = tipo_servicio_prestado
            
            if (condiciones_adicionales):
                consulta += " AND " + " AND ".join(condiciones_adicionales)
            
            consulta += " ORDER BY fecha_servicio"
            
            servicios_modelo = sesion.execute(text(consulta), parametros).yield_per(100)
            
            for servicio in servicios_modelo:
                yield servicio
    
    def obtener_por_anio(self, anio: str, tipo_servicio_prestado: Optional[str] = None) -> Generator[Tuple, None, None]:
        with self._bd.sesion() as sesion:
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
                    descripcion,
                    cantidad,
                    observaciones_adicionales
                FROM vw_servicios_prestados
                WHERE YEAR(fecha_servicio) = :anio
            """
            
            parametros = {"anio": anio}
            
            condiciones_adicionales = []
            
            if (tipo_servicio_prestado):
                condiciones_adicionales.append("tipo_servicio_prestado = :tipo_servicio_prestado")
                parametros["tipo_servicio_prestado"] = tipo_servicio_prestado
            
            if (condiciones_adicionales):
                consulta += " AND " + " AND ".join(condiciones_adicionales)
            
            consulta += " ORDER BY fecha_servicio"
            
            servicios_modelo = sesion.execute(text(consulta), parametros).yield_per(100)
            
            for servicio in servicios_modelo:
                yield servicio
    
    def obtener_por_fecha_o_departamento_o_tipo_servicio(self, fecha_servicio: date, nombre_departamento: Optional[str], tipo_servicio_prestado: Optional[str]) -> Generator[Tuple, None, None]:
        with self._bd.sesion() as sesion:
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
                    descripcion,
                    cantidad,
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
            
            servicios_modelo = sesion.execute(text(consulta), parametros).yield_per(100)
            
            for servicio in servicios_modelo:
                yield servicio
    
    def obtener_conteo_tipos_servicios_realizados(self, mes_anio: str, tipo_servicio_prestado: Optional[str]) -> Generator[Tuple, None, None]:
        with self._bd.sesion() as sesion:
            mes, anio = mes_anio.split("-")
            mes = int(mes)
            anio = int(anio)
            
            consulta = """
                SELECT 
                    tipos_servicio.tipo_servicio_prestado,
                    categoria_tipo_servicio.nombre_categoria,
                    SUM(servicios.cantidad) AS total_servicios_realizados
                FROM tb_servicios servicios
                INNER JOIN tb_tipos_servicio tipos_servicio ON servicios.tipo_servicio_id = tipos_servicio.tipo_servicio_id
                INNER JOIN tb_categorias_tipo_servicio categoria_tipo_servicio ON tipos_servicio.categoria_tipo_servicio_id = categoria_tipo_servicio.categoria_tipo_servicio_id
                WHERE MONTH(servicios.fecha_servicio) = :mes
                AND YEAR(servicios.fecha_servicio) = :anio
            """
            
            parametros = {
                "mes": mes,
                "anio": anio
            }
            
            condiciones_adicionales = []
            
            if (tipo_servicio_prestado):
                condiciones_adicionales.append("tipos_servicio.tipo_servicio_prestado = :tipo_servicio_prestado")
                parametros["tipo_servicio_prestado"] = tipo_servicio_prestado
            
            if (condiciones_adicionales):
                consulta += " AND " + " AND ".join(condiciones_adicionales)
            
            consulta += " GROUP BY tipos_servicio.tipo_servicio_prestado, categoria_tipo_servicio.nombre_categoria "
            
            conteo_servicios_modelo = sesion.execute(text(consulta), parametros).yield_per(100)
            
            for conteo in conteo_servicios_modelo:
                yield conteo

    def obtener_conteo_tipos_servicios_realizados_por_rango_fecha(self, fecha_desde: date, fecha_hasta: date, tipo_servicio_prestado: Optional[str]) -> Generator[Tuple, None, None]:
        with self._bd.sesion() as sesion:
            
            consulta = """
                SELECT 
                    tipos_servicio.tipo_servicio_prestado,
                    categoria_tipo_servicio.nombre_categoria,
                    SUM(servicios.cantidad) AS total_servicios_realizados
                FROM tb_servicios servicios
                INNER JOIN tb_tipos_servicio tipos_servicio ON servicios.tipo_servicio_id = tipos_servicio.tipo_servicio_id
                INNER JOIN tb_categorias_tipo_servicio categoria_tipo_servicio ON tipos_servicio.categoria_tipo_servicio_id = categoria_tipo_servicio.categoria_tipo_servicio_id
                WHERE servicios.fecha_servicio BETWEEN :fecha_desde AND :fecha_hasta
            """
            
            parametros = {
                "fecha_desde": fecha_desde,
                "fecha_hasta": fecha_hasta
            }
            
            condiciones_adicionales = []
            
            if (tipo_servicio_prestado):
                condiciones_adicionales.append("tipos_servicio.tipo_servicio_prestado = :tipo_servicio_prestado")
                parametros["tipo_servicio_prestado"] = tipo_servicio_prestado
            
            if (condiciones_adicionales):
                consulta += " AND " + " AND ".join(condiciones_adicionales)
            
            consulta += " GROUP BY tipos_servicio.tipo_servicio_prestado, categoria_tipo_servicio.nombre_categoria "
            
            conteo_servicios_modelo = sesion.execute(text(consulta), parametros).yield_per(100)
            
            for conteo_servicio in conteo_servicios_modelo:
                yield conteo_servicio
    
    def obtener_conteo_tipos_servicios_realizados_por_anio(self, anio: str, tipo_servicio_prestado: Optional[str]) -> Generator[Tuple, None, None]:
        with self._bd.sesion() as sesion:
            anio = int(anio)
            
            consulta = """
                SELECT 
                    tipos_servicio.tipo_servicio_prestado,
                    categoria_tipo_servicio.nombre_categoria,
                    SUM(servicios.cantidad) AS total_servicios_realizados
                FROM tb_servicios servicios
                INNER JOIN tb_tipos_servicio tipos_servicio ON servicios.tipo_servicio_id = tipos_servicio.tipo_servicio_id
                INNER JOIN tb_categorias_tipo_servicio categoria_tipo_servicio ON tipos_servicio.categoria_tipo_servicio_id = categoria_tipo_servicio.categoria_tipo_servicio_id
                WHERE YEAR(servicios.fecha_servicio) = :anio
            """
            
            parametros = {"anio": anio}
            
            condiciones_adicionales = []
            
            if (tipo_servicio_prestado):
                condiciones_adicionales.append("tipos_servicio.tipo_servicio_prestado = :tipo_servicio_prestado")
                parametros["tipo_servicio_prestado"] = tipo_servicio_prestado
            
            if (condiciones_adicionales):
                consulta += " AND " + " AND ".join(condiciones_adicionales)
            
            consulta += " GROUP BY tipos_servicio.tipo_servicio_prestado, categoria_tipo_servicio.nombre_categoria "
            
            conteo_servicios_modelo = sesion.execute(text(consulta), parametros).yield_per(100)
            
            for conteo_servicio in conteo_servicios_modelo:
                yield conteo_servicio
    
    def obtener_conteo_servicios_x_departamento(self, mes_anio: str, tipo_servicio_prestado: Optional[str]) -> Generator[Tuple, None, None]:
        with self._bd.sesion() as sesion:
            mes, anio = mes_anio.split("-")
            mes = int(mes)
            anio = int(anio)
            
            consulta = """
                SELECT
                    nombre_departamento,
                    tipo_servicio_prestado,
                    SUM(cantidad) AS total_servicios_realizados
                FROM vw_servicios_prestados
                WHERE MONTH(fecha_servicio) = :mes
                AND YEAR(fecha_servicio) = :anio
            """
            parametros = {
                "mes": mes,
                "anio": anio
            }
            
            condiciones_adicionales = []
            
            if (tipo_servicio_prestado):
                condiciones_adicionales.append("tipo_servicio_prestado = :tipo_servicio_prestado")
                parametros["tipo_servicio_prestado"] = tipo_servicio_prestado
            
            if (condiciones_adicionales):
                consulta += " AND " + " AND ".join(condiciones_adicionales)
            
            consulta += " GROUP BY nombre_departamento, tipo_servicio_prestado"
            
            conteo_servicios_modelo = sesion.execute(text(consulta), parametros).yield_per(100)
            
            for conteo_servicio in conteo_servicios_modelo:
                yield conteo_servicio
    
    def obtener_conteo_servicios_x_departamento_por_rango_fecha(self, fecha_desde: date, fecha_hasta: date, tipo_servicio_prestado: Optional[str]) -> Generator[Tuple, None, None]:
        with self._bd.sesion() as sesion:
            consulta = """
                SELECT
                    nombre_departamento,
                    tipo_servicio_prestado,
                    SUM(cantidad) AS total_servicios_realizados
                FROM vw_servicios_prestados
                WHERE fecha_servicio BETWEEN :fecha_desde AND :fecha_hasta
            """
            parametros = {
                "fecha_desde": fecha_desde,
                "fecha_hasta": fecha_hasta
            }
            
            condiciones_adicionales = []
            
            if (tipo_servicio_prestado):
                condiciones_adicionales.append("tipo_servicio_prestado = :tipo_servicio_prestado")
                parametros["tipo_servicio_prestado"] = tipo_servicio_prestado
            
            if (condiciones_adicionales):
                consulta += " AND " + " AND ".join(condiciones_adicionales)
            
            consulta += " GROUP BY nombre_departamento, tipo_servicio_prestado"
            
            conteo_servicios_modelo = sesion.execute(text(consulta), parametros).yield_per(100)
            
            for conteo_servicio in conteo_servicios_modelo:
                yield conteo_servicio
    
    def obtener_conteo_servicios_x_departamento_por_anio(self, anio: str, tipo_servicio_prestado: Optional[str]) -> Generator[Tuple, None, None]:
        with self._bd.sesion() as sesion:
            anio = int(anio)
            
            consulta = """
                SELECT
                    nombre_departamento,
                    tipo_servicio_prestado,
                    SUM(cantidad) AS total_servicios_realizados
                FROM vw_servicios_prestados
                WHERE YEAR(fecha_servicio) = :anio
            """
            parametros = {"anio": anio}
            
            condiciones_adicionales = []
            
            if (tipo_servicio_prestado):
                condiciones_adicionales.append("tipo_servicio_prestado = :tipo_servicio_prestado")
                parametros["tipo_servicio_prestado"] = tipo_servicio_prestado
            
            if (condiciones_adicionales):
                consulta += " AND " + " AND ".join(condiciones_adicionales)
            
            consulta += " GROUP BY nombre_departamento, tipo_servicio_prestado"
            
            conteo_servicios_modelo = sesion.execute(text(consulta), parametros).yield_per(100)
            
            for conteo_servicio in conteo_servicios_modelo:
                yield conteo_servicio
    
    def obtener_conteo_agrupado_servicios_x_departamento(self, mes_anio: str, tipo_servicio_prestado: Optional[str]) -> Generator[Tuple, None, None]:
        with self._bd.sesion() as sesion:
            mes, anio = mes_anio.split("-")
            mes = int(mes)
            anio = int(anio)
            
            consulta = """
                SELECT
                    nombre_departamento,
                    SUM(cantidad) AS total_servicios_realizados
                FROM vw_servicios_prestados
                WHERE MONTH(fecha_servicio) = :mes
                AND YEAR(fecha_servicio) = :anio
            """
            parametros = {
                "mes": mes,
                "anio": anio
            }
            
            condiciones_adicionales = []
            
            if (tipo_servicio_prestado):
                condiciones_adicionales.append("tipo_servicio_prestado = :tipo_servicio_prestado")
                parametros["tipo_servicio_prestado"] = tipo_servicio_prestado
            
            if (condiciones_adicionales):
                consulta += " AND " + " AND ".join(condiciones_adicionales)
            
            consulta += " GROUP BY nombre_departamento ORDER BY total_servicios_realizados DESC "
            
            conteo_servicios_modelo = sesion.execute(text(consulta), parametros).yield_per(100)
            
            for conteo_servicio in conteo_servicios_modelo:
                yield conteo_servicio
    
    def obtener_conteo_agrupado_servicios_x_departamento_por_rango_fecha(self, fecha_desde: date, fecha_hasta: date, tipo_servicio_prestado: Optional[str]) -> Generator[Tuple, None, None]:
        with self._bd.sesion() as sesion:
            consulta = """
                SELECT
                    nombre_departamento,
                    SUM(cantidad) AS total_servicios_realizados
                FROM vw_servicios_prestados
                WHERE fecha_servicio BETWEEN :fecha_desde AND :fecha_hasta
            """
            parametros = {
                "fecha_desde": fecha_desde,
                "fecha_hasta": fecha_hasta
            }
            
            condiciones_adicionales = []
            
            if (tipo_servicio_prestado):
                condiciones_adicionales.append("tipo_servicio_prestado = :tipo_servicio_prestado")
                parametros["tipo_servicio_prestado"] = tipo_servicio_prestado
            
            if (condiciones_adicionales):
                consulta += " AND " + " AND ".join(condiciones_adicionales)
            
            consulta += " GROUP BY nombre_departamento ORDER BY total_servicios_realizados DESC "
            
            conteo_servicios_modelo = sesion.execute(text(consulta), parametros).yield_per(100)
            
            for conteo_servicio in conteo_servicios_modelo:
                yield conteo_servicio
    
    def obtener_conteo_agrupado_servicios_x_departamento_por_anio(self, anio: str, tipo_servicio_prestado: Optional[str]) -> Generator[Tuple, None, None]:
        with self._bd.sesion() as sesion:
            anio = int(anio)
            
            consulta = """
                SELECT
                    nombre_departamento,
                    SUM(cantidad) AS total_servicios_realizados
                FROM vw_servicios_prestados
                WHERE YEAR(fecha_servicio) = :anio
            """
            parametros = {"anio": anio}
            
            condiciones_adicionales = []
            
            if (tipo_servicio_prestado):
                condiciones_adicionales.append("tipo_servicio_prestado = :tipo_servicio_prestado")
                parametros["tipo_servicio_prestado"] = tipo_servicio_prestado
            
            if (condiciones_adicionales):
                consulta += " AND " + " AND ".join(condiciones_adicionales)
            
            consulta += " GROUP BY nombre_departamento ORDER BY total_servicios_realizados DESC "
            
            conteo_servicios_modelo = sesion.execute(text(consulta), parametros).yield_per(100)
            
            for conteo_servicio in conteo_servicios_modelo:
                yield conteo_servicio
    
    def actualizar(self, servicio: ServicioTecnicoModelo) -> None:
        with self._bd.sesion() as sesion:
            servicio_modelo = sesion.query(ServicioTecnicoModelo).filter_by(servicio_id = servicio.servicio_id).first()
            
            servicio_modelo.departamento_id = servicio.departamento_id
            servicio_modelo.fecha_servicio = servicio.fecha_servicio
            servicio_modelo.falla_presenta = servicio.falla_presenta
            servicio_modelo.tipo_servicio_id = servicio.tipo_servicio_id
            servicio_modelo.nombres_tecnicos = servicio.nombres_tecnicos
            servicio_modelo.cantidad = servicio.cantidad
            servicio_modelo.descripcion = servicio.descripcion
            servicio_modelo.observaciones_adicionales = servicio.observaciones_adicionales
    
    def eliminar(self, servicio: ServicioTecnicoModelo) -> None:
        with self._bd.sesion() as sesion:
            servicio_modelo = sesion.query(ServicioTecnicoModelo).filter_by(servicio_id = servicio.servicio_id).first()
            sesion.delete(servicio_modelo)