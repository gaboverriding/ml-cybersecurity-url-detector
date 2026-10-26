# Usar una imagen oficial ligera de Python como base compatible con Podman
FROM python:3.11-slim

# Establecer el directorio de trabajo dentro del contenedor
WORKDIR /app

# Instalar herramientas básicas de compilación si fueran necesarias
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copiar e instalar las dependencias de Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código fuente de la API y el modelo entrenado
COPY ./app ./app
COPY ./model ./model

# Exponer el puerto estándar de FastAPI
EXPOSE 8000

# Comando para iniciar el servidor Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

