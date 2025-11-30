import json
from dominio.excepciones import UsuarioValidacionError
from aplicacion.unidad_trabajo.unidad_trabajo_base import UnidadTrabajo
from aplicacion.unidad_trabajo.sqlalchemy_unidad_trabajo import SQLAlchemyUnidadTrabajo
from typing import Optional, Dict
from configuraciones.rutas import obtener_ruta_sesion_json

RUTA_SESION_JSON = obtener_ruta_sesion_json()


class SesionUsuario:
    def __init__(self, unidad_trabajo: UnidadTrabajo):
        self.unidad_trabajo = unidad_trabajo
    
    def iniciar_sesion(self, nombre_usuario: str, clave_usuario: str) -> Optional[Dict]:
        with self.unidad_trabajo() as unidad_trabajo:
            try:
                errores = []
                
                usuario_id = unidad_trabajo.usuario.autenticar_usuario(nombre_usuario, clave_usuario)
                
                if not(usuario_id):
                    errores.append("El usuario y/o contraseña son incorrectos.")
                
                if (errores):
                    raise UsuarioValidacionError(errores)
                
                return usuario_id
            except UsuarioValidacionError as error:
                raise error
    
    def cargar_sesion(self, nombre_usuario: str, clave_usuario) -> None:
        usuario_id_autenticado = self.iniciar_sesion(nombre_usuario, clave_usuario)
        
        if (usuario_id_autenticado):
            with open(RUTA_SESION_JSON, "w") as sesion_usuario_json:
                json.dump(usuario_id_autenticado, sesion_usuario_json, indent = 4)
    
    def cerrar_sesion(self) -> None:
        try:
            with open(RUTA_SESION_JSON, "r") as sesion_usuario_json:
                data = json.load(sesion_usuario_json)
                
                if ("usuario_id" in data):
                    data["usuario_id"] = None
                else:
                    print("Clave 'usuario_id' no encontrada en el JSON.")
                    return
                
                with open(RUTA_SESION_JSON, "w") as sesion_usuario_json:
                    json.dump(data, sesion_usuario_json, indent = 4)
        except FileNotFoundError as error:
            raise error
        except json.JSONDecodeError as error:
            raise error


if __name__ == "__main__":
    try:
        unidad_trabajo = SQLAlchemyUnidadTrabajo()
        sesion_usuario = SesionUsuario(unidad_trabajo)
        
        nombre_usuario = "alonso124"
        clave_usuario = "1234"
        
        usuario_id = sesion_usuario.iniciar_sesion(nombre_usuario, clave_usuario)
        
        if (usuario_id):
            sesion_usuario.cargar_sesion(nombre_usuario, clave_usuario)
            print("Se inició sesión correctamente.")
        
        #sesion_usuario.cerrar_sesion()
        #print("Se cerró la sesión correctamente.")
    except UsuarioValidacionError as error:
        print("\n".join(error.errores))
    except FileNotFoundError:
        print("ERROR: EL ARCHIVO no se encontró.")
    except json.JSONDecodeError:
        print("ERROR: NO SE PUDO DECODIFICAR EL ARCHIVO JSON.")
    except Exception as error:
        print(error)