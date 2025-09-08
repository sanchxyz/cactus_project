# Usa una imagen oficial de Python como base
FROM python:3.13-slim

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia el archivo de requerimientos
COPY requirements.txt .

# Instala las dependencias del proyecto
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto del código de tu aplicación al contenedor
COPY . .

# Expone el puerto en el que Gunicorn correrá
EXPOSE 8000

# El comando para iniciar la aplicación usando Gunicorn (Versión simple)
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app:app"]
