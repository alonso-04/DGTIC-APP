import os
from contextlib import contextmanager
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import create_engine, text
from sqlalchemy.orm import declarative_base
from sqlalchemy_utils import database_exists, create_database


Base = declarative_base()


class MySQLBaseDatos:
    def __init__(self):
        self._motor_bd = None
        self._fabrica_sesiones = None
    
    def inicializar_conexion(self):
        if self._motor_bd is not None:
            return
        
        URL_BASE_DATOS_MYSQL = (
            f"mysql+pymysql://"
            f"{os.environ.get('NOMBRE_USUARIO_BD')}:"
            f"{os.environ.get('CLAVE_USUARIO_BD')}@"
            f"{os.environ.get('HOST_BD')}:"
            f"{os.environ.get('PUERTO_BD', '3306')}/"
            f"{os.environ.get('NOMBRE_BD')}"
        )
        
        try:
            if not database_exists(URL_BASE_DATOS_MYSQL):
                create_database(URL_BASE_DATOS_MYSQL)
                print(f"¡Base de datos '{os.environ.get('NOMBRE_BD')}' creada exitosamente!")
            
            self._motor_bd = create_engine(
                URL_BASE_DATOS_MYSQL,
                pool_size = 10,
                max_overflow = 20,
                pool_timeout = 30,
                pool_recycle = 1800
            )
            
            self._fabrica_sesiones = sessionmaker(
                autocommit = False,
                autoflush = False,
                bind = self._motor_bd,
                expire_on_commit = False
            
            )
            
            print(f"Motor de base de datos MySQL creado y conectado a: {os.environ.get('HOST_BD')}/{os.environ.get('NOMBRE_BD')}")
            
            # Para que el Base no esté vacío al intentar crear las tablas, vistas, etc.
            import modelos
            
            # Crear las tablas del esquema
            Base.metadata.create_all(self._motor_bd)
            print("Verificación de tablas completada (se crean solo si no existen).")
            
            try:
                # Crear vista si no existe
                QUERY_VISTA = """
                CREATE VIEW IF NOT EXISTS vw_servicios_prestados AS
                    SELECT
                        servicios.servicio_id,
                        departamentos.departamento_id,
                        tipos_servicio.tipo_servicio_id,
                        departamentos.nombre_departamento,
                        servicios.fecha_servicio,
                        servicios.falla_presenta,
                        tipos_servicio.tipo_servicio_prestado,
                        servicios.nombres_tecnicos,
                        servicios.descripcion,
                        servicios.cantidad,
                        servicios.observaciones_adicionales,
                        comunas.nombre_comuna
                    FROM tb_servicios AS servicios
                    INNER JOIN tb_departamentos AS departamentos ON servicios.departamento_id = departamentos.departamento_id
                    INNER JOIN tb_tipos_servicio AS tipos_servicio ON servicios.tipo_servicio_id = tipos_servicio.tipo_servicio_id
                    INNER JOIN tb_comunas AS comunas ON servicios.comuna_id = comunas.comuna_id;
                """
                
                # Ejecutamos el SQL plano directamente sobre el motor de SQLAlchemy
                with self._motor_bd.connect() as conexion_sql:
                    conexion_sql.execute(text(QUERY_VISTA))
                    conexion_sql.commit() 
                    
                print("Verificación de vista completada (creada o ya existente).")
                
            except Exception as error_vista:
                print(f"Advertencia al crear la vista: {error_vista}")
        except Exception as error:
            print(f"ERROR AL CREAR EL MOTOR DE LA BASE DE DATOS: {error}")
            self._motor_bd = None
            self._fabrica_sesiones = None
    
    def obtener_fabrica_sesiones(self) -> sessionmaker:
        if not (self._fabrica_sesiones):
            raise Exception("No se ha podido inicializar la base de datos")
        
        return self._fabrica_sesiones
    
    def crear_sesion(self) -> Session:
        if not (self._fabrica_sesiones):
            raise Exception("No se ha podido inicializar la base de datos")
        
        return self._fabrica_sesiones()
    
    def obtener_base_declarativa(self) -> declarative_base:
        return Base
    
    @contextmanager
    def sesion(self):
        sesion = self.crear_sesion()
        try:
            yield sesion
            sesion.commit()
        except Exception:
            sesion.rollback()
            raise
        finally:
            sesion.close()

bd = MySQLBaseDatos()

if __name__ == "__main__":
    try:
        bd.crear_sesion()
        print("se creo la sesión correctamente")
    except Exception as error:
        print(f"ERROR AL CREAR LA SESIÓN")