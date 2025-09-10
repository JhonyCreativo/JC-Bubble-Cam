import tkinter as tk
from tkinter import messagebox
import cv2
from PIL import Image, ImageTk, ImageDraw, ImageFilter
import threading
import time
import ctypes


class BubbleCamWindow:
    """Ventana flotante arrastrable para Bubble Cam con calidad HD optimizada"""
    
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
        
        # Configurar ventana circular perfecta con transparencia optimizada
        self.bubble_size = 300  # Tamaño aumentado para aprovechar calidad HD
        self.bubble_window.geometry(f"{self.bubble_size}x{self.bubble_size}+100+100")
        self.bubble_window.resizable(False, False)
        self.bubble_window.attributes('-topmost', True)  # Siempre visible
        self.bubble_window.overrideredirect(True)  # Sin bordes del sistema
        self.bubble_window.configure(bg='#010101')  # Fondo casi negro para transparencia
        self.bubble_window.attributes('-transparentcolor', '#010101')  # Hacer fondo transparente
        
        # Crear canvas optimizado para forma circular perfecta sin fondo
        self.canvas = tk.Canvas(
            self.bubble_window,
            width=self.bubble_size,
            height=self.bubble_size,
            bg='#010101',  # Mismo color transparente que la ventana
            highlightthickness=0,
            bd=0
        )
        self.canvas.pack()
        
        # Aplicar forma circular después de que la ventana esté lista
        self.bubble_window.after(100, self.apply_circular_shape)
        
        # Crear área de video circular completamente transparente
        self.video_label = tk.Label(
            self.canvas, 
            bg='#010101',  # Mismo color transparente que la ventana
            text="",  # Sin texto inicial
            bd=0,
            highlightthickness=0
        )
        self.video_canvas_item = self.canvas.create_window(
            self.bubble_size//2, 
            self.bubble_size//2, 
            window=self.video_label
        )
        
        # Configurar eventos de arrastre
        self.video_label.bind('<Button-1>', self.start_drag)
        self.video_label.bind('<B1-Motion>', self.do_drag)
        self.video_label.bind('<Double-Button-1>', self.close_bubble)  # Doble clic para cerrar
        
        # Iniciar cámara
        self.start_camera()
    
    def apply_circular_shape(self):
        """Aplica forma circular perfecta a la ventana con bordes optimizados y sin latencia"""
        try:
            # Obtener el handle de la ventana
            hwnd = self.bubble_window.winfo_id()
            
            # Crear región circular perfecta con margen mínimo para bordes suaves
            margin = 1  # Margen mínimo para suavizado
            hrgn = ctypes.windll.gdi32.CreateEllipticRgn(
                margin, margin, 
                self.bubble_size - margin, 
                self.bubble_size - margin
            )
            
            # Aplicar la región a la ventana de forma inmediata
            ctypes.windll.user32.SetWindowRgn(hwnd, hrgn, False)  # False para evitar redibujado inmediato
            
            # Aplicar efectos de suavizado optimizados
            self.apply_window_smoothing(hwnd)
            
            # Forzar actualización única
            ctypes.windll.user32.UpdateWindow(hwnd)
            
        except Exception as e:
            print(f"Error aplicando forma circular: {e}")
    
    def apply_window_smoothing(self, hwnd):
        """Aplica suavizado adicional a la ventana"""
        try:
            # Habilitar composición de ventana para mejor antialiasing
            ctypes.windll.dwmapi.DwmEnableComposition(1)
            
            # Configurar atributos de ventana para mejor renderizado
            DWMWA_NCRENDERING_POLICY = 2
            DWMNCRP_ENABLED = 2
            ctypes.windll.dwmapi.DwmSetWindowAttribute(
                hwnd, 
                DWMWA_NCRENDERING_POLICY, 
                ctypes.byref(ctypes.c_int(DWMNCRP_ENABLED)), 
                ctypes.sizeof(ctypes.c_int)
            )
            
        except Exception as e:
            print(f"Error aplicando suavizado: {e}")
        
    def start_drag(self, event):
        """Inicia el arrastre de la ventana"""
        self.start_x = event.x_root - self.bubble_window.winfo_x()
        self.start_y = event.y_root - self.bubble_window.winfo_y()
        
    def do_drag(self, event):
        """Realiza el arrastre de la ventana"""
        x = event.x_root - self.start_x
        y = event.y_root - self.start_y
        self.bubble_window.geometry(f"+{x}+{y}")
        
    def start_camera(self, camera_index=None):
        """Inicia la cámara con configuración HD optimizada para baja latencia"""
        if camera_index is not None:
            self.camera_index = camera_index
            
        try:
            # Inicializar cámara con índice específico y configuración rápida
            self.cap = cv2.VideoCapture(self.camera_index, cv2.CAP_DSHOW)  # DirectShow para Windows
            
            if not self.cap.isOpened():
                # Mostrar placeholder temporal sin texto para evitar distorsión
                self.video_label.config(image="", text="")
                return
                
            # Configuración HD optimizada para baja latencia
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)  # HD 720p width
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)   # HD 720p height
            self.cap.set(cv2.CAP_PROP_FPS, 60)             # 60 FPS para menor latencia
            self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 0)       # Sin buffer para latencia mínima
            # Configuraciones adicionales para velocidad
            self.cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M','J','P','G'))
            self.cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.75)  # Exposición más rápida
            self.cap.set(cv2.CAP_PROP_AUTOFOCUS, 0)         # Desactivar enfoque automático para velocidad
            
            self.is_running = True
            
            # Iniciar hilo de video
            self.video_thread = threading.Thread(target=self.update_video, daemon=True)
            self.video_thread.start()
            
        except Exception as e:
            self.video_label.config(text=f"Error: {str(e)}")
            
    def create_circular_image(self, image_pil):
        """Crea una imagen circular perfecta con transparencia total y bordes limpios"""
        final_size = self.bubble_size
        border_width = 2  # Borde más delgado para mayor claridad
        
        # Recorte cuadrado desde el centro
        original_width, original_height = image_pil.size
        crop_size = min(original_width, original_height)
        
        left = (original_width - crop_size) // 2
        top = (original_height - crop_size) // 2
        image_cropped = image_pil.crop((left, top, left + crop_size, top + crop_size))
        
        # Redimensionar video directamente al tamaño final
        video_image = image_cropped.resize((final_size, final_size), Image.Resampling.LANCZOS)
        video_rgba = video_image.convert('RGBA')
        
        center = final_size // 2
        radius = center - border_width
        
        # === CREAR MÁSCARA CIRCULAR PERFECTA ===
        mask = Image.new('L', (final_size, final_size), 0)
        mask_draw = ImageDraw.Draw(mask)
        
        # Círculo con bordes suaves
        mask_draw.ellipse((center - radius, center - radius,
                          center + radius, center + radius), fill=255)
        
        # Suavizado mínimo para bordes limpios
        mask = mask.filter(ImageFilter.GaussianBlur(radius=0.8))
        
        # === CREAR IMAGEN FINAL COMPLETAMENTE TRANSPARENTE ===
        result = Image.new('RGBA', (final_size, final_size), (0, 0, 0, 0))
        
        # Aplicar máscara directamente al video
        video_rgba.putalpha(mask)
        
        # Pegar video con transparencia perfecta
        result.paste(video_rgba, (0, 0), video_rgba)
        
        # === AGREGAR BORDE BLANCO SIMPLE ===
        border_draw = ImageDraw.Draw(result)
        
        # Borde circular blanco simple
        border_draw.ellipse((center - radius - 1, center - radius - 1,
                            center + radius + 1, center + radius + 1),
                           outline=(255, 255, 255, 200), width=2)
        
        return result
    
    def update_video(self):
        """Actualiza el video circular en la burbuja con máscara de recorte perfecta"""
        frame_count = 0
        
        while self.is_running and self.cap and self.cap.isOpened():
            try:
                ret, frame = self.cap.read()
                if ret:
                    frame_count += 1
                    
                    # Procesar frames optimizado para reducir latencia
                    if frame_count % 3 == 0:  # Procesar cada 3 frames para reducir latencia
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
                            
                time.sleep(0.016)  # ~60 FPS para reducir latencia
                
            except Exception as e:
                print(f"Error en video de burbuja: {e}")
                break
                
    def update_video_label(self, image_tk):
        """Actualiza el label de video de forma thread-safe y optimizada"""
        if self.is_running and self.video_label:
            # Actualización optimizada sin configuraciones innecesarias
            self.video_label.configure(image=image_tk)
            self.video_label.image = image_tk  # Mantener referencia para evitar garbage collection
            
    def close_bubble(self):
        """Cierra la ventana burbuja"""
        self.is_running = False
        
        if self.cap:
            self.cap.release()
            
        if self.bubble_window:
            self.bubble_window.destroy()