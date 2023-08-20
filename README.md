# Ecommerce Flask Postgres App

Este es un proyecto de una aplicación de comercio electrónico desarrollada en Flask y utilizando PostgreSQL como base de datos. A continuación, se detallan los pasos para configurar y ejecutar la aplicación en su entorno de desarrollo.

**Recomendación:** Se recomienda utilizar la consola de Git Bash para ejecutar los comandos a lo largo de este proceso.

## Configuración del Entorno de Desarrollo

1. Cree un entorno virtual de Python utilizando una de las siguientes opciones:

   - Utilizando `virtualenv`:
     ```bash
     pip install virtualenv
     ```

   - Utilizando `venv` (dependiendo de su versión de Python):
     ```bash
     pip install venv
     ```

2. Active el entorno virtual de Python:
   - En Windows:
     ```bash
     venv\Scripts\activate
     ```
   - En consola Git:
     ```bash
     . venv/Scripts/activate
     ```

## Instalación de Dependencias

3. Instale las dependencias del proyecto desde el archivo `requirements.txt`:
   ```bash
   pip install -r requirements.txt

## Instalación y configuración de base de datos

4. Instale PostgreSQL y configure su base de datos.

5. En el archivo .env, proporcione la información necesaria para la conexión a la base de datos. Debe configurar las siguientes variables de entorno:
  DB_HOST=nombre_de_host
  DB_USER=nombre_de_usuario
  DB_PASSWORD=contraseña
  DB_NAME=nombre_de_base_de_datos

## Ejecución de aplicación

6. Para iniciar la aplicación, ejecute el siguiente comando:
  ```
    flask run
  ```
   
## Modo Debug de Flask

7. Para evitar tener que detener y reiniciar el servidor cada vez que realice cambios en el código, configure el modo de depuración de Flask. En Git Bash, ejecute el siguiente comando:
   ```
    export FLASK_DEBUG=1
   ```
