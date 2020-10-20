# SSII - Consultoria 1

<h3> Script de almacenamiento de una contraseña dada o generada </h3>

<p>Librerias empleadas:</p>
    <ul>SQLAlchemy: Para conectarnos a una base de datos y crear la tabla de almacenamiento</ul>
    <ul>PyMySQl: Para conectarnos a MySql</ul>
    <ul>hashlib: Para generar el hash de la contraseña</ul>
    <ul>random: Para generar valores aleatorios</ul>
    
<p>Pasos para utilizar el script:</p>
        <ol>
        <li>Definir la conexion con la base de datos</li>
        <li>Ejecutar "generator_password.py" e introducir los datos que correspondan en la consola</li>
        </ol>
        
<p>Definir la conexion a la base de datos dentro de "base_hash.py":</p>
 <p><code>'mysql+pymysql://root:password@127.0.0.1/schema'</code></p>
 <p>Donde:</p> 
 <p><code>mysql+pymsql</code> es el controlador para conectarnos a la base de datos</p>
 <p><code>root</code> es el usuario</p>
 <p><code>password</code> es la contraseña</p>
 <p><code>schema</code> es el schema vacio creado donde almacenaremos la tabla con las contraseñas</p>
 
 <p>Ejecutar "generator_passowrd.py":</p>
    <ul>Una vez ejecutado tendremos que responder las preguntas pertinentes en el terminal, al finalizar,
     si la contraseña cumple con los requisitos, tiene la opción de guardarla en la base de datos
     antes descrita.</ul>