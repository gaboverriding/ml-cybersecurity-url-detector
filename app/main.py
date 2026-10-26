from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import os
from app.utils import extract_features

app = FastAPI(
    title="ML Cybersecurity URL Detector API",
    description="API para la detección de URLs maliciosas mediante Machine Learning",
    version="1.0.0"
)

# Cargar el modelo entrenado
MODEL_PATH = os.path.join("model", "url_phishing_model.joblib")
try:
    model = joblib.load(MODEL_PATH)
except Exception as e:
    model = None

class URLRequest(BaseModel):
    url: str

@app.get("/")
def read_root():
    return {"message": "Bienvenido a la API de Detección de Phishing con ML", "status": "activo"}

@app.post("/predict")
def predict_url(payload: URLRequest):
    if model is None:
        raise HTTPException(status_code=500, detail="El modelo no se encuentra cargado en el servidor.")
    
    url = payload.url.strip()
    if not url:
        raise HTTPException(status_code=400, detail="La URL proporcionada está vacía.")
    
    try:
        # Extraer características y predecir
        features = extract_features(url)
        prediction = int(model.predict(features)[0])
        probability = float(model.predict_proba(features)[0].max())
        
        result_label = "Malicioso" if prediction == 1 else "Benigno"
        
        return {
            "url": url,
            "prediction": result_label,
            "prediction_code": prediction,
            "confidence": round(probability * 100, 2)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error procesando la URL: {str(e)}")