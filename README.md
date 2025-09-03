# Predictor de Enfermedad Cardíaca

Aplicación con interfaz gráfica para predecir problemas cardíacos usando un árbol de decisión.

## Archivos del proyecto

- `main.py` - Archivo principal para ejecutar la aplicación
- `modelo.py` - Lógica del modelo de machine learning
- `interfaz.py` - Interfaz gráfica de usuario
- `heart.csv` - Dataset necesario (debe estar en la misma carpeta)
- `requirements.txt` - Dependencias de Python

## Instalación

1. Instalar las dependencias:
```bash
pip install -r requirements.txt
```

2. Asegurarse de que el archivo `heart.csv` esté en la misma carpeta que los archivos Python

## Ejecución

```bash
python main.py
```

## Uso de la aplicación

### Campos de entrada
- **Edad**: Edad del paciente en años (20-80)
- **Sexo**: 0 = femenino, 1 = masculino
- **Dolor de pecho**: Tipo de dolor (0-3)
- **Presión arterial**: Presión en reposo en mmHg (70-250)
- **Colesterol**: Nivel de colesterol en mg/dl (100-600)
- **Glucosa ayunas**: Si glucosa > 120 mg/dl (0=No, 1=Sí)
- **ECG reposo**: Resultados del electrocardiograma (0-2)
- **Frecuencia cardíaca máx**: Frecuencia máxima alcanzada (60-220)
- **Angina ejercicio**: Angina inducida por ejercicio (0=No, 1=Sí)
- **Depresión ST**: Depresión ST por ejercicio (0.0-6.0)
- **Pendiente ST**: Pendiente del segmento ST (0-2)
- **Vasos principales**: Número de vasos coloreados (0-3)
- **Talasemia**: Tipo de talasemia (1-3)

### Botones disponibles

1. **Generar Predicción**: Analiza los datos ingresados y muestra el resultado
2. **Limpiar Predicción**: Borra los resultados y restaura valores por defecto
3. **Guardar Imagen del Árbol**: Abre un diálogo para guardar la visualización del árbol

### Información mostrada

- **Resultado de la predicción**: Si el paciente está sano o tiene riesgo
- **Características del árbol**: Profundidad, número de nodos, ramas y nodos terminales
- **Camino de decisión**: Pasos seguidos por el algoritmo para llegar al resultado
- **Probabilidades**: Porcentaje de probabilidad para cada clase

## Estructura del código

El código está organizado en clases para facilitar el mantenimiento:

- `ModeloPredictor`: Maneja toda la lógica del modelo de machine learning
- `InterfazPredictor`: Maneja la interfaz gráfica y la interacción con el usuario
