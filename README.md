# JC Bubble Cam

Aplicación de escritorio para visualización de cámaras web con interfaz moderna desarrollada en Python.

## Características

- 🎥 Detección automática de cámaras disponibles
- 📺 Vista previa en tiempo real
- 🎨 Interfaz moderna con tema oscuro
- 🔄 Selección dinámica de cámaras
- 🚀 Preparado para funcionalidad Bubble Cam (próximamente)

## Requisitos del Sistema

- Python 3.7 o superior
- Cámara web conectada
- Sistema operativo: Windows, macOS, Linux

## Instalación

### Opción 1: Instalación Rápida (Recomendada)
1. **Clonar o descargar el proyecto:**
   ```bash
   git clone <url-del-repositorio>
   cd jc-bubble-cam
   ```
2. Ejecuta el archivo `start.bat` (Windows) - esto creará automáticamente el entorno virtual e instalará las dependencias

### Opción 2: Instalación Manual
1. **Clonar o descargar el proyecto:**
   ```bash
   git clone <url-del-repositorio>
   cd jc-bubble-cam
   ```

2. **Crear entorno virtual:**
   ```bash
   python -m venv venv
   ```

3. **Activar el entorno virtual:**
   ```bash
   # Windows
   venv\Scripts\activate

   # Linux/Mac
   source venv/bin/activate
   ```

4. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

## Uso

### Inicio Rápido
1. **Windows**: Doble clic en `start.bat`
2. **Manual**: 
   ```bash
   # Activa el entorno virtual
   venv\Scripts\activate
   # Ejecuta la aplicación
   python main.py
   ```

### Funcionalidades
1. **Detección automática de cámaras** - La aplicación detecta automáticamente las cámaras disponibles
2. **Selección de cámara** - Usa el menú desplegable para elegir la cámara
3. **Vista previa optimizada** - Haz clic en "Iniciar Cámara" para ver la transmisión en tiempo real
4. **🎥 Bubble Cam Circular Perfecto (Estilo Loom)** - Crea una ventana flotante circular arrastrable en el escritorio con la cámara activa
   - **Borde circular perfecto** - Antialiasing avanzado con supersampling 4x
   - **Fondo completamente transparente** - El escritorio se ve a través de la burbuja
   - **Máscara de recorte inteligente** - Evita distorsión recortando desde el centro
   - **Borde blanco suave** - Sin pixelado, círculo matemáticamente perfecto
   - **Diseño ultra-limpio** - Sin botones visibles, doble clic para cerrar
   - Transparencia real del sistema operativo Windows
   - Ventana siempre visible (topmost)
   - Completamente arrastrable por toda la pantalla
   - Sin bordes rectangulares del sistema
   - Video optimizado en formato circular de 160x160 píxeles
   - Algoritmo anti-distorsión para video perfecto
   - Integración visual perfecta con el escritorio
5. **Interfaz responsiva** - Optimizada para un rendimiento fluido

### Cómo usar Bubble Cam
1. **Selecciona una cámara** en el menú desplegable
2. **Inicia la vista previa** haciendo clic en "Iniciar Cámara"
3. **Abre Bubble Cam** haciendo clic en "🎥 Abrir Bubble Cam"
4. **Disfruta del círculo perfecto sin pixelado**
5. **Arrastra la burbuja** a cualquier posición del escritorio
6. **Cierra cuando termines** haciendo **doble clic** en la burbuja (diseño ultra-limpio)

## Optimizaciones de Rendimiento

- ✅ **Entorno virtual aislado** para evitar conflictos de dependencias
- ✅ **Detección rápida de cámaras** (solo índices comunes 0 y 1)
- ✅ **Procesamiento optimizado de frames** (salto de frames para mejor rendimiento)
- ✅ **Configuración DirectShow** para Windows
- ✅ **Buffer mínimo** para reducir latencia
- ✅ **Variables de entorno OpenCV** optimizadas

## Estructura del Proyecto

```
jc-bubble-cam/
├── main.py              # Aplicación principal
├── requirements.txt     # Dependencias de Python
└── README.md           # Este archivo
```

## Dependencias

- **OpenCV (cv2)**: Captura y procesamiento de video
- **Pillow (PIL)**: Manipulación de imágenes
- **tkinter**: Interfaz gráfica (incluido con Python)
- **numpy**: Operaciones numéricas (dependencia de OpenCV)

## Funcionalidades Implementadas

✅ Detección automática de cámaras  
✅ Interfaz gráfica moderna  
✅ Vista previa en tiempo real  
✅ Selección de cámaras  
✅ Controles de inicio/parada  

## Funcionalidades Futuras

✅ Bubble Cam flotante transparente en escritorio  
🔄 Configuración de resolución  
🔄 Grabación de video  
🔄 Captura de fotos  
🔄 Filtros y efectos  

## Solución de Problemas

### No se detectan cámaras
- Verifica que la cámara esté conectada y funcionando
- Asegúrate de que no esté siendo usada por otra aplicación
- Reinicia la aplicación

### Error al iniciar la cámara
- Comprueba los permisos de la cámara
- Verifica que OpenCV esté instalado correctamente
- Prueba con una cámara diferente

### Problemas de rendimiento
- Cierra otras aplicaciones que usen la cámara
- Reduce la resolución de la cámara
- Actualiza los drivers de la cámara

## Contribuir

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## Contacto

Proyecto Link: [https://github.com/tu-usuario/jc-bubble-cam](https://github.com/tu-usuario/jc-bubble-cam)