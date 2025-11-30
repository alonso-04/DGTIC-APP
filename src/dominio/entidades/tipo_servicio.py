from dataclasses import dataclass
from typing import Optional


@dataclass
class TipoServicio:
    tipo_servicio_prestado: str
    
    tipo_servicio_id: Optional[int] = None
    
    def _validar_campos(self):
        errores = []
        
        if (self._esta_vacio(self.tipo_servicio_prestado) or (self.tipo_servicio_prestado is None)):
            errores.append("Tipo de servicio: No puede estar vacío.")
        elif (len(self.tipo_servicio_prestado) > 120):
            errores.append("Tipo de servicio: No puede contener más de 120 caracteres.")
        
        return errores
    
    def _esta_vacio(self, campo: str) -> bool:
        if not (campo):
            return True
        elif (campo):
            campo_sin_espacios = campo.replace(" ", "")
            
            if (len(campo_sin_espacios) == 0):
                return True