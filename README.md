# GUÍA DE CÓMO INSTALAR EL PROYECTO

## Configuración del entorno
Esta aplicación fue hecha en `Python 3.8.10`, por lo que los pasos serían los siguientes una vez clonado el repositorio:

1. **Instalación de dependencias:** <br>

`uv sync` (si tienes instalado uv) <br><br>
`pip install .` (si no tienes o no puedes usar uv, usa este comando que detectará el archivo `pyproject.toml` e instalará las dependencias) <br><br>

2. **Archivo `.env`:** <br>
Para poder trabajar en desarrollo y posteriormente ir empaquetando la app, necesitas crear este archivo en la raíz del proyecto con las siguientes credenciales: <br><br>

`NOMBRE_USUARIO_ADMIN_DEFECTO`<br>
`CLAVE_USUARIO_ADMIN_DEFECTO`<br>
`HOST_BD`<br>
`PUERTO_BD`<br>
`NOMBRE_BD`<br>
`NOMBRE_USUARIO_BD`<br>
`CLAVE_USUARIO_BD`<br>
`CLAVE_SECRETA_SESION`.<br><br>

3. **Ejecutar la aplicación:** <br>
En la raíz del proyecto ejecutas el comando: `python main.py`.<br><br>

4. **Empaquetar la aplicación** <br>
Ejecutas el comando: `pyinstaller .\DGTIC-APP-SERVICIOS.spec` y en la carpeta `dist` se encontrará la carpeta con el `.exe` junto con la carpeta `_internal` con todos las librerias y archivos de recursos necesarios para que la aplicación funcione.
