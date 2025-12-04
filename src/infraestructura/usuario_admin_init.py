import os
import mysql.connector
from utilidades.hasher import hashear_contenido


def inicializar_usuario_admin_bd():
    conexion = None
    cursor = None
    
    try:
        conexion = mysql.connector.connect(
            host = os.getenv("HOST_BD"),
            user = os.getenv("NOMBRE_USUARIO_BD"),
            password = os.getenv("CLAVE_USUARIO_BD"),
            database = os.getenv("NOMBRE_BD")
        )
        
        if not(conexion.is_connected()):
            print("NO SE PUDO REALIZAR LA CONEXIÓN A LA BASE DE DATOS.")
            return
        
        cursor = conexion.cursor()
        
        # VERIFICAR SI HAY USUARIOS EN LA BASE DE DATOS
        cursor.execute("SELECT COUNT(*) FROM tb_usuarios;")
        (contador_usuarios,) = cursor.fetchone()
        
        if (contador_usuarios == 0):
            # LEER LAS CREDENCIALES DIRECTAMENTE DE LAS VARIABLES DE ENTORNO
            NOMBRE_USUARIO_ADMIN_DEFECTO = os.getenv("NOMBRE_USUARIO_ADMIN_DEFECTO")
            CLAVE_USUARIO_ADMIN_DEFECTO = os.getenv("CLAVE_USUARIO_ADMIN_DEFECTO")
            
            if (not(NOMBRE_USUARIO_ADMIN_DEFECTO) or not(CLAVE_USUARIO_ADMIN_DEFECTO)):
                print("NO SE PUDIERON LEER LAS VARIABLES DE ENTORNO")
                return
            
            # GENERAR EL HASH Y GUARDAR
            CLAVE_USUARIO_ADMIN_HASHEADA = hashear_contenido(CLAVE_USUARIO_ADMIN_DEFECTO)
            
            cursor.execute("""
                INSERT INTO tb_usuarios(usuario_id, rol_id, nombre_usuario, clave_usuario)
                VALUES (%s, %s, %s, %s);
            """, (1, 1, NOMBRE_USUARIO_ADMIN_DEFECTO, CLAVE_USUARIO_ADMIN_HASHEADA))
            
            conexion.commit()
            
            print(f"Usuario administrador '{NOMBRE_USUARIO_ADMIN_DEFECTO}' creado exitosamente.")
    except Exception as error:
        if (conexion):
            conexion.rollback()
            print(f"ERROR AL CREAR EL USUARIO ADMINISTRADOR: {error}")
    finally:
        if (cursor):
            cursor.close()
            
        if (conexion and conexion.is_connected()):
            conexion.close()