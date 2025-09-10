import tkinter as tk
from tkinter import messagebox, ttk
import cv2
from PIL import Image, ImageTk, ImageDraw
import threading
import time
import os

# Optimizaciones de rendimiento
os.environ['OPENCV_VIDEOIO_PRIORITY_MSMF'] = '0'  # Desactivar MSMF para mejor rendimiento
os.environ['OPENCV_VIDEOIO_DEBUG'] = '0'  # Desactivar debug de OpenCV

class BubbleCamWindow:
    """Ventana flotante arrastrable para Bubble Cam"""
    
    def __init__(self, camera_index):
        self.camera_index = camera_index
        self.cap = None
        self.is_running = False
        self.bubble_window = None
        self.video_label = None
        
        # Variables para arrastrar la ventana
        self.start_x = 0
        self.start_y = 0
        
        self.create_bubble_window()
        
    def create_bubble_window(self):
        """Crea la ventana flotante circular estilo Loom con transparencia y diseño elegante"""
        self.bubble_window = tk.Toplevel()
        self.bubble_window.title("JC Bubble Cam")
        
        # Configurar ventana circular con transparencia
        self.bubble_size = 160  # Tamaño ligeramente mayor para mejor calidad
        self.bubble_window.geometry(f"{self.bubble_size}x{self.bubble_size}+100+100")
        self.bubble_window.resizable(False, False)
        self.bubble_window.attributes('-topmost', True)  # Siempre visible
        self.bubble_window.attributes('-transparentcolor', 'black')  # Transparencia real
        self.bubble_window.attributes('-alpha', 0.98)  # Casi opaco para mejor calidad
        self.bubble_window.overrideredirect(True)  # Sin bordes del sistema
        self.bubble_window.configure(bg='black')  # Color que será transparente
        
        # Crear canvas para la forma circular con transparencia
        self.canvas = tk.Canvas(self.bubble_window, 
                               width=self.bubble_size, 
                               height=self.bubble_size,
                               bg='black', highlightthickness=0)
        self.canvas.pack()
        
        # Crear área de video circular (sin borde aquí, se añadirá con PIL)
        self.video_label = tk.Label(self.canvas, bg='black', text="🎥",
                                   fg='white', font=('Arial', 24))
        self.video_canvas_item = self.canvas.create_window(self.bubble_size//2, 
                                                          self.bubble_size//2,
                                                          window=self.video_label)
        
        # Hacer toda la ventana arrastrable (sin botón X)
        self.canvas.bind('<Button-1>', self.start_drag)
        self.canvas.bind('<B1-Motion>', self.drag_window)
        self.canvas.bind('<Double-Button-1>', self.close_bubble)  # Doble clic para cerrar
        self.video_label.bind('<Button-1>', self.start_drag)
        self.video_label.bind('<B1-Motion>', self.drag_window)
        self.video_label.bind('<Double-Button-1>', self.close_bubble)  # Doble clic para cerrar
        
        # Iniciar cámara
        self.start_camera()
        
    def start_drag(self, event):
        """Inicia el arrastre de la ventana"""
        self.start_x = event.x_root - self.bubble_window.winfo_x()
        self.start_y = event.y_root - self.bubble_window.winfo_y()
        
    def drag_window(self, event):
        """Arrastra la ventana"""
        x = event.x_root - self.start_x
        y = event.y_root - self.start_y
        self.bubble_window.geometry(f"+{x}+{y}")
        
    def start_camera(self):
        """Inicia la captura de video para la burbuja"""
        try:
            self.cap = cv2.VideoCapture(self.camera_index, cv2.CAP_DSHOW)
            
            if not self.cap.isOpened():
                self.video_label.config(text="Error: Cámara no disponible")
                return
                
            # Configuración optimizada para burbuja
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
            self.cap.set(cv2.CAP_PROP_FPS, 30)
            self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
            
            self.is_running = True
            
            # Iniciar hilo de video
            self.video_thread = threading.Thread(target=self.update_video, daemon=True)
            self.video_thread.start()
            
        except Exception as e:
            self.video_label.config(text=f"Error: {str(e)}")
            
    def create_circular_image(self, image_pil):
        """Crea una imagen circular con máscara de recorte perfecta y borde suave"""
        # Usar supersampling para antialiasing perfecto
        supersample = 4  # Factor de supersampling
        final_size = self.bubble_size
        work_size = final_size * supersample
        
        # Redimensionar la imagen manteniendo proporción
        original_width, original_height = image_pil.size
        
        # Calcular el recorte cuadrado desde el centro para evitar distorsión
        if original_width > original_height:
            # Imagen horizontal - recortar los lados
            crop_size = original_height
            left = (original_width - crop_size) // 2
            top = 0
            right = left + crop_size
            bottom = crop_size
        else:
            # Imagen vertical - recortar arriba y abajo
            crop_size = original_width
            left = 0
            top = (original_height - crop_size) // 2
            right = crop_size
            bottom = top + crop_size
        
        # Recortar imagen cuadrada desde el centro
        image_cropped = image_pil.crop((left, top, right, bottom))
        
        # Redimensionar al tamaño de trabajo (supersampling)
        image_work = image_cropped.resize((work_size, work_size), Image.Resampling.LANCZOS)
        
        # Crear imagen final con fondo transparente
        final_image = Image.new('RGBA', (work_size, work_size), (0, 0, 0, 0))
        
        # Crear máscara circular perfecta con antialiasing
        mask = Image.new('L', (work_size, work_size), 0)
        draw = ImageDraw.Draw(mask)
        
        # Dibujar círculo con borde blanco suave
        border_width = 8 * supersample  # Borde escalado
        
        # Círculo exterior (borde blanco)
        draw.ellipse((0, 0, work_size, work_size), fill=255)
        
        # Círculo interior (para el video)
        inner_margin = border_width
        draw.ellipse((inner_margin, inner_margin, 
                     work_size - inner_margin, work_size - inner_margin), fill=0)
        
        # Crear máscara para el video
        video_mask = Image.new('L', (work_size, work_size), 0)
        video_draw = ImageDraw.Draw(video_mask)
        video_draw.ellipse((inner_margin, inner_margin, 
                           work_size - inner_margin, work_size - inner_margin), fill=255)
        
        # Aplicar máscara al video
        image_work.putalpha(video_mask)
        
        # Crear borde blanco
        border_image = Image.new('RGBA', (work_size, work_size), (255, 255, 255, 255))
        border_image.putalpha(mask)
        
        # Combinar borde y video
        final_image.paste(border_image, (0, 0), border_image)
        final_image.paste(image_work, (0, 0), image_work)
        
        # Redimensionar al tamaño final con antialiasing
        final_image = final_image.resize((final_size, final_size), Image.Resampling.LANCZOS)
        
        return final_image
    
    def update_video(self):
        """Actualiza el video circular en la burbuja con máscara de recorte perfecta"""
        frame_count = 0
        
        while self.is_running and self.cap and self.cap.isOpened():
            try:
                ret, frame = self.cap.read()
                if ret:
                    frame_count += 1
                    
                    # Procesar cada frame para la burbuja circular
                    if frame_count % 1 == 0:  # Procesar todos los frames
                        # Convertir a RGB primero
                        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                        
                        # Convertir a PIL para procesamiento de máscara
                        image_pil = Image.fromarray(frame_rgb)
                        
                        # Crear imagen circular con recorte perfecto
                        circular_image = self.create_circular_image(image_pil)
                        
                        # Convertir a PhotoImage
                        image_tk = ImageTk.PhotoImage(circular_image)
                        
                        # Actualizar de forma thread-safe
                        if self.bubble_window and self.bubble_window.winfo_exists():
                            self.bubble_window.after(0, self.update_video_label, image_tk)
                        else:
                            break
                            
                time.sleep(0.033)  # ~30 FPS
                
            except Exception as e:
                print(f"Error en video de burbuja: {e}")
                break
                
    def update_video_label(self, image_tk):
        """Actualiza el label de video de forma thread-safe"""
        if self.is_running and self.video_label:
            self.video_label.config(image=image_tk, text="")
            self.video_label.image = image_tk
            
    def close_bubble(self):
        """Cierra la ventana burbuja"""
        self.is_running = False
        
        if self.cap:
            self.cap.release()
            
        if self.bubble_window:
            self.bubble_window.destroy()

class CameraApp:
    def __init__(self, root):
        self.root = root
        self.root.title("JC Bubble Cam - Selector de Cámaras")
        self.root.geometry("800x600")
        self.root.configure(bg='#2c3e50')
        
        # Variables
        self.cap = None
        self.is_running = False
        self.current_frame = None
        self.available_cameras = []
        
        # Configurar interfaz
        self.setup_ui()
        
        # Detectar cámaras disponibles
        self.detect_cameras()
        
        # Iniciar bucle de actualización
        self.update_frame()
        
        # Mostrar ventana
        self.root.deiconify()
        
    def setup_ui(self):
        """Configura la interfaz de usuario"""
        # Frame principal
        main_frame = tk.Frame(self.root, bg='#2c3e50')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Título
        title_label = tk.Label(
            main_frame, 
            text="JC Bubble Cam", 
            font=('Arial', 24, 'bold'),
            fg='#ecf0f1',
            bg='#2c3e50'
        )
        title_label.pack(pady=(0, 20))
        
        # Frame de controles
        controls_frame = tk.Frame(main_frame, bg='#2c3e50')
        controls_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Label y ComboBox para cámaras
        camera_label = tk.Label(
            controls_frame,
            text="Seleccionar Cámara:",
            font=('Arial', 12),
            fg='#ecf0f1',
            bg='#2c3e50'
        )
        camera_label.pack(side=tk.LEFT, padx=(0, 10))
        
        self.camera_var = tk.StringVar()
        self.camera_combo = ttk.Combobox(
            controls_frame,
            textvariable=self.camera_var,
            state="readonly",
            width=30,
            font=('Arial', 10)
        )
        self.camera_combo.pack(side=tk.LEFT, padx=(0, 20))
        self.camera_combo.bind('<<ComboboxSelected>>', self.on_camera_selected)
        
        # Botones
        button_frame = tk.Frame(controls_frame, bg='#2c3e50')
        button_frame.pack(side=tk.RIGHT)
        
        self.start_button = tk.Button(
            button_frame,
            text="Iniciar Cámara",
            command=self.start_camera,
            bg='#27ae60',
            fg='white',
            font=('Arial', 10, 'bold'),
            padx=15,
            pady=5,
            relief=tk.FLAT
        )
        self.start_button.pack(side=tk.LEFT, padx=(0, 10))
        
        self.stop_button = tk.Button(
            button_frame,
            text="Detener Cámara",
            command=self.stop_camera,
            bg='#e74c3c',
            fg='white',
            font=('Arial', 10, 'bold'),
            padx=15,
            pady=5,
            relief=tk.FLAT,
            state=tk.DISABLED
        )
        self.stop_button.pack(side=tk.LEFT, padx=(0, 10))
        
        self.bubble_button = tk.Button(
            button_frame,
            text="Abrir Bubble Cam",
            command=self.open_bubble_cam,
            bg='#3498db',
            fg='white',
            font=('Arial', 10, 'bold'),
            padx=15,
            pady=5,
            relief=tk.FLAT,
            state=tk.DISABLED
        )
        self.bubble_button.pack(side=tk.LEFT)
        
        # Frame para vista previa
        preview_frame = tk.Frame(main_frame, bg='#34495e', relief=tk.SUNKEN, bd=2)
        preview_frame.pack(fill=tk.BOTH, expand=True)
        
        # Label para vista previa
        self.preview_label = tk.Label(
            preview_frame,
            text="Selecciona una cámara para ver la vista previa",
            font=('Arial', 14),
            fg='#bdc3c7',
            bg='#34495e'
        )
        self.preview_label.pack(expand=True)
        
        # Frame inferior con botón cerrar
        bottom_frame = tk.Frame(main_frame, bg='#2c3e50')
        bottom_frame.pack(fill=tk.X, pady=(20, 0))
        
        close_button = tk.Button(
            bottom_frame,
            text="Cerrar Aplicación",
            command=self.close_app,
            bg='#95a5a6',
            fg='white',
            font=('Arial', 12, 'bold'),
            padx=20,
            pady=8,
            relief=tk.FLAT
        )
        close_button.pack(side=tk.RIGHT)
        
        # Status label
        self.status_label = tk.Label(
            bottom_frame,
            text="Aplicación iniciada - Detectando cámaras...",
            font=('Arial', 10),
            fg='#bdc3c7',
            bg='#2c3e50'
        )
        self.status_label.pack(side=tk.LEFT)
        
    def detect_cameras(self):
        """Detecta las cámaras disponibles en el sistema de forma optimizada"""
        self.available_cameras = []
        
        print("Iniciando detección rápida de cámaras...")
        self.status_label.config(text="Detectando cámaras disponibles...")
        
        # Detección optimizada - solo probar índices comunes
        common_indices = [0, 1]  # Reducido a solo los índices más comunes
        
        for i in common_indices:
            try:
                # Configuración optimizada para detección rápida
                cap = cv2.VideoCapture(i, cv2.CAP_DSHOW)
                cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)  # Resolución baja para test
                cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
                cap.set(cv2.CAP_PROP_FPS, 15)  # FPS bajo para test
                
                if cap.isOpened():
                    # Test rápido de lectura
                    cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
                    ret, frame = cap.read()
                    if ret and frame is not None and frame.size > 0:
                        self.available_cameras.append(f"Cámara {i}")
                        print(f"✓ Cámara {i} detectada (rápido)")
                cap.release()
            except Exception as e:
                print(f"Error al probar cámara {i}: {e}")
        
        # Si no se encuentran cámaras, agregar una opción por defecto
        if not self.available_cameras:
            self.available_cameras = ["Cámara por defecto"]
            print("Usando cámara por defecto")
        
        # Actualizar ComboBox
        self.camera_combo['values'] = self.available_cameras
        if self.available_cameras:
            self.camera_combo.current(0)
        
        print(f"Detección completada. Cámaras: {self.available_cameras}")
        self.status_label.config(text=f"Listo - {len(self.available_cameras)} cámara(s)")
    
    def on_camera_selected(self, event):
        """Maneja la selección de cámara"""
        if self.is_running:
            self.stop_camera()
    
    def start_camera(self):
        """Inicia la captura de video de la cámara seleccionada con optimizaciones"""
        selected = self.camera_var.get()
        if not selected:
            messagebox.showwarning("Advertencia", "Por favor selecciona una cámara")
            return
        
        # Extraer índice de cámara
        try:
            if "defecto" in selected.lower():
                camera_index = 0
            else:
                camera_index = int(selected.split()[-1])
        except:
            camera_index = 0
        
        # Inicializar captura
        try:
            # Configuración optimizada de cámara
            self.cap = cv2.VideoCapture(camera_index, cv2.CAP_DSHOW)
            
            if not self.cap.isOpened():
                messagebox.showerror("Error", f"No se pudo abrir la cámara {camera_index}")
                return
            
            # Configuraciones de rendimiento
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
            self.cap.set(cv2.CAP_PROP_FPS, 30)  # FPS optimizado
            self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)  # Buffer mínimo para reducir latencia
            
            # Probar lectura
            ret, frame = self.cap.read()
            if not ret:
                messagebox.showerror("Error", f"No se puede leer de la cámara {camera_index}")
                self.cap.release()
                return
            
            self.is_running = True
            self.start_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)
            self.bubble_button.config(state=tk.NORMAL)
            self.status_label.config(text=f"Cámara {camera_index} activa")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al inicializar la cámara: {str(e)}")
            self.status_label.config(text="Error en cámara")
        
    def stop_camera(self):
        """Detiene la captura de video"""
        self.is_running = False
        if self.cap:
            self.cap.release()
            self.cap = None
        
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.bubble_button.config(state=tk.DISABLED)
        self.status_label.config(text="Cámara detenida")
        
        # Limpiar vista previa
        self.preview_label.config(
            image='',
            text="Selecciona una cámara para ver la vista previa"
        )
        
    def update_frame(self):
        """Actualiza el frame de video en la interfaz con optimizaciones"""
        if self.is_running and self.cap and self.cap.isOpened():
            try:
                ret, frame = self.cap.read()
                if ret:
                    # Redimensionar directamente a tamaño fijo para mejor rendimiento
                    frame_resized = cv2.resize(frame, (400, 300))
                    
                    # Convertir de BGR a RGB
                    frame_rgb = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2RGB)
                    
                    # Convertir a PIL Image y luego a PhotoImage
                    pil_image = Image.fromarray(frame_rgb)
                    photo = ImageTk.PhotoImage(pil_image)
                    
                    # Actualizar label
                    self.preview_label.config(image=photo, text="")
                    self.preview_label.image = photo  # Mantener referencia
            except Exception as e:
                print(f"Error al actualizar frame: {e}")
                self.stop_camera()
        
        # Programar siguiente actualización con intervalo optimizado
        self.root.after(33, self.update_frame)  # ~30 FPS
    
    def open_bubble_cam(self):
        """Abre la ventana flotante Bubble Cam"""
        if not self.is_running:
            messagebox.showwarning("Advertencia", "Primero debes iniciar una cámara")
            return
            
        selected = self.camera_var.get()
        if not selected:
            messagebox.showwarning("Advertencia", "No hay cámara seleccionada")
            return
            
        # Extraer índice de cámara
        try:
            if "defecto" in selected.lower():
                camera_index = 0
            else:
                camera_index = int(selected.split()[-1])
        except:
            camera_index = 0
            
        try:
            # Crear ventana flotante Bubble Cam
            bubble_cam = BubbleCamWindow(camera_index)
            messagebox.showinfo("Bubble Cam", "¡Ventana flotante creada!\n\nPuedes arrastrarla por toda la pantalla.\nUsa el botón ✕ para cerrarla.")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al crear Bubble Cam: {str(e)}")
    
    def close_app(self):
        """Cierra la aplicación"""
        if self.is_running:
            self.stop_camera()
        self.root.quit()
        self.root.destroy()

def main():
    """Función principal"""
    print("Iniciando JC Bubble Cam...")
    
    root = tk.Tk()
    
    # Asegurar que la ventana aparezca
    root.lift()
    root.attributes('-topmost', True)
    root.after_idle(root.attributes, '-topmost', False)
    
    app = CameraApp(root)
    
    # Manejar cierre de ventana
    root.protocol("WM_DELETE_WINDOW", app.close_app)
    
    print("Interfaz gráfica iniciada")
    
    # Iniciar aplicación
    root.mainloop()
    
    print("Aplicación cerrada")

if __name__ == "__main__":
    main()