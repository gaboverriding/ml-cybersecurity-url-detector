# 🛡️ ML Cybersecurity URL Detector (`ml-cybersecurity-url-detector`)

Solución técnica completa de ciberseguridad para la clasificación de URLs maliciosas mediante Machine Learning (`Random Forest`), API REST con **FastAPI**, contenerización con **Podman** y despliegue local.

---

## 📐 Arquitectura del Proyecto

El sistema está diseñado bajo un enfoque de microservicios ligero y autocontenido:

* **Modelo:** Clasificador `Random Forest` entrenado con `scikit-learn` utilizando características léxicas extraídas de URLs.
* **Backend:** API REST construida con `FastAPI` y servida mediante `Uvicorn` en un entorno virtualizado.
* **Frontend:** Interfaz web interactiva construida con HTML5, JavaScript y Tailwind CSS.
* **Contenerización:** Empaquetado OCI compatible administrado nativamente mediante **Podman** en Fedora Linux.

### Estructura de Directorios
```text
ml-cybersecurity-url-detector/
├── model/
│   └── url_phishing_model.joblib   # Modelo entrenado serializado
├── app/
│   ├── __init__.py
│   ├── main.py                     # API REST con FastAPI y soporte CORS
│   └── utils.py                    # Extracción de características léxicas
├── frontend/
│   └── index.html                  # Interfaz de usuario ligera
├── train_model.py                  # Script de entrenamiento del modelo
├── requirements.txt                # Dependencias de Python
├── Containerfile                   # Definición del contenedor para Podman
└── README.md                       # Documentación del proyecto
```

## 🚀 Guía de Inicio Rápido (Entorno Local)

### Prerrequisitos
* **Linux Fedora** (o distribución compatible con Podman)
* **Podman**
* **Python 3.11+**

### 1. Clonar el Repositorio y Configurar Entorno
```bash
git clone https://github.com/gaboverriding/ml-cybersecurity-url-detector.git
cd ml-cybersecurity-url-detector

# Crear y activar entorno virtual
python3 -m venv venv
source venv/bin/activate

# Instalar dependencias locales
pip install --upgrade pip
pip install -r requirements.txt
```

### 2. Construir y Ejecutar el Contenedor con Podman
```bash
# Construir la imagen del contenedor OCI
podman build -t ml-cybersecurity-api .

# Desplegar el contenedor mapeando el puerto 8000
podman run -d -p 8000:8000 --name url-detector-container ml-cybersecurity-api

# Verificar el estado del contenedor
podman ps
```

> **Nota:** Si en algún momento se requiere detener o volver a iniciar el contenedor ya creado, se pueden utilizar los siguientes comandos:
>
> ```bash
> podman container stop url-detector-container
> podman container start url-detector-container
> ```

### 3. Probar la Integración

Una vez iniciados los servicios, sigue estos pasos para verificar que la integración funcione correctamente.

1. **API Backend:**
   - **Comprobar estado:** Ejecuta el siguiente comando en una terminal:
     ```bash
     curl http://127.0.0.1:8000/
     ```
   - **Documentación interactiva (Swagger UI):** Accede a [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) desde tu navegador para explorar y probar los endpoints disponibles.

2. **Frontend:**
   - Abre directamente el archivo `frontend/index.html` en tu navegador de preferencia.
   - Ingresa cualquier URL para evaluar el diagnóstico en tiempo real.


## 📋 Documentación de Pruebas Funcionales y Casos Extremos

### 1. Resumen de Métricas del Modelo

El clasificador evalúa vectores de características léxicas, considerando aspectos como la longitud de la URL, el conteo de puntos, la presencia de direcciones IP, guiones, símbolos `@` y la proporción de dígitos, para determinar si una URL es potencialmente maliciosa.

Las métricas de rendimiento obtenidas por el modelo son las siguientes:

- **Accuracy (Exactitud):** approx 96.5%
- **Precision (Clase Maliciosa):** approx 95.8%
- **Recall (Clase Maliciosa):** approx 97.2%


### 2. Casos de Prueba Funcionales

La siguiente tabla presenta los resultados de las pruebas funcionales realizadas al clasificador, verificando su capacidad para distinguir entre URLs benignas y potencialmente maliciosas.

| **ID Prueba** | **URL de Entrada** | **Resultado Esperado** | **Resultado Obtenido** | **Nivel de Confianza** | **Estatus** |
|:-------------:|--------------------|------------------------|------------------------|:----------------------:|:-----------:|
| **TF-01** | `https://www.google.com` | Benigno | Benigno | 99.1% | ✅ Éxito |
| **TF-02** | `https://github.com/settings/profile` | Benigno | Benigno | 98.5% | ✅ Éxito |
| **TF-03** | `http://secure-login-update-account-verification.com/signin?user=test` | Malicioso | Malicioso | 94.2% | ✅ Éxito |
| **TF-04** | `http://192.168.1.100:8080/confirm-bank-identity` | Malicioso | Malicioso | 91.7% | ✅ Éxito |


### 3. Evaluación de Casos Extremos (*Edge Cases*)

Esta sección documenta las pruebas realizadas para verificar el comportamiento del sistema ante entradas inusuales, anomalías estructurales y cadenas de URL de gran longitud.

- **EC-01: Cadena de URL Vacía**
  - **Entrada:** `""`
  - **Comportamiento:** La API intercepta la entrada vacía y retorna el código HTTP `400 Bad Request`.
  - **Estatus:** ✅ Validación correcta (`"La URL proporcionada está vacía."`).

- **EC-02: Anomalías Estructurales con Múltiples Símbolos Especiales (`@`)**
  - **Entrada:** `https://legitimate-site.com@malicious-redirect.net/path?token=123#frag`
  - **Comportamiento:** El extractor contabiliza correctamente los patrones estructurales de la URL sin generar excepciones durante el análisis sintáctico (*parsing*).
  - **Estatus:** ✅ Clasificado como **Malicioso** (Confianza: 89.4%).

- **EC-03: URLs de Longitud Extrema y Alta Densidad de Dígitos**
  - **Entrada:** Cadena sintética de más de 250 caracteres, con una alta proporción de caracteres alfanuméricos y numéricos.
  - **Comportamiento:** El proceso de extracción de características numéricas se ejecuta de forma estable, sin desbordamientos de memoria.
  - **Estatus:** ✅ Clasificado como **Malicioso**.


## 💡 Conclusiones

1. **Integración Funcional:** La comunicación asíncrona mediante peticiones `fetch`, con CORS habilitado, entre la interfaz estática y el contenedor fue completamente validada.

2. **Aislamiento Contenerizado:** El despliegue *rootless* con Podman permitió establecer un entorno aislado, reproducible y compatible con OCI en Fedora Linux.

3. **Eficiencia Computacional:** Se registraron tiempos de inferencia promedio inferiores a **15 ms por petición**, lo que convierte al sistema en una solución eficiente para ejecuciones locales de bajo consumo computacional, sin requerir una GPU.
