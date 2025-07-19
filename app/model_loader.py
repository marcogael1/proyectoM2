import joblib

def load_model(path="reglas_asociacion.pkl"):
    return joblib.load(path)
