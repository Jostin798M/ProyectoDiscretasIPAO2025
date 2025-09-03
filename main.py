import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import pandas as pd
from modelo import ModeloPredictor
from interfaz import InterfazPredictor

def main():
    # Crear ventana principal
    root = tk.Tk()
    root.title("Predictor de Enfermedad Cardíaca")
    root.geometry("800x900")
    root.resizable(True, True)
    
    try:
        # Cargar datos y crear modelo
        df = pd.read_csv('heart.csv')
        modelo = ModeloPredictor(df)
        
        # Crear interfaz
        app = InterfazPredictor(root, modelo)
        
        # Iniciar aplicación
        root.mainloop()
        
    except FileNotFoundError:
        messagebox.showerror("Error", "No se encontró el archivo 'heart.csv'. Asegúrate de que esté en la misma carpeta.")
    except Exception as e:
        messagebox.showerror("Error", f"Error al inicializar la aplicación: {str(e)}")

if __name__ == "__main__":
    main()