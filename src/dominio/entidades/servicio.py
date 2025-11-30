from dataclasses import dataclass
from typing import Optional
from datetime import date


@dataclass
class Servicio:
    fecha_servicio: date
    falla_presenta: str
    nombres_tecnicos: str
    observaciones_adicionales: str
    
    departamento_id: Optional[int] = None
    tipo_servicio_id: Optional[int] = None
    servicio_id: Optional[int] = None
    
    def _validar_campos(self):
        errores = []
        
        # Validando el campo de falla que presenta
        if (self._esta_vacio(self.falla_presenta) or (self.falla_presenta is None)):
            errores.append("Falla que presenta: No puede estar vacío.")
        elif (len(self.falla_presenta) > 150):
            errores.append("Falla que presenta: No puede contener más de 150 caracteres.")
        
        
        # Validando el campo de nombres de los técnicos
        if (self._esta_vacio(self.nombres_tecnicos) or (self.nombres_tecnicos is None)):
            errores.append("Nombre del técnico: No puede estar vacío.")
        elif (len(self.nombres_tecnicos) > 250):
            errores.append("Nombre del técnico: No puede contener más de 250 caracteres.")
        
        # Validando el campo de observaciones adicionales
        if not(self._esta_vacio(self.observaciones_adicionales)):
            if (len(self.observaciones_adicionales) > 255):
                errores.append("Observaciones adicionales: No puede contener más de 255 caracteres.")
        
        
        # Validando el campo de departamento_id
        if not (self.departamento_id):
            errores.append("Departamento: Debe elegir un departamento.")
        
        
        # Validando el campo de tipo_servicio_id
        if not(self.tipo_servicio_id):
            errores.append("Tipo de servicio: Debe elegir un tipo de servicio.")
        
        
        # Retornar las validaciones de Sevicio
        return errores
    
    def _esta_vacio(self, campo: str) -> bool:
        if not (campo):
            return True
        elif (campo):
            campo_sin_espacios = campo.replace(" ", "")
            
            if (len(campo_sin_espacios) == 0):
                return True