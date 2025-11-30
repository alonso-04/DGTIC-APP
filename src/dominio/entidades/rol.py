from dataclasses import dataclass
from typing import Optional


@dataclass
class Rol:
    tipo_rol: str
    
    rol_id: Optional[int] = None
    
    def _validar_campos(self):
        errores = []
        
        # Validando el tipo de rol
        if (self._esta_vacio(self.tipo_rol) or (self.tipo_rol is None)):
            errores.append("Rol: No puede estar vacío.")
        elif (len(self.tipo_rol) > 15):
            errores.append("Rol: No puede contener más de 15 caracteres.")
        
        # Retornando las validaciones del Rol
        return errores
    
    def _esta_vacio(self, campo: str) -> bool:
        if not (campo):
            return True
        elif (campo):
            campo_sin_espacios = campo.replace(" ", "")
            
            if (len(campo_sin_espacios) == 0):
                return True