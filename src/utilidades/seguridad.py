import bcrypt
from cryptography.fernet import Fernet


def hashear_contenido(contenido: str) -> str:
    if (contenido is None):
        return None
    
    contenido_codificado = contenido.encode("utf-8")
    salt = bcrypt.gensalt()
    contenido_encriptado = bcrypt.hashpw(contenido_codificado, salt)
    contenido_encriptado_string = contenido_encriptado.decode("utf-8")
    
    return contenido_encriptado_string

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