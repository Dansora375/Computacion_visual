# Sistema de Detección de Postura Corporal

## Descripción
Sistema que detecta si un usuario está sentado con una postura correcta o incorrecta usando la cámara del computador en tiempo real. Desarrollado en Python con OpenCV, MediaPipe y Vedo.

## Funcionalidades
- Análisis de postura corporal en tiempo real mediante cámara
- Detección de mala postura (encorvado, hombros desalineados, etc.)
- Advertencia visual cuando se detecta mala postura
- Visualización 3D interactiva de la postura correcta
- **Modelo 3D rotable con mouse y zoom**
- **🔄 Soporte para múltiples modelos 3D con alternancia automática**
- **🎮 Controles interactivos (N/P para cambiar modelos, Espacio para pausar)**

## Instalación
1. Instalar dependencias:
```bash
pip install -r requirements.txt
```

2. Ejecutar el sistema:
```bash
python main.py
```

## Estructura del proyecto
- `main.py`: Archivo principal que ejecuta el sistema
- `posture_detector.py`: Módulo de detección de postura
- `pose_3d_visualizer.py`: Módulo de visualización 3D con alternancia
- `models/`: Carpeta para modelos 3D personalizados
- `requirements.txt`: Dependencias del proyecto
- `MULTIPLES_MODELOS_GUIA.md`: Guía para múltiples modelos
- `MODELOS_3D_GUIA.md`: Guía para descargar modelos

## Uso Básico
- Al ejecutar, se abrirán dos ventanas:
  1. Cámara en tiempo real con análisis de postura
  2. Visualizador 3D (aparece cuando se detecta mala postura)
- Presiona 'q' para salir del programa

## 🎮 Controles Avanzados (Ventana 3D)
Cuando hay múltiples modelos disponibles:
- **N**: Siguiente modelo
- **P**: Modelo anterior  
- **Espacio**: Pausar/reanudar alternancia automática
- **Mouse**: Rotar vista, zoom con rueda, pan con click derecho

## Modelos 3D
Si deseas usar un modelo 3D más realista, coloca archivos .obj, .ply o .stl en la carpeta `models/`
