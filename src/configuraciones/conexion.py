import os
from contextlib import contextmanager
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from dotenv import load_dotenv

load_dotenv()

URL_BASE_DATOS_MYSQL = (
    f"mysql+pymysql://"
    f"{os.environ.get('NOMBRE_USUARIO_BD')}:"
    f"{os.environ.get('CLAVE_USUARIO_BD')}@"
    f"{os.environ.get('HOST_BD')}:"
    f"{os.environ.get('PUERTO_BD', '3306')}/"
    f"{os.environ.get('NOMBRE_BD')}"
)

Base = declarative_base()


class MySQLBaseDatos:
    def __init__(self, URL_BASE_DATOS: str = URL_BASE_DATOS_MYSQL):
        try:
            self._motor_bd = create_engine(
                URL_BASE_DATOS,
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