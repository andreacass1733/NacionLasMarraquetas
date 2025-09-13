#Usa una imagen base de Python 3.11 ligera (ideal para producción).
FROM python:3.11-slim

#Establece el directorio de trabajo dentro del contenedor. 
#Todo lo que hagas después (copiar archivos, ejecutar comandos) será relativo a /app.
WORKDIR /app

#Copia todo el contenido de tu carpeta backend/ 
#(donde tienes app.py, templates/, static/, etc.) dentro del contenedor, en el directorio /app.
COPY backend/ ./

#Instala las dependencias de Python listadas en requirements.txt, sin guardar caché (para que la imagen sea más liviana).
RUN pip install --no-cache-dir -r requirements.txt

#Informa que el contenedor va a escuchar en el puerto 5000 (el puerto por defecto de Flask). Es útil para que Docker o 
#plataformas externas sepan qué puerto abrir.
EXPOSE 5000

#Indica el comando por defecto que se ejecuta cuando el contenedor arranca. En este caso, inicia tu app Flask (app.py).
CMD ["python", "app.py"]

#Cambio para generar el archivo de IBM
