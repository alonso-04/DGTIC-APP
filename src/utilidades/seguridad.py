import hashlib
from cryptography.fernet import Fernet


def hashear_contenido(contenido: str) -> str:
    """
    Genera un hash limitado estrictamente a 12 caracteres.
    Compatible con la columna String(12) y sistemas de 32/64 bits.
    """
    if contenido is None:
        return None
    
    # Limpieza rigurosa de entrada (evita problemas de buffers en Windows 7)
    texto_limpio = str(contenido).strip().replace('"', '').replace("'", "")
    
    # Generamos el hash MD5 plano nativo de Python
    hash_completo = hashlib.md5(texto_limpio.encode("utf-8")).hexdigest()
    
    # RECORTE ESTRICTO: Tomamos solo los primeros 12 caracteres
    hash_limitado = hash_completo[:12]
    
    return hash_limitado


def verificar_clave_usuario(clave_texto_plano: str, hash_almacenado: str) -> bool:
    """Verifica la contraseña limitando el hash ingresado a 12 caracteres."""
    if not clave_texto_plano or not hash_almacenado:
        return False
        
    try:
        # Hasheamos y recortamos la contraseña que viene del formulario de Login
        hash_nuevo = hashear_contenido(clave_texto_plano)
        
        # Comparación directa carácter por carácter de los 12 dígitos
        return hash_nuevo == hash_almacenado
    except Exception:
        return False

def cifrar_env():
    # 1. Generar una clave de cifrado
    key = Fernet.generate_key()
    print(f"Tu CLAVE SECRETA (guárdala bien): {key.decode()}")

    # 2. Leer el archivo .env original
    with open(".env", "rb") as env_file:
        datos_originales = env_file.read()

    # 3. Cifrar los datos
    f = Fernet(key)
    datos_cifrados = f.encrypt(datos_originales)

    # 4. Guardar los datos cifrados en un archivo ilegible
    with open(".env.enc", "wb") as enc_file:
        enc_file.write(datos_cifrados)

    print("¡Archivo .env.enc generado con éxito!")


if __name__ == "__main__":
    # clave_texto_plano = input("Ingrese su contraseña: ")
    # contenido_encriptado_string = hashear_contenido(clave_texto_plano)
    
    # print(contenido_encriptado_string)
    # print(type(contenido_encriptado_string))
    cifrar_env()