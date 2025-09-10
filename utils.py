import os
import cv2

# Configuraciones de optimización de rendimiento
os.environ['OPENCV_VIDEOIO_MSMF_ENABLE_HW_TRANSFORMS'] = '0'
os.environ['OPENCV_VIDEOIO_PRIORITY_MSMF'] = '0'
os.environ['OPENCV_VIDEOIO_PRIORITY_DSHOW'] = '1'


def get_camera_index_from_selection(selected_camera):
    """Extrae el índice de cámara de la selección del usuario"""
    try:
        if "defecto" in selected_camera.lower():
            return 0
        else:
            return int(selected_camera.split()[-1])
    except:
        return 0


def configure_camera_for_preview(cap):
    """Configura la cámara para vista previa optimizada"""
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    cap.set(cv2.CAP_PROP_FPS, 30)
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)


def configure_camera_for_bubble(cap):
    """Configura la cámara para Bubble Cam con máxima calidad y mínima latencia"""
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)  # HD 720p width
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)   # HD 720p height
    cap.set(cv2.CAP_PROP_FPS, 60)             # 60 FPS para menor latencia
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 0)       # Sin buffer para latencia mínima
    cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M','J','P','G'))
    cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.75)  # Exposición más rápida
    cap.set(cv2.CAP_PROP_AUTOFOCUS, 0)         # Desactivar enfoque automático


def configure_camera_for_detection(cap):
    """Configura la cámara para detección rápida"""
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
    cap.set(cv2.CAP_PROP_FPS, 15)
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)


def detect_available_cameras():
    """Detecta las cámaras disponibles en el sistema"""
    available_cameras = []
    common_indices = [0, 1]  # Índices más comunes
    
    print("Iniciando detección rápida de cámaras...")
    
    for i in common_indices:
        try:
            cap = cv2.VideoCapture(i, cv2.CAP_DSHOW)
            configure_camera_for_detection(cap)
            
            if cap.isOpened():
                ret, frame = cap.read()
                if ret and frame is not None and frame.size > 0:
                    available_cameras.append(f"Cámara {i}")
                    print(f"✓ Cámara {i} detectada")
            cap.release()
        except Exception as e:
            print(f"Error al probar cámara {i}: {e}")
    
    # Si no se encuentran cámaras, agregar opción por defecto
    if not available_cameras:
        available_cameras = ["Cámara por defecto"]
        print("Usando cámara por defecto")
    
    print(f"Detección completada. Cámaras: {available_cameras}")
    return available_cameras


def print_app_info():
    """Imprime información de la aplicación"""
    print("🚀 Iniciando JC Bubble Cam...")
    print("📱 Sistema de cámara flotante optimizado")
    print("✨ Versión: 2.0 - Código reestructurado")