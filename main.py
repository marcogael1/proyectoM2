from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import joblib
import os

# Cargar las reglas de asociación desde el archivo .pkl
rules_path = os.path.join(os.path.dirname(__file__), "reglas_asociacion.pkl")
rules = joblib.load(rules_path)

# Inicializar la aplicación FastAPI
app = FastAPI()

# Modelo de entrada
class RecomendacionInput(BaseModel):
    productos: List[str]

# Endpoint de recomendación
@app.post("/recomendar")
async def recomendar(input: RecomendacionInput):
    productos_comprados = set(input.productos)
    recomendaciones = []

    for _, row in rules.iterrows():
        if row['antecedents'].issubset(productos_comprados):
            for producto in row['consequents']:
                if producto not in productos_comprados:
                    recomendaciones.append((producto, row['confidence'], row['lift']))

    # Ordenar por confianza y lift
    recomendaciones = sorted(set(recomendaciones), key=lambda x: (-x[1], -x[2]))

    # Devolver solo los IDs únicos (top 5)
    ids = []
    for rec in recomendaciones:
        if rec[0] not in ids:
            ids.append(rec[0])
        if len(ids) >= 5:
            break

    return {"recomendaciones": ids}
