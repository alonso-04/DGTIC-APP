from typing import List
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QCompleter


def cargar_completer(servicio, lista_campos: List, nombre_entidad: str) -> None:
    """
    Método para poder cargar los QCompleter dentro de las diferentes ventanas
    del sistema, por ejemplo el listado sugerido de departamentos,
    tipos de servicio y categorías que vayan apareciendo mediante
    escribamos en el campo de texto
    
    - servicio: Es una variable que contiene el servicio al cual consultar su método de **obtener_todos()** y poder acceder a la posición 1 que en todas las consultas sería donde va el nombre ya sea de un departamento, tipo de servicio o categoría.
    - lista_campos: Una lista que contiene los campos que se les va a setear el QCompleter del listado sugerido mientras se está escribiendo.
    - nombre_entidad: Es un string que contiene el nombre de la entidad que se está consultando, por ejemplo "departamento", "tipo de servicio" o "categoría".
    """
    
    lista_modelos = servicio.obtener_todos()
    
    if not lista_modelos:
        QCompleter([])
        return
    
    columnas = lista_modelos[0].__table__.columns.keys()
    lista_elementos = [tuple(getattr(modelo, columna) for columna in columnas) for modelo in lista_modelos]
    
    if nombre_entidad == "departamento" or nombre_entidad == "categoria":
        nombres_elementos = [str(elemento[1]) for elemento in lista_elementos]
    else:
        nombres_elementos = [str(elemento[2]) for elemento in lista_elementos]
    
    completer = QCompleter(nombres_elementos)
    completer.setCaseSensitivity(Qt.CaseInsensitive)
    completer.setFilterMode(Qt.MatchContains)
    completer.setCompletionMode(QCompleter.PopupCompletion)
    
    for campo in lista_campos:
        campo.setCompleter(completer)