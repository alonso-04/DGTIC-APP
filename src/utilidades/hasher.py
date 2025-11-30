import bcrypt


def hashear_contenido(contenido: str) -> str:
    if (contenido is None):
        return None
    
    contenido_codificado = contenido.encode("utf-8")
    salt = bcrypt.gensalt()
    contenido_encriptado = bcrypt.hashpw(contenido_codificado, salt)
    contenido_encriptado_string = contenido_encriptado.decode("utf-8")
    
    return contenido_encriptado_string


if __name__ == "__main__":
    clave_texto_plano = input("Ingrese su contraseña: ")
    contenido_encriptado_string = hashear_contenido(clave_texto_plano)
    
    print(contenido_encriptado_string)
    print(type(contenido_encriptado_string))