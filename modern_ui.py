import customtkinter as ctk
import cv2
from PIL import Image, ImageTk
import threading
import time
import os

# Configurar tema moderno
ctk.set_appearance_mode("dark")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

class ModernCameraApp:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("JC Bubble Cam - Interfaz Moderna")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        # Variables
        self.cameras = []
        self.selected_camera = None
        self.cap = None
        self.is_running = False
        self.bubble_window = None
        
        self.setup_modern_ui()
        self.detect_cameras_fast()
        
    def setup_modern_ui(self):
        """Configura la interfaz moderna con CustomTkinter"""
        # Frame principal con padding
        main_frame = ctk.CTkFrame(self.root)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Título principal
        title_label = ctk.CTkLabel(
            main_frame, 
            text="🎥 JC Bubble Cam",
            font=ctk.CTkFont(size=32, weight="bold")
        )
        title_label.pack(pady=(20, 10))
        
        # Subtítulo
        subtitle_label = ctk.CTkLabel(
            main_frame,
            text="Crea burbujas de cámara flotantes con estilo moderno",
            font=ctk.CTkFont(size=16),
            text_color=("gray70", "gray30")
        )
        subtitle_label.pack(pady=(0, 30))
        
        # Frame de selección de cámara
        camera_frame = ctk.CTkFrame(main_frame)
        camera_frame.pack(fill="x", padx=20, pady=10)
        
        # Label para selección de cámara
        camera_label = ctk.CTkLabel(
            camera_frame,
            text="📹 Seleccionar Cámara:",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        camera_label.pack(pady=(15, 5))
        
        # ComboBox moderno para cámaras
        self.camera_combo = ctk.CTkComboBox(
            camera_frame,
            values=["Detectando cámaras..."],
            command=self.on_camera_selected,
            width=300,
            height=40,
            font=ctk.CTkFont(size=14)
        )
        self.camera_combo.pack(pady=(5, 15))
        
        # Frame de vista previa
        preview_frame = ctk.CTkFrame(main_frame)
        preview_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Label para vista previa
        preview_label = ctk.CTkLabel(
            preview_frame,
            text="👁️ Vista Previa de la Cámara",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        preview_label.pack(pady=(15, 10))
        
        # Canvas para vista previa con esquinas redondeadas
        self.preview_canvas = ctk.CTkLabel(
            preview_frame,
            text="Selecciona una cámara para ver la vista previa",
            width=400,
            height=300,
            corner_radius=15,
            fg_color=("gray80", "gray20")
        )
        self.preview_canvas.pack(pady=(0, 15), expand=True)
        
        # Frame de controles
        controls_frame = ctk.CTkFrame(main_frame)
        controls_frame.pack(fill="x", padx=20, pady=10)
        
        # Botones modernos
        buttons_frame = ctk.CTkFrame(controls_frame, fg_color="transparent")
        buttons_frame.pack(pady=20)
        
        # Botón para abrir burbuja
        self.bubble_button = ctk.CTkButton(
            buttons_frame,
            text="🫧 Abrir Bubble",
            command=self.open_bubble_cam,
            width=200,
            height=50,
            font=ctk.CTkFont(size=16, weight="bold"),
            corner_radius=25
        )
        self.bubble_button.pack(side="left", padx=10)
        
        # Botón para detener
        self.stop_button = ctk.CTkButton(
            buttons_frame,
            text="⏹️ Detener Cámara",
            command=self.stop_camera,
            width=200,
            height=50,
            font=ctk.CTkFont(size=16, weight="bold"),
            corner_radius=25,
            fg_color="#e74c3c",
            hover_color="#c0392b"
        )
        self.stop_button.pack(side="left", padx=10)
        
        # Progress bar para carga
        self.progress_bar = ctk.CTkProgressBar(
            main_frame,
            width=400,
            height=20,
            corner_radius=10
        )
        self.progress_bar.pack(pady=10)
        self.progress_bar.set(0)
        
        # Status label
        self.status_label = ctk.CTkLabel(
            main_frame,
            text="✅ Listo para usar",
            font=ctk.CTkFont(size=14),
            text_color=("green", "lightgreen")
        )
        self.status_label.pack(pady=(5, 20))
        
    def detect_cameras_fast(self):
        """Detección ultra-rápida de cámaras en hilo separado"""
        def detect():
            self.update_status("🔍 Detectando cámaras...", "orange")
            self.progress_bar.set(0.3)
            
            cameras_found = []
            for i in range(2):  # Solo verificar primeras 2 cámaras para mayor velocidad
                try:
                    # Configuración optimizada para detección rápida
                    cap = cv2.VideoCapture(i, cv2.CAP_DSHOW)
                    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 160)
                    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 120)
                    cap.set(cv2.CAP_PROP_FPS, 15)
                    
                    if cap.isOpened():
                        # Test rápido de lectura
                        ret, _ = cap.read()
                        if ret:
                            cameras_found.append(f"Cámara {i}")
                    cap.release()
                    self.progress_bar.set(0.3 + (i + 1) * 0.35)
                except:
                    continue
            
            self.cameras = cameras_found
            
            # Actualizar UI en el hilo principal
            self.root.after(0, self.update_camera_list)
            
        threading.Thread(target=detect, daemon=True).start()
        
    def update_camera_list(self):
        """Actualiza la lista de cámaras en la UI"""
        if self.cameras:
            self.camera_combo.configure(values=self.cameras)
            self.camera_combo.set(self.cameras[0])
            self.update_status(f"✅ {len(self.cameras)} cámara(s) detectada(s)", "green")
            self.progress_bar.set(1.0)
        else:
            self.camera_combo.configure(values=["No se encontraron cámaras"])
            self.update_status("❌ No se encontraron cámaras", "red")
            self.progress_bar.set(0)
            
    def update_status(self, message, color="gray"):
        """Actualiza el mensaje de estado"""
        self.status_label.configure(text=message, text_color=color)
        
    def on_camera_selected(self, selection):
        """Maneja la selección de cámara"""
        if "Cámara" in selection:
            camera_index = int(selection.split()[-1])
            self.selected_camera = camera_index
            self.start_preview()
            
    def start_preview(self):
        """Inicia la vista previa de la cámara"""
        if self.cap:
            self.cap.release()
            
        self.cap = cv2.VideoCapture(self.selected_camera, cv2.CAP_DSHOW)
        self.is_running = True
        self.update_preview()
        
    def update_preview(self):
        """Actualiza la vista previa de la cámara con optimización de rendimiento"""
        if self.is_running and self.cap and self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                # Redimensionar frame para vista previa (optimizado)
                frame = cv2.resize(frame, (320, 240), interpolation=cv2.INTER_LINEAR)
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                
                # Convertir a imagen PIL y luego a PhotoImage (optimizado)
                image_pil = Image.fromarray(frame_rgb)
                image_tk = ImageTk.PhotoImage(image_pil)
                
                # Actualizar canvas
                self.preview_canvas.configure(image=image_tk, text="")
                self.preview_canvas.image = image_tk  # Mantener referencia
                
            # Programar siguiente actualización con menor latencia
            self.root.after(50, self.update_preview)  # ~20 FPS para mejor rendimiento
            
    def open_bubble_cam(self):
        """Abre la ventana de burbuja de cámara con feedback mejorado"""
        if self.selected_camera is not None:
            try:
                self.update_status("🔄 Creando burbuja de cámara...", "orange")
                
                # Cerrar burbuja anterior si existe
                if self.bubble_window:
                    try:
                        self.bubble_window.close_bubble()
                    except:
                        pass
                
                # Importar y crear nueva burbuja
                from main import BubbleCamWindow
                self.bubble_window = BubbleCamWindow(self.selected_camera)
                
                # Feedback de éxito
                self.update_status("🫧 Burbuja de cámara creada exitosamente", "green")
                
                # Actualizar texto del botón
                self.bubble_button.configure(text="🔄 Recrear Bubble")
                
            except Exception as e:
                self.update_status(f"❌ Error al crear burbuja: {str(e)[:50]}...", "red")
        else:
            self.update_status("⚠️ Selecciona una cámara primero", "orange")
            # Hacer parpadear el combo de cámaras
            original_color = self.camera_combo.cget("border_color")
            self.camera_combo.configure(border_color="orange")
            self.root.after(1000, lambda: self.camera_combo.configure(border_color=original_color))
            
    def stop_camera(self):
        """Detiene la cámara"""
        self.is_running = False
        if self.cap:
            self.cap.release()
            self.cap = None
            
        # Limpiar vista previa
        self.preview_canvas.configure(
            image=None, 
            text="Cámara detenida\nSelecciona una cámara para reanudar"
        )
        self.update_status("⏹️ Cámara detenida", "gray")
        
    def run(self):
        """Ejecuta la aplicación"""
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()
        
    def on_closing(self):
        """Maneja el cierre de la aplicación"""
        self.is_running = False
        if self.cap:
            self.cap.release()
        if self.bubble_window:
            try:
                self.bubble_window.close_bubble()
            except:
                pass
        self.root.destroy()

def main():
    """Función principal con interfaz moderna"""
    try:
        app = ModernCameraApp()
        app.run()
    except ImportError:
        print("❌ CustomTkinter no está instalado.")
        print("📦 Instala con: pip install customtkinter")
        print("🔄 Usando interfaz clásica...")
        
        # Fallback a la interfaz original
        import main
        main.main()
    except Exception as e:
        print(f"❌ Error al iniciar la aplicación moderna: {e}")
        print("🔄 Usando interfaz clásica...")
        
        # Fallback a la interfaz original
        import main
        main.main()

if __name__ == "__main__":
    main()