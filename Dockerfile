# Imagen base de Python
FROM python:3.12-slim

# Establecer directorio de trabajo
WORKDIR /app

# Copiar dependencias y código
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app /app

# Puerto por defecto para FastAPI
EXPOSE 8000

# Comando para ejecutar la aplicación
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
