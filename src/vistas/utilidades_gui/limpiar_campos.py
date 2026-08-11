from typing import List
from PyQt5.QtWidgets import QSpinBox, QComboBox


def limpiar_campos(lista_campos_limpiar: List[object]) -> None:
    """
    Método para limpiar los campos de las diferentes ventanas del sistema, por ejemplo un servicio, departamento, tipo de servicio,
    categoría, etc. mediante el botón de limpiar en la ventana correspondiente.
    
    - lista_campos_limpiar: Es una lista que contiene los campos a limpiar.
    """
    
    for campo in lista_campos_limpiar:
        if isinstance(campo, QSpinBox):
            campo.setValue(1)
        elif not isinstance(campo, QComboBox):
            campo.clear()