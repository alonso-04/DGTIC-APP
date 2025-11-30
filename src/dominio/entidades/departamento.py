from dataclasses import dataclass
from typing import Optional


@dataclass
class Departamento:
    nombre_departamento: str
    
    departamento_id: Optional[int] = None
    
    def _validar_campos(self):
        errores = []
        
        # Validando el nombre del departamento
        if (self._esta_vacio(self.nombre_departamento) or (self.nombre_departamento is None)):
            errores.append("Nombre del Departamento: No puede estar vacío.")
        elif (len(self.nombre_departamento) > 120):
            errores.append("Nombre del Departamento: No puede contener más de 120 caracteres.")
        
        # Retornando las validaciones del Departamento
        return errores
    
    def _esta_vacio(self, campo: str) -> bool:
        if not (campo):
            return True
        elif (campo):
            campo_sin_espacios = campo.replace(" ", "")
            
            if (len(campo_sin_espacios) == 0):
                return True