import pandas as pd
from sklearn.tree import DecisionTreeClassifier, plot_tree, export_text
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

class ModeloPredictor:
    def __init__(self, dataframe):
        self.dataframe = dataframe
        self.arbol = None
        self.x_train = None
        self.y_train = None
        self.x_test = None
        self.y_test = None
        self.columnas_entrenamiento = None
        self.entrenar_modelo()
    
    def sacar_particiones(self):
        # X: entradas, Y: salida a predecir
        datos_estudio = self.dataframe.iloc[:,:-1]
        datos_resultados = self.dataframe.iloc[:,-1]
        
        # Partición
        x_train, x_test, y_train, y_test = train_test_split(
            datos_estudio, datos_resultados, 
            test_size=0.3, random_state=123
        )
        
        return x_train, x_test, y_train, y_test
    
    def crear_arbol(self, x_train, y_train):
        # Crear instancia del árbol y entrenar
        arbol = DecisionTreeClassifier(random_state=123, max_depth=5)
        arbol.fit(x_train, y_train)
        return arbol
    
    def entrenar_modelo(self):
        self.x_train, self.x_test, self.y_train, self.y_test = self.sacar_particiones()
        self.arbol = self.crear_arbol(self.x_train, self.y_train)
        self.columnas_entrenamiento = self.x_train.columns
    
    def predecir_paciente(self, datos_paciente):
        # Crear DataFrame con los datos del paciente
        df_paciente = pd.DataFrame([datos_paciente])
        
        # Hacer predicción
        prediccion = self.arbol.predict(df_paciente)[0]
        probabilidad = self.arbol.predict_proba(df_paciente)[0]
        
        return prediccion, probabilidad
    
    def obtener_camino_prediccion(self, datos_paciente):
        # Crear DataFrame con los datos del paciente
        df_paciente = pd.DataFrame([datos_paciente])
        
        # Obtener el camino de decisión
        camino = self.arbol.decision_path(df_paciente).toarray()[0]
        feature = self.arbol.tree_.feature
        threshold = self.arbol.tree_.threshold
        
        camino_texto = []
        nodos_visitados = []
        
        for i, nodo_visitado in enumerate(camino):
            if nodo_visitado:
                nodos_visitados.append(i)
        
        # Construir el camino textual
        for i in range(len(nodos_visitados) - 1):
            nodo_actual = nodos_visitados[i]
            caracteristica_idx = feature[nodo_actual]
            umbral = threshold[nodo_actual]
            
            if caracteristica_idx >= 0:  # Si no es hoja
                nombre_caracteristica = self.columnas_entrenamiento[caracteristica_idx]
                valor_paciente = datos_paciente[nombre_caracteristica]
                
                if valor_paciente <= umbral:
                    decision = f"{nombre_caracteristica} ({valor_paciente}) <= {umbral:.2f}"
                else:
                    decision = f"{nombre_caracteristica} ({valor_paciente}) > {umbral:.2f}"
                
                camino_texto.append(decision)
        
        return camino_texto
    
    def crear_imagen_arbol(self, ruta_guardado):
        plt.figure(figsize=(30, 15))
        plot_tree(self.arbol,
                  feature_names=self.x_train.columns,
                  class_names=['Sano', 'Problemas del corazón'],
                  filled=True,
                  rounded=True)
        
        plt.savefig(ruta_guardado, dpi=700, bbox_inches='tight')
        plt.close()
    
    def obtener_caracteristicas_arbol(self):
        profundidad = self.arbol.get_depth()
        hojas = self.arbol.get_n_leaves()
        total_nodos = self.arbol.tree_.node_count
        
        # Calcular ramas (nodos internos)
        ramas = total_nodos - hojas
        
        return {
            'profundidad': profundidad,
            'nodos_terminales': hojas,
            'total_nodos': total_nodos,
            'ramas': ramas
        }