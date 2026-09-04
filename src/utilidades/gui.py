import os
import sys
from typing import List, Dict, Tuple
from functools import reduce
from datetime import date
from PyQt5 import uic
from PyQt5.QtCore import Qt

from PyQt5.QtWidgets import (
    QMessageBox,
    QTableView,
    QAbstractItemView,
    QHBoxLayout,
    QCompleter,
    QLineEdit,
    QDateEdit,
    QComboBox,
    QSpinBox,
    QPlainTextEdit,
    QTextEdit
)

from PyQt5.QtGui import QIcon, QColor, QStandardItemModel, QStandardItem

from configuraciones.rutas import RUTA_BASE, obtener_ruta_icono_app, obtener_ruta_manual_usuario
from componentes.boton_acciones import BotonAcciones


# CLASE PARA LA INTERFAZ BASE DE TODAS LAS VENTANAS
class UiBase:
    def __init__(self, nombre_archivo_ui: str = None, nombre_archivo_estilos: str = None):
        self.ui = self._cargar_ui(nombre_archivo_ui)
        self.cargar_estilos(nombre_archivo_estilos)
    
    def abrir(self):
        self.ui.show()
    
    def _cargar_ui(self, nombre_archivo_ui: str):
        try:
            if not nombre_archivo_ui:
                return
            
            ruta_ui = os.path.abspath(os.path.join(RUTA_BASE, "vistas", "vistas_qt", nombre_archivo_ui))
            ui_cargada = uic.loadUi(ruta_ui, None)
            return ui_cargada
        except FileNotFoundError:
            self.mostrar_mensaje_error(f"Error: No se encontró el archivo: {ruta_ui}")
            sys.exit(1)
    
    def _cargar_icono_app(self):
        ruta_icono_app = obtener_ruta_icono_app()
        self.ui.setWindowIcon(QIcon(ruta_icono_app))
    
    def cargar_estilos(self, nombre_archivo_estilos: str, pagina_stacked_widget: object = None):
        try:
            if not nombre_archivo_estilos:
                return
            
            ruta_estilos = os.path.abspath(os.path.join(RUTA_BASE, "recursos", "estilos", nombre_archivo_estilos))
            
            with open(ruta_estilos, "r", encoding="utf-8") as archivo:
                if not pagina_stacked_widget:
                    self.ui.setStyleSheet(archivo.read())
                else:
                    pagina_stacked_widget.setStyleSheet(archivo.read())
            
            ruta_icono_app = obtener_ruta_icono_app()
            self.ui.setWindowIcon(QIcon(ruta_icono_app))
        except FileNotFoundError:
            self.mostrar_mensaje_error(f"Error: No se encontró el archivo: {ruta_estilos}")
            sys.exit(1)
    
    def cargar_botones(self):
        ruta_estilos_boton = os.path.abspath(os.path.join(RUTA_BASE, "recursos", "estilos", "estilos_botones_acciones.qss"))
        
        self.btn_actualizar = BotonAcciones("Actualizar", "actualizar", ruta_estilos_boton)
        self.btn_eliminar = BotonAcciones("Eliminar", "eliminar", ruta_estilos_boton)
        self.btn_cancelar = BotonAcciones("Cancelar", "cancelar", ruta_estilos_boton)
        
        layout_botones = QHBoxLayout()
        
        layout_botones.addWidget(self.btn_actualizar)
        layout_botones.addWidget(self.btn_eliminar)
        layout_botones.addWidget(self.btn_cancelar)
        
        self.ui.layout_principal.addLayout(layout_botones)
    
    def configurar_tabla(self, tabla: QTableView):
        # SELECCIÓN DE FILA COMPLETA E INDIVIDUAL
        tabla.setSelectionBehavior(self.ui.tabla_servicios.SelectRows)
        tabla.setSelectionMode(self.ui.tabla_servicios.SingleSelection)
        
        # DESACTIVAR LA EDICIÓN DE CELDAS AL HACER DOBLE CLICK
        tabla.setEditTriggers(QAbstractItemView.NoEditTriggers)
        
        # OCULTAR LOS NÚMEROS DE FILA DE LA TABLA
        cabecera_vertical = tabla.verticalHeader()
        cabecera_vertical.setVisible(False)
    
    def mostrar_mensaje_error(self, mensaje: str):
        QMessageBox.critical(None, "Error", mensaje)
    
    def mostrar_mensaje_info(self, mensaje: str):
        QMessageBox.information(None, "Éxito", mensaje)
    
    def ver_manual_usuario(self):
        try:
            RUTA_MANUAL_GENERADO = obtener_ruta_manual_usuario()
            self.mostrar_mensaje_info(f"Se generó el manual de usuario en la ruta {RUTA_MANUAL_GENERADO} en caso de querer consultar más tarde.")
        except Exception as error:
            self.mostrar_mensaje_error(f"Error al generar el manual de usuario: {error}")


# FUNCIONES REUTILIZABLES POR LAS VENTANAS
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
    
    if nombre_entidad == "departamento" or nombre_entidad == "categoria" or nombre_entidad == "comuna":
        nombres_elementos = [str(elemento[1]) for elemento in lista_elementos]
    else:
        nombres_elementos = [str(elemento[2]) for elemento in lista_elementos]
    
    completer = QCompleter(nombres_elementos)
    completer.setCaseSensitivity(Qt.CaseInsensitive)
    completer.setFilterMode(Qt.MatchContains)
    completer.setCompletionMode(QCompleter.PopupCompletion)
    
    for campo in lista_campos:
        campo.setCompleter(completer)


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
            elif isinstance(campo, QComboBox):
                criterios_filtro[columna] = campo.currentText()
            
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
            if rgetattr(registro, campo_evaluar, ""):
                es_fila_resaltada = True
        
        for columna, nombre_columna in enumerate(nombres_columnas):
            valor = rgetattr(registro, nombre_columna, "")
            
            if valor is None:
                valor = ""
            elif isinstance(valor, date):
                valor = valor.strftime("%d-%m-%Y")
            
            item = QStandardItem(str(valor))
            item.setToolTip(str(valor))
            
            if es_fila_resaltada and color_resaltar:
                item.setBackground(color_resaltar)
            
            modelo_datos.setItem(fila, columna, item)
    
    return modelo_datos, registros

def rgetattr(objeto, atributo, defecto=""):
    """Obtiene un atributo simple o anidado (ej. 'rol.tipo_rol') de un objeto."""
    try:
        return reduce(getattr, atributo.split('.'), objeto)
    except AttributeError:
        return defecto

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