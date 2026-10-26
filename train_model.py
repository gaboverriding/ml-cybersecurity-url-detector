import os
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
import joblib

# 1. Simulación o carga de datos de ejemplo (Características léxicas de URLs)
# En un caso real, aquí cargarías un CSV público como el de Phishing Dataset de UCI o Kaggle.
np.random.seed(42)
n_samples = 2000

# Características simuladas:
# [url_length, num_dots, has_ip, num_hyphens, num_at_symbol, ratio_digits]
data_benign = np.column_stack([
    np.random.normal(35, 10, n_samples // 2),  # Longitud moderada
    np.random.poisson(2, n_samples // 2),     # Pocos puntos
    np.random.choice([0, 1], n_samples // 2, p=[0.99, 0.01]), # Rara vez IP
    np.random.poisson(1, n_samples // 2),     # Pocos guiones
    np.zeros(n_samples // 2),                 # Sin '@'
    np.random.beta(2, 5, n_samples // 2)      # Bajo ratio de dígitos
])

data_malicious = np.column_stack([
    np.random.normal(75, 20, n_samples // 2), # URLs más largas
    np.random.poisson(5, n_samples // 2),     # Más puntos
    np.random.choice([0, 1], n_samples // 2, p=[0.70, 0.30]), # Mayor probabilidad de IP
    np.random.poisson(3, n_samples // 2),     # Más guiones
    np.random.choice([0, 1], n_samples // 2, p=[0.80, 0.20]), # Posible presencia de '@'
    np.random.beta(5, 2, n_samples // 2)      # Alto ratio de dígitos
])

X = np.vstack([data_benign, data_malicious])
y = np.array([0] * (n_samples // 2) + [1] * (n_samples // 2)) # 0: Benigno, 1: Malicioso

# 2. División de datos en entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# 3. Entrenamiento del modelo Random Forest
print("Entrenando el modelo RandomForest...")
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# 4. Evaluación del modelo
y_pred = model.predict(X_test)
print(f"\nAccuracy: {accuracy_score(y_test, y_pred):.4f}\n")
print("Reporte de Clasificación:")
print(classification_report(y_test, y_pred, target_names=["Benigno", "Malicioso"]))

# 5. Guardar el modelo serializado
os.makedirs("model", exist_ok=True)
model_filename = os.path.join("model", "url_phishing_model.joblib")
joblib.dump(model, model_filename)
print(f"\n¡Modelo guardado exitosamente como '{model_filename}'!")