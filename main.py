import tkinter as tk
from utils import print_app_info
from camera_selector import CameraApp





def main_classic():
    """Función principal con interfaz clásica (Tkinter)"""
    try:
        print("🚀 Iniciando JC Bubble Cam...")
        print("📱 Cargando interfaz clásica...")
        
        # Crear ventana principal
        root = tk.Tk()
        root.withdraw()  # Ocultar ventana hasta que esté lista
        
        # Crear aplicación usando el módulo camera_selector
        app = CameraApp(root)
        
        # Iniciar bucle principal
        root.mainloop()
        
    except Exception as e:
        print(f"❌ Error al iniciar la aplicación: {e}")
        from tkinter import messagebox
        messagebox.showerror("Error", f"Error al iniciar la aplicación: {str(e)}")

def main():
    """Función principal que maneja la selección de interfaz"""
    try:
        # Intentar usar interfaz moderna primero
        try:
            import modern_ui
            print("🎨 Usando interfaz moderna...")
            modern_ui.main()
        except ImportError:
            print("⚠️ Interfaz moderna no disponible, usando clásica...")
            main_classic()
        except Exception as e:
            print(f"⚠️ Error en interfaz moderna: {e}")
            print("🔄 Cambiando a interfaz clásica...")
            main_classic()
            
    except Exception as e:
        print(f"❌ Error crítico: {e}")
        from tkinter import messagebox
        messagebox.showerror("Error Crítico", f"No se pudo iniciar la aplicación: {str(e)}")

if __name__ == "__main__":
    print_app_info()
    main()