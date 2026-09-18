# GUÍA DE CÓMO INSTALAR EL PROYECTO

## Configuración del entorno
Esta aplicación fue hecha en `Python 3.8.10`, por lo que los pasos serían los siguientes una vez clonado el repositorio:

1. **Instalación de dependencias:** <br>

`uv sync` (si tienes instalado uv) <br><br>
`pip install .` (que detectará el archivo `pyproject.toml` e instalará las dependencias) <br><br>

2. **Archivo `.env` y `.env.ejemplo`:** <br>
El archivo `.env` se utiliza para las variables de entorno mientras estas desarrollando, mientras que `.env.ejemplo` es cuando quieres ejecutar la aplicación ya empaquetada.<br><br>

3. **Ejecutar la aplicación:** <br>
En la raíz del proyecto ejecutas el comando: `python main.py`.<br><br>

4. **Empaquetar la aplicación** <br>
Ejecutas el comando: `pyinstaller .\DGTIC-APP-SERVICIOS.spec` y en la carpeta `dist` se encontrará la carpeta con el `.exe` junto con la carpeta `_internal` con todos las librerias y archivos de recursos necesarios para que la aplicación funcione.
