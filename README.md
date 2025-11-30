# GUÍA DE CÓMO INSTALAR EL PROYECTO

## Configuración del entorno
Esta aplicación fue hecha en `Python 3.8.10`, por lo que los pasos serían los siguientes una vez clonado el repositorio:

1. **Configuramos el entorno de python:** <br>

`pip install virtualenv` <br><br>
`py -3.8 -m venv nombre_del_entorno` <br><br>
`.\nombre_del_entorno\Scripts\activate` <br><br>
`pip install -r requerimientos.txt` (para instalar todas las dependencias en tu entorno virtual) <br><br>

2. **Configuración para la base de datos:** <br>

Hay que tener para esto instalado XAMPP y activar los servicios de Apache y MySQL, utilizar el archivo que está ubicado en `src/infraestructura/base_datos/estructura_bd.sql`, para poder cargarlo en el gestor de base de datos<br> 
de tu preferencia (como phpMyAdmin por ejemplo). Si el usuario que creaste en tu gestor es el predeterminado, que si `usuario: root` y `clave: ""`, entonces lo siguiente es crear 
un archivo `.env` para cargar la configuración de la base de datos.<br><br>

3. **Crear el archivo `.env`:** <br>

Para esto te situas en el mismo directorio que está el archivo `.env.ejemplo` y copias su contenido en el nuevo archivo llamado `.env`. Importante el nombre que le des a la base de datos sea el mismo
que el que vayas a poner en `NOMBRE_BD`.<br><br>

4. **Ejecutar la aplicación:** <br>

Situandose en la carpeta `src` ejecutamos el siguiente comando: `python main.py` e iniciamos sesión con el usuario y contraseña que se estableció por defecto en el `.env` que crearon
que están en `NOMBRE_USUARIO_ADMIN_DEFECTO` y `CLAVE_USUARIO_ADMIN_DEFECTO`.
