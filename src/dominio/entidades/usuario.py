import re
from dataclasses import dataclass
from typing import Optional


@dataclass
class Usuario:
    nombre_usuario: str
    clave_usuario: str
    
    rol_id: Optional[int] = None
    usuario_id: Optional[int] = None

    def _validar_campos(self):
        errores = []
        
        # Validando el nombre de usuario
        if (self._esta_vacio(self.nombre_usuario) or (self.nombre_usuario is None)):
            errores.append("Nombre de usuario: No puede estar vacío.")
        elif (len(self.nombre_usuario) > 12):
            errores.append("Nombre de usuario: No puede contener más de 12 caracteres.")
        
        if (self._contiene_espacios(self.nombre_usuario)):
            errores.append("Nombre de usuario: No puede contener espacios.")
        
        
        # Validando la clave de usuario
        if (self._esta_vacio(self.clave_usuario) or (self.clave_usuario is None)):
            errores.append("Contraseña: No puede estar vacío.")
        
        if (self._contiene_espacios(self.clave_usuario)):
            errores.append("Contraseña: No puede contener espacios.")
        
        
        # Validando el rol a asignar
        if not (self.rol_id):
            errores.append("Rol: Debe asignarle un rol al usuario.")
        
        # Retornando las validaciones del Usuario
        return errores
    
    def _esta_vacio(self, campo: str) -> bool:
        if not (campo):
            return True
        elif (campo):
            campo_sin_espacios = campo.replace(" ", "")
            
            if (len(campo_sin_espacios) == 0):
                return True
    
    def _contiene_espacios(self, campo: str) -> bool:
        if not(isinstance(campo, str)):
            return False
        
        return re.search(r"\s", campo)