import os
from mysql import connector
from pathlib import Path
from infraestructura.conexiones.respaldo_base import RespaldoBase
from datetime import datetime, date
from configuraciones.rutas import obtener_ruta_respaldos_bd


TABLAS_RESPALDO = ["tb_departamentos", "tb_tipos_servicio", "tb_servicios"]
ORDEN_TABLAS_LIMPIAR = ["tb_servicios", "tb_tipos_servicio", "tb_departamentos"]

def _obtener_parametros_conexion_mysql():
    NOMBRE_USUARIO_BD = os.getenv('NOMBRE_USUARIO_BD')
    CLAVE_USUARIO_BD = os.getenv('CLAVE_USUARIO_BD')
    HOST_BD = os.getenv('HOST_BD')
    PUERTO_BD = os.getenv('PUERTO_BD', '3306')
    NOMBRE_BD = os.getenv('NOMBRE_BD')
    
    if not all([NOMBRE_USUARIO_BD, CLAVE_USUARIO_BD, HOST_BD, NOMBRE_BD]):
        raise ValueError("FALTAN LAS VARIABLES DE ENTORNO: NOMBRE_USUARIO_BD, CLAVE_USUARIO_BD, HOST_BD O NOMBRE_BD")
    
    return {
        "user": NOMBRE_USUARIO_BD,
        "password": CLAVE_USUARIO_BD,
        "host": HOST_BD,
        "port": PUERTO_BD,
        "database": NOMBRE_BD,
        "charset": "utf8mb4"
    }


class RespaldoLocal(RespaldoBase):
    def _obtener_conexion_bd(self):
        try:
            parametros = _obtener_parametros_conexion_mysql()
            return connector.connect(**parametros)
        except Exception as error:
            raise Exception(f"ERROR AL CONECTARSE A LA BASE DE DATOS. VERIFIQUE LAS CREDENCIALES. ERROR: {error}")
    
    def exportar(self):
        DIRECTORIO_RESPALDOS_BD = obtener_ruta_respaldos_bd()
        fecha_actual = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        respaldo = f"{DIRECTORIO_RESPALDOS_BD}/backup_informatica_{fecha_actual}.sql"
        
        conexion = None
        cursor = None
        
        try:
            conexion = self._obtener_conexion_bd()
            cursor = conexion.cursor()
            
            with open(respaldo, "w", encoding = "utf-8") as archivo:
                
                # EXPORTAR LOS DATOS (INSERT INTO) DE LAS TABLAS A RESPALDAR
                for tabla in TABLAS_RESPALDO:
                    cursor.execute(f"SELECT * FROM `{tabla}`")
                    
                    # NOMBRE DE LAS COLUMNAS PARA EL INSERT
                    nombre_columnas = [descripcion[0] for descripcion in cursor.description]
                    
                    for fila in cursor.fetchall():
                        
                        # --- CÓDIGO DIRECTO Y CORREGIDO ---
                        valores_listos = []
                        for valor in fila:
                            if valor is None:
                                valores_listos.append('NULL')

                            elif isinstance(valor, (datetime, date)):
                                # ✅ Asegura formato de fecha (comillas necesarias)
                                valores_listos.append(f"'{valor.strftime('%Y-%m-%d')}'")

                            elif isinstance(valor, (int, float)):
                                # ✅ Los números se insertan sin comillas
                                valores_listos.append(str(valor))

                            else:
                                # ✅ Manejar texto, bytes y otros tipos
                                if isinstance(valor, bytes):
                                    valor_str = valor.decode("utf-8", errors="replace")
                                else:
                                    valor_str = str(valor)

                                # Escapar comillas simples
                                valor_escapado = valor_str.replace("'", "''")
                                valores_listos.append(f"'{valor_escapado}'")
                        
                        valores = ", ".join(valores_listos)
                        insersion_fila = f"INSERT IGNORE INTO `{tabla}` ({', '.join(nombre_columnas)}) VALUES ({valores});"
                        archivo.write(f"{insersion_fila}\n")
                    
                    archivo.write("\n")
            
            return respaldo
        except Exception as error:
            raise error
        finally:
            if (cursor):
                cursor.close()
            if (conexion):
                conexion.close()
    
    def importar(self, ruta_origen: Path):
        conexion = None
        cursor = None
        
        try:
            conexion = self._obtener_conexion_bd()
            cursor = conexion.cursor()
            
            with open(ruta_origen, "r", encoding="utf-8") as archivo:
                comando_actual = ""
                for linea in archivo:
                    linea = linea.strip()

                    # Ignorar comentarios y líneas vacías
                    if not linea or linea.startswith("--") or linea.startswith("/*"):
                        continue
                    
                    comando_actual += linea + " "

                    # Ejecutar si hay punto y coma al final
                    if linea.endswith(";"):
                        try:
                            cursor.execute(comando_actual.strip())
                            conexion.commit()
                        except Exception as error:
                            conexion.rollback()
                            raise error
                        
                        comando_actual = ""  # Reiniciar el buffer
                
                conexion.commit()
                print(f"Importación desde {ruta_origen} completada.")
        except Exception as error:
            if (conexion):
                conexion.rollback()
            print(f"ERROR AL IMPORTAR LA BASE DE DATOS: {error}")
            raise error
        finally:
            if (conexion):
                conexion.close()


if __name__ == "__main__":
    try:
        respaldo_local = RespaldoLocal()
        
        respaldo = respaldo_local.exportar()
        #print(f"Se exportó el respaldo correctamente en: {respaldo}")
        
        #respaldo_local.importar(Path(r"C:\\Users\\Hp\\Documents\\RESPALDOS_BD\\backup_informatica_2025-11-08_09-03-53.sql"))
    except Exception as error:
        print(error)