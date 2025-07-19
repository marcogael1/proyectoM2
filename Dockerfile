# Imagen base
FROM python:3.12-slim

# Crear el directorio de trabajo
WORKDIR /app

# Copiar archivos necesarios
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py .
COPY reglas_asociacion.pkl .  # 👈 Asegúrate de copiar el archivo de reglas aquí

# Exponer el puerto que usará FastAPI
EXPOSE 8000

# Comando para ejecutar la app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
