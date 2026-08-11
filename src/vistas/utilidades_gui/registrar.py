from typing import List, Tuple
from PyQt5.QtWidgets import (
    QLineEdit, QTextEdit, QPlainTextEdit, 
    QSpinBox, QDateEdit, QComboBox
)


def registrar_campos(
    servicio,
    lista_campos_registrar: List[Tuple[object, str]]
) -> None:
    """
    Método para poder registrar los campos de las diferentes ventanas del sistema, por ejemplo un servicio, departamento, tipo de servicio,
    categoría, etc. mediante el botón de registrar en la ventana correspondiente.
    
    - servicio: Es la capa con acceso a los métodos de registrar un servicio, departamento, tipo de servicio, categoría, etc.
    - lista_campos_registrar: Es una lista de tuplas que contiene los campos a registrar y el nombre de la columna correspondiente en la base de datos.
    """
    
    datos_a_registrar = {}
    
    for campo, columna in lista_campos_registrar:
        if isinstance(campo, QLineEdit):
            datos_a_registrar[columna] = campo.text().upper()
        elif isinstance(campo, QTextEdit) or isinstance(campo, QPlainTextEdit):
            datos_a_registrar[columna] = campo.toPlainText().upper()
        elif isinstance(campo, QSpinBox):
            datos_a_registrar[columna] = campo.value()
        elif isinstance(campo, QDateEdit):
            datos_a_registrar[columna] = campo.date().toPyDate()
        elif isinstance(campo, QComboBox):
            datos_a_registrar[columna] = campo.currentText()
    
    servicio.registrar(**datos_a_registrar)