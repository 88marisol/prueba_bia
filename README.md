# PRUEBA MARISOL CORREA HENAO
## 88marisol@gmail.com

A continuación se explicará el contenido de las carpetas:
- En la carpeta Microservicio1 se encuentran los archivos necesarios para leer los datos del archivo .cdv que contiene  latitud y longitud y guardarlos en una base de datos
- En la carpeta Microservicio2 se encuentran los archivos necesarios para leer los datos almacenados en la base de datos y hacer las peticiones a la api para traer los códigos postales y mostrarlos

Dentro de cada carpeta se tiene la siguiente estructura:
- En la carpeta app se encontrará el controlador con el código en pythonpara realizar el procedimiento correspondiente
- En la carpeta files se encuentran los archivos necesarios
- en la carpeta instance se encuentra la base de datos (esta carpeta se crear automáticamente al ejecutar el código) 
- en la carpeta views se encontrará la vista de cada app de manera que sea más facil el proceso
- Se encuentra el Dockerfile para ejecutar y el archivo requirements para instalar dependiencias

## Generalidades

-Al momento de leer el archivo csv se hace manejo de errores en caso que no encuentre archivo o el archivo que se lea sea otra extensión diferente a csv, desde la vista tambipen se controla que sólo se reciba archivos csv desde las opciones del formulario html.
-Se crea en la base de datos la columna cod_postal pensando en el funcionamiento del microservicio2, ya que en el microservicio2 no se crea base de datos sino que se copia la instancia de la base de datos creada en el microservicio1
-En el microservicio2 se hace manejo de error al momento de llamar la api, para facilitar el uso de la app, en caso de algún error al momento de hacer la petición a la API el arror se guarda como texto y se pone en la base dedatos en la columna cod_postal, por lo que si no encuentra codigo postal guardará el error generado y no se realiza manejo de nulos
-Dado a la gran cantidad de datos el microservicio2 puede demorarse un poco.
-Se limita las peticiones a la api a través de la librería ratelimits, se parametriza 1 petición por segundo.


## Mejoras
-Los microservicios se crearon de forma sencilla, mejoraría la conextión entre microservicios con una interfaz que pase de uno al otro
-El manejo de errores de la api tienen muchas portunidades de mejora
-haría algún modulo o solución para mejorar el tiempo de respuesta al hacer la petición