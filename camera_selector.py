import tkinter as tk
from tkinter import ttk, messagebox
import cv2
from PIL import Image, ImageTk
from bubble_camera import BubbleCamWindow


class CameraApp:
    """Interfaz principal para selección y configuración de cámaras"""
    
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