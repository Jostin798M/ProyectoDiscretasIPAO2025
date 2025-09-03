import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os

class InterfazPredictor:
    '''Inicializa la interfaz gráfica del predictor de enfermedades cardíacas'''
    def __init__(self, root, modelo):
        self.root = root
        self.modelo = modelo
        self.campos = {}
        self.resultado_label = None
        self.caracteristicas_label = None
        self.camino_text = None
        
        self.configurar_interfaz()
    
    '''Configura y organiza todos los componentes principales de la interfaz gráfica'''
    def configurar_interfaz(self):
        # Frame principal con scroll
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Canvas y scrollbar para scroll vertical
        canvas = tk.Canvas(main_frame)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Título
        titulo = ttk.Label(scrollable_frame, text="Predictor de Enfermedad Cardíaca", 
                          font=("Arial", 16, "bold"))
        titulo.pack(pady=(0, 20))
        
        # Frame para los campos de entrada
        campos_frame = ttk.LabelFrame(scrollable_frame, text="Datos del Paciente", padding=10)
        campos_frame.pack(fill=tk.X, pady=(0, 20))
        
        self.crear_campos_entrada(campos_frame)
        
        # Frame para botones
        botones_frame = ttk.Frame(scrollable_frame)
        botones_frame.pack(fill=tk.X, pady=(0, 20))
        
        self.crear_botones(botones_frame)
        
        # Frame para resultados
        resultados_frame = ttk.LabelFrame(scrollable_frame, text="Resultados", padding=10)
        resultados_frame.pack(fill=tk.BOTH, expand=True)
        
        self.crear_seccion_resultados(resultados_frame)
        
        # Empaquetar canvas y scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Configurar scroll con rueda del mouse
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
    
    '''Crea los campos de entrada de datos del paciente organizados en columnas'''
    def crear_campos_entrada(self, parent):
        # Descripciones y valores por defecto
        campos_info = {
            'edad': {'desc': 'Edad (años)', 'defecto': 50, 'rango': '20-80'},
            'sexo': {'desc': 'Sexo (0=F, 1=M)', 'defecto': 1, 'rango': '0-1'},
            'dolorPecho': {'desc': 'Dolor de pecho', 'defecto': 0, 'rango': '0-3'},
            'PresionArterialReposo': {'desc': 'Presión arterial (mmHg)', 'defecto': 120, 'rango': '70-250'},
            'Colesterol': {'desc': 'Colesterol (mg/dl)', 'defecto': 200, 'rango': '100-600'},
            'GlucosaAyunas': {'desc': 'Glucosa ayunas >120 (0=No, 1=Sí)', 'defecto': 0, 'rango': '0-1'},
            'ResultadosElectroReposo': {'desc': 'ECG reposo', 'defecto': 0, 'rango': '0-2'},
            'FrecuenciaCardicaMaxima': {'desc': 'Frecuencia cardíaca máx (bpm)', 'defecto': 150, 'rango': '60-220'},
            'AnginaEjercicio': {'desc': 'Angina ejercicio (0=No, 1=Sí)', 'defecto': 0, 'rango': '0-1'},
            'DepresionSt': {'desc': 'Depresión ST', 'defecto': 0.0, 'rango': '0.0-6.0'},
            'PendienteSt': {'desc': 'Pendiente ST', 'defecto': 1, 'rango': '0-2'},
            'VasosPrincipales': {'desc': 'Vasos principales', 'defecto': 0, 'rango': '0-3'},
            'Talasemia': {'desc': 'Talasemia', 'defecto': 2, 'rango': '1-3'}
        }
        
        # Crear campos en columnas
        row = 0
        col = 0
        max_cols = 2
        
        for campo, info in campos_info.items():
            # Label
            label = ttk.Label(parent, text=f"{info['desc']} ({info['rango']}):")
            label.grid(row=row, column=col*2, sticky="w", padx=(0, 5), pady=2)
            
            # Entry
            var = tk.StringVar(value=str(info['defecto']))
            entry = ttk.Entry(parent, textvariable=var, width=15)
            entry.grid(row=row, column=col*2+1, sticky="w", padx=(0, 20), pady=2)
            
            self.campos[campo] = var
            
            # Siguiente posición
            col += 1
            if col >= max_cols:
                col = 0
                row += 1
    
    '''Crea los botones de acción de la interfaz (predecir, limpiar, guardar imagen)'''
    def crear_botones(self, parent):
        # Botón generar predicción
        btn_predecir = ttk.Button(parent, text="Generar Predicción", 
                                 command=self.generar_prediccion)
        btn_predecir.pack(side=tk.LEFT, padx=(0, 10))
        
        # Botón limpiar
        btn_limpiar = ttk.Button(parent, text="Limpiar Predicción", 
                                command=self.limpiar_prediccion)
        btn_limpiar.pack(side=tk.LEFT, padx=(0, 10))
        
        # Botón guardar imagen
        btn_guardar = ttk.Button(parent, text="Guardar Imagen del Árbol", 
                                command=self.guardar_imagen_arbol)
        btn_guardar.pack(side=tk.LEFT)
    
    '''Crea la sección para mostrar resultados de predicción y camino de decisión'''
    def crear_seccion_resultados(self, parent):
        # Label para resultado de predicción
        self.resultado_label = ttk.Label(parent, text="Predicción: No realizada", 
                                        font=("Arial", 12, "bold"))
        self.resultado_label.pack(pady=(0, 10))
        
        # Label para características del árbol
        self.caracteristicas_label = ttk.Label(parent, text="", justify=tk.LEFT)
        self.caracteristicas_label.pack(pady=(0, 10))
        
        # Mostrar características del árbol al inicio
        self.mostrar_caracteristicas_arbol()
        
        # Frame para camino de decisión
        camino_frame = ttk.LabelFrame(parent, text="Camino de Decisión", padding=5)
        camino_frame.pack(fill=tk.BOTH, expand=True)
        
        # Text widget con scrollbar para mostrar el camino
        text_frame = ttk.Frame(camino_frame)
        text_frame.pack(fill=tk.BOTH, expand=True)
        
        self.camino_text = tk.Text(text_frame, height=10, wrap=tk.WORD, 
                                  font=("Courier", 9))
        text_scrollbar = ttk.Scrollbar(text_frame, orient="vertical", 
                                      command=self.camino_text.yview)
        self.camino_text.configure(yscrollcommand=text_scrollbar.set)
        
        self.camino_text.pack(side="left", fill="both", expand=True)
        text_scrollbar.pack(side="right", fill="y")
    
    '''Obtiene y muestra las características del árbol de decisión (profundidad, nodos, etc.)'''
    def mostrar_caracteristicas_arbol(self):
        caracteristicas = self.modelo.obtener_caracteristicas_arbol()
        texto = f"""Características del Árbol:
Profundidad: {caracteristicas['profundidad']}
Total de nodos: {caracteristicas['total_nodos']}
Número de ramas: {caracteristicas['ramas']}
Nodos terminales: {caracteristicas['nodos_terminales']}"""
        
        self.caracteristicas_label.config(text=texto)
    
    '''Extrae y valida los datos ingresados en el formulario por el usuario'''
    def obtener_datos_formulario(self):
        datos = {}
        try:
            for campo, var in self.campos.items():
                valor_str = var.get().strip()
                if valor_str == "":
                    messagebox.showerror("Error", f"El campo '{campo}' no puede estar vacío")
                    return None
                
                # Convertir a número
                if campo == 'DepresionSt':
                    datos[campo] = float(valor_str)
                else:
                    datos[campo] = int(float(valor_str))
            
            return datos
        except ValueError:
            messagebox.showerror("Error", "Todos los campos deben contener números válidos")
            return None
    
    '''Realiza la predicción del modelo y muestra el resultado con el camino de decisión'''
    def generar_prediccion(self):
        datos = self.obtener_datos_formulario()
        if datos is None:
            return
        
        try:
            # Hacer predicción
            prediccion, probabilidad = self.modelo.predecir_paciente(datos)
            
            # Obtener camino de decisión
            camino = self.modelo.obtener_camino_prediccion(datos)
            
            # Mostrar resultado
            if prediccion == 1:
                resultado_texto = "🔴 PROBLEMAS DEL CORAZÓN"
                color = "red"
            else:
                resultado_texto = "🟢 PACIENTE SANO"
                color = "green"
            
            self.resultado_label.config(text=f"Predicción: {resultado_texto}", 
                                       foreground=color)
            
            # Mostrar camino de decisión
            self.camino_text.delete(1.0, tk.END)
            camino_texto = f"Probabilidad de estar sano: {probabilidad[0]:.1%}\n"
            camino_texto += f"Probabilidad de problemas cardíacos: {probabilidad[1]:.1%}\n\n"
            camino_texto += "Camino de decisión seguido:\n"
            camino_texto += "-" * 40 + "\n"
            
            for i, paso in enumerate(camino, 1):
                camino_texto += f"{i}. {paso}\n"
            
            if not camino:
                camino_texto += "Decisión directa en nodo raíz\n"
            
            self.camino_text.insert(1.0, camino_texto)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al generar predicción: {str(e)}")
    
    '''Limpia los resultados de predicción y restaura los valores por defecto'''
    def limpiar_prediccion(self):
        # Limpiar resultado
        self.resultado_label.config(text="Predicción: No realizada", foreground="black")
        
        # Limpiar camino de decisión
        self.camino_text.delete(1.0, tk.END)
        
        # Restablecer valores por defecto en los campos
        valores_defecto = {
            'edad': 50, 'sexo': 1, 'dolorPecho': 0, 'PresionArterialReposo': 120,
            'Colesterol': 200, 'GlucosaAyunas': 0, 'ResultadosElectroReposo': 0,
            'FrecuenciaCardicaMaxima': 150, 'AnginaEjercicio': 0, 'DepresionSt': 0.0,
            'PendienteSt': 1, 'VasosPrincipales': 0, 'Talasemia': 2
        }
        
        for campo, var in self.campos.items():
            var.set(str(valores_defecto[campo]))
    
    '''Abre un diálogo para guardar la imagen visual del árbol de decisión'''
    def guardar_imagen_arbol(self):
        # Abrir diálogo para seleccionar donde guardar
        archivo = filedialog.asksaveasfilename(
            title="Guardar imagen del árbol",
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("All files", "*.*")]
        )
        
        if archivo:
            try:
                self.modelo.crear_imagen_arbol(archivo)
                messagebox.showinfo("Éxito", f"Imagen guardada exitosamente en:\n{archivo}")
            except Exception as e:
                messagebox.showerror("Error", f"Error al guardar la imagen: {str(e)}")
