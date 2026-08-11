from datetime import date
from typing import List, Tuple, Dict
from PyQt5.QtWidgets import QLineEdit, QDateEdit
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QColor


def obtener_modelo_datos_y_data(
    servicio_filtrar,
    nombres_labels: List[str],
    nombres_columnas: List[str],
    lista_campos_filtrar: List[Tuple[object, str]] = None,
    filas_resaltadas: Dict[object, QColor] = None
) -> List:
    """
    Método para poder filtrar los registros de las diferentes ventanas del sistema, por ejemplo un servicio, departamento, tipo de servicio,
    categoría, etc. mediante el botón de filtrar en la ventana correspondiente.
    
    - servicio_filtrar: Es la capa con acceso a los métodos de filtrar un servicio, departamento, tipo de servicio, categoría, etc.
    - lista_campos_filtrar: Es una lista de tuplas que contiene los campos a filtrar y el nombre de la columna correspondiente en la base de datos.
    - nombres_labels: Es una lista que contiene los nombres de las columnas que se van a mostrar en la tabla.
    - nombres_columnas: Es una lista que contiene los nombres de las columnas en la bd.
    - filas_resaltadas: Es un diccionario que contiene el nombre de la columna y el color que se va a utilizar para resaltar las filas.
    """
    
    if lista_campos_filtrar:
        criterios_filtro = {}
            
        for campo, columna in lista_campos_filtrar:
            if isinstance(campo, QLineEdit):
                criterios_filtro[columna] = campo.text().upper()
            elif isinstance(campo, QDateEdit):
                criterios_filtro[columna] = campo.date().toPyDate()
            
        registros = servicio_filtrar(**criterios_filtro)
    else:
        registros = servicio_filtrar()
    
    NUMERO_FILAS = len(registros)
    NUMERO_COLUMNAS = len(nombres_labels)
    
    modelo_datos = QStandardItemModel(NUMERO_FILAS, NUMERO_COLUMNAS)
    modelo_datos.setHorizontalHeaderLabels(nombres_labels)
    color_resaltar = filas_resaltadas.get("color") if filas_resaltadas else None
    
    for fila, registro in enumerate(registros):
        es_fila_resaltada = False
        if filas_resaltadas:
            campo_evaluar = filas_resaltadas.get("nombre_columna")
            if getattr(registro, campo_evaluar, None):
                es_fila_resaltada = True
        
        for columna, nombre_columna in enumerate(nombres_columnas):
            valor = getattr(registro, nombre_columna, "")
            
            if valor is None:
                valor = ""
            elif isinstance(valor, date):
                valor = valor.strftime("%d-%m-%Y")
            
            item = QStandardItem(str(valor))
            
            if es_fila_resaltada and color_resaltar:
                item.setBackground(color_resaltar)
            
            modelo_datos.setItem(fila, columna, item)
    
    return modelo_datos, registros