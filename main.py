from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import joblib
import os
import uvicorn

# Cargar las reglas de asociación
rules_path = os.path.join(os.path.dirname(__file__), "reglas_asociacion.pkl")
rules = joblib.load(rules_path)

# Inicializar la app FastAPI
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

    recomendaciones = sorted(set(recomendaciones), key=lambda x: (-x[1], -x[2]))

    ids = []
    for rec in recomendaciones:
        if rec[0] not in ids:
            ids.append(rec[0])
        if len(ids) >= 5:
            break

    return {"recomendaciones": ids}

# Solo necesario si corres localmente
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)
