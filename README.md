# PizzeriaMaven1
## Info.
Este proyecto trata de obtener, a partir de una ETL que procesa una serie de pedidos de un dataset de una pizzeria, el número de ingredientes que se debe pedir por cada una de las semanas del año. La idea tras la transformacion de los datos es bastante simple: mapear las fechas de cada uno de los pedidos a su correspondiente semana, e ir sumando por cada pizza pedida los ingredientes necesarios por cada tipo de ingrediente distinto. Todo hecho con el objetivo de ser lo mas eficiente posible, usando las funciones built-in de pandas para iterar sobre los datos de manera rápida y segura. El output es un csv con el número de ingredientes para cada tipo por semana y un fichero xml con el reporte de tipologia de los datos.
- Para lanzar el programa sera necesario crear una carpeta llamada 'out' dentro del directorio de trabajo.
## Requirements.
Para poder correr el programa hay que instalar los paquetes necesarios con sus correspondientes versiones. Se ejecutara el siguiente codigo en terminal:

>>>pip install -r requirements.txt

## Docker.
Para lanzar la imagen de docker habrá que seguir los siguientes pasos:
1. Crear la imagen:
- El punto indica que se cogen todos los archivos del directorio en el que nos encontramos. Podemos llamar a la imagen como queramos, teniendo en cuenta que al ejecutarla tendremos que usar ese nombre.
>>>docker build . -t 'nombre con el que quieras llamarlo'

2. Una vez que tengamos la imagen creada tendremos que elegir un path absoluto del directorio al que queramos que se linkee el contenedor de docker para que podamos ver la salida del programa.
- absolute_path = ['path del directorio de salida host']. En el caso en el que no exista el directorio que queremos linkear lo crea.
- Es importante mantener la estructura del siguiente comando. En particular el path tras ':' no debera ser alterado ya que es el directorio interno del contenedor.
>>>docker run -v absolute_path:/out 'nombre con el que hayas llamado a la imagen'.
