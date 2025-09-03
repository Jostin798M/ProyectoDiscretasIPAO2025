import pandas as pd
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

# Para mayor facilidad del manejo de los datos creamos una clase llama modeloPredictor
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
    
    '''
    Metodo encargado de particionar los datos del data set
    1. Separa los datos de estudio del dato resultado usando iloc de pandas
    2. Usado el metodo decisionTreeClassifier separa los datos de entrenamiento y de testeo
       en caso de ser necesarios a futuro.
    Retorno: Retorna un arreglo con todos los datos creados.
    '''
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
    
    '''
    Mediante el uso del algoritmo de CART crea la estructura del arbol y luego lo entrena usando fit
    con los datos creados en el metodo sacar_particiones
    Retorno: nos retorna la variable tipo arbol.
    '''
    def crear_arbol(self, x_train, y_train):
        # Crear instancia del árbol y entrenar
        arbol = DecisionTreeClassifier(random_state=123, max_depth=5)
        arbol.fit(x_train, y_train)
        return arbol

    '''
    Metodo encargado hacer de constructor con los datos previamente calculados
    en el metodo sacar_particiones y crear_arbol a los parametros de la clase
    '''
    def entrenar_modelo(self):
        self.x_train, self.x_test, self.y_train, self.y_test = self.sacar_particiones()
        self.arbol = self.crear_arbol(self.x_train, self.y_train)
        self.columnas_entrenamiento = self.x_train.columns
    

    '''
    Metodo encargado de realizar la prediccion de los datos ingresados por el usuario
    mediante el modelo previamente entrenado
    '''
    def predecir_paciente(self, datos_paciente):
        # Crear DataFrame con los datos del paciente
        df_paciente = pd.DataFrame([datos_paciente])
        
        # Hacer predicción
        prediccion = self.arbol.predict(df_paciente)[0]
        probabilidad = self.arbol.predict_proba(df_paciente)[0]
        
        return prediccion, probabilidad
    

    '''
    Metodo encargado de extraer el camino textual por el que paso el arbol para llegar a esa prediccion
    utilizando metodos de sklearn como decicion_path encargado de extrarer la ruta del arbol y
    posteriormente convertirla a texto
    '''
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
    

    '''
    Metodo encargado de la construccion visual del arbol por medio de la libreria matplotlib
    junto a ciertas caracteristicas dadas en el metodo plot_tree de como se va a cisualizar el arbol
    '''
    def crear_imagen_arbol(self, ruta_guardado):
        plt.figure(figsize=(30, 15))
        plot_tree(self.arbol,
                  feature_names=self.x_train.columns,
                  class_names=['Sano', 'Problemas del corazón'],
                  filled=True,
                  rounded=True)
        
        plt.savefig(ruta_guardado, dpi=700, bbox_inches='tight')
        plt.close()
    
    '''
    Metodo encargado de realizar los calculos de cual es la profundidad del arbol el numero de nodos
    por medio de la operacion de arboles binarios total_nodos = ramas + hojas
    '''
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
    
