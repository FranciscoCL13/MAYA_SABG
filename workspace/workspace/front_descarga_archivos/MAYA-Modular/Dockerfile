FROM python:3.10-slim

# Establecer directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar los archivos del proyecto al contenedor
COPY . .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Exponer el puerto 5000 para Flask
EXPOSE 8083

# Comando que se ejecutará al iniciar el contenedor
CMD ["python", "-m", "app.main"]
