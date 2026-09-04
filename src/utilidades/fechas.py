import calendar
from datetime import datetime


def cargar_mes(fecha_str: str) -> str:
        fecha_dt = datetime.strptime(fecha_str, "%m-%Y")
        
        diccionario_meses_espaniol = {
            "January": "Enero",
            "February": "Febrero",
            "March": "Marzo",
            "April": "Abril",
            "May": "Mayo",
            "June": "Junio",
            "July": "Julio",
            "August": "Agosto",
            "September": "Septiembre",
            "October": "Octubre",
            "November": "Noviembre",
            "December": "Diciembre"
        }
        
        # Obtener el nombre del mes en inglés de la fecha de nacimiento
        nombre_mes_ingles = calendar.month_name[fecha_dt.month]
        
        # Devolver el nombre del mes en español
        return diccionario_meses_espaniol.get(nombre_mes_ingles)


if __name__ == "__main__":
    try:
        mes_espaniol = cargar_mes("10-2025")
        
        print(mes_espaniol)
    except Exception as error:
        print(error)