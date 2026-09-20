import os
from configuraciones.conexion import bd
from modelos.rol_modelo import RolModelo
from modelos.usuario_modelo import UsuarioModelo
from utilidades.seguridad import hashear_contenido


def inicializar_usuario_admin_bd():
    try:
        with bd.sesion() as sesion:
            
            # 1. VERIFICAR E INICIALIZAR LOS ROLES POR DEFECTO
            # Contamos cuántos roles existen en la base de datos
            contador_roles = sesion.query(RolModelo).count()
            
            if contador_roles == 0:
                print("La tabla de roles está vacía. Insertando roles por defecto...")
                
                rol_admin = RolModelo(rol_id=1, tipo_rol="ADMINISTRADOR")
                rol_estandar = RolModelo(rol_id=2, tipo_rol="ESTANDAR")
                
                # Agregamos ambos roles a la sesión
                sesion.add_all([rol_admin, rol_estandar])
                
                # Forzamos el guardado intermedio para que los IDs estén disponibles
                sesion.flush() 
                print("Roles 'ADMINISTRADOR' y 'ESTANDAR' creados correctamente.")
            
            # 2. VERIFICAR E INICIALIZAR EL USUARIO ADMINISTRADOR
            contador_usuarios = sesion.query(UsuarioModelo).count()
            
            if contador_usuarios == 0:
                NOMBRE_USUARIO_ADMIN_DEFECTO = os.getenv("NOMBRE_USUARIO_ADMIN_DEFECTO")
                CLAVE_USUARIO_ADMIN_DEFECTO = os.getenv("CLAVE_USUARIO_ADMIN_DEFECTO")
                
                if not NOMBRE_USUARIO_ADMIN_DEFECTO or not CLAVE_USUARIO_ADMIN_DEFECTO:
                    print("ERROR: No se pudieron leer las variables de entorno para el usuario admin.")
                    return
                
                # Generar el hash de la contraseña utilizando tu función existente
                CLAVE_USUARIO_ADMIN_HASHEADA = hashear_contenido(CLAVE_USUARIO_ADMIN_DEFECTO)
                
                # Creamos la instancia del objeto utilizando el modelo de SQLAlchemy
                nuevo_admin = UsuarioModelo(
                    usuario_id=1,
                    rol_id=1,
                    nombre_usuario=NOMBRE_USUARIO_ADMIN_DEFECTO,
                    clave_usuario=CLAVE_USUARIO_ADMIN_HASHEADA
                )
                
                sesion.add(nuevo_admin)
    except Exception as error:
        raise error