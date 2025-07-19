from fastapi import FastAPI, Request
from pydantic import BaseModel
from typing import List
import joblib
import os

# Cargar las reglas de asociación (debes usar el pkl correcto)
rules = joblib.load("reglas_asociacion.pkl")

app = FastAPI()

# Modelo de entrada
class RecomendacionInput(BaseModel):
    productos: List[str]  # Lista de IDs como string

@app.post("/recomendar")
async def recomendar(input: RecomendacionInput, top_n: int = 5):
    productos_comprados = set(input.productos)
    recomendaciones = []

    for _, row in rules.iterrows():
        if row['antecedents'].issubset(productos_comprados):
            for prod in row['consequents']:
                if prod not in productos_comprados:
                    recomendaciones.append((prod, row['confidence'], row['lift']))

    # Ordenar por confianza y lift
    recomendaciones = sorted(set(recomendaciones), key=lambda x: (-x[1], -x[2]))

    # Extraer solo los IDs sin duplicados
    ids = []
    for rec in recomendaciones:
        if rec[0] not in ids:
            ids.append(rec[0])
        if len(ids) >= top_n:
            break

    return {"recomendaciones": ids}
