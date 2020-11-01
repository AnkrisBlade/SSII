# SSII - Practica 1

<h3> Script de comprobación de la integridad de ficheros (HIDS)</h3>

<p>Librerias empleadas:</p>
    <ul>csv: Para manejar archivos csv</ul>
    <ul>hashlib: Para generar el hash de la contraseña</ul>
    <ul>logging: Para generar un informe con las notificaciones</ul>
    <ul>configparser: Para hacer uso de un archivo de configuracion</ul>
    
<p>Pasos para utilizar el script:</p>

1. Rellenar los campos necesarios en el archivo de configuracion
2. Crear un archivo .shadow que contendrá la contraseña del administrador hasheada,
sino se le solicitará una contraseña que será guardada en un archivo sin nombre con dicha extension.
3. Crear un archivo .csv con los que contendra los diferentes directorios a 
comprobar, un directorio por cada linea del archivo.
4. Ejecutar "hids.py" desde el terminal e introducir los datos pertinentes en la consola.

<p>Funcionamiento del script: 
<br>
Una vez ejecutado "hids.py" se comprobarán que se cumplimenten los parametros definidos
en el archivo de configuracion, luego se le solicitará la contraseña de administrador
si ya tiene una, sino, se le pedirá que la inserte. Después se accederá al archivo
donde a definido los directorios a comprobar y se generarán los hashes para su comprobación.

Una vez realizado todo esto se da comienzo al bucle que irá verificando la integridad de
los archivos, generando de forma diaria un informe con las notificaciones almacenadas a lo
largo de un día</p>