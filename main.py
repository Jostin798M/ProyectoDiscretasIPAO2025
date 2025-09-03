import tkinter as tk
from tkinter import messagebox
import pandas as pd
from modelo import ModeloPredictor
from interfaz import InterfazPredictor

# Creacion de la ventana principal de la interfaz
ventana = tk.Tk()
ventana.title("Predictor de Enfermedad Cardíaca")
ventana.geometry("800x900")
ventana.resizable(False, False)

try:
    # Cargar datos y crear modelo de arbol de decicion
    df = pd.read_csv('test/heart.csv')
    modelo = ModeloPredictor(df)
    
    # Crear interfaz principal
    app = InterfazPredictor(ventana, modelo)
    
    # Iniciar aplicación
    ventana.mainloop()
    
    # Manejo de excepciones en caso de la existencia de algun error
except FileNotFoundError:
    messagebox.showerror("Error", "No se encontró el archivo 'heart.csv'.")
except Exception as e:
    messagebox.showerror("Error", f"Error al inicializar la aplicación: {str(e)}")
