# Sistema de Detección de Postura Corporal - VERSIÓN MEJORADA

## Descripción
Sistema avanzado que detecta si un usuario está sentado con una postura correcta o incorrecta usando la cámara del computador en tiempo real. Desarrollado en Python con OpenCV, MediaPipe y Vedo.

## 🆕 MEJORAS IMPLEMENTADAS

### Sistema de Calibración Personal
- **Calibración automática**: El sistema se calibra con la postura correcta del usuario durante 2 segundos
- **Umbrales adaptativos**: Cada usuario tiene umbrales personalizados basados en su anatomía
- **Detección mejorada**: Mejor precisión al detectar cambios específicos en la postura individual

### Análisis Avanzado de Postura
- **Coordenadas 3D**: Usa las coordenadas X, Y, Z de MediaPipe para análisis en profundidad
- **Ángulos precisos**: Calcula ángulos reales entre articulaciones (cuello, columna, hombros)
- **Detección específica mejorada**: Identifica múltiples tipos de mala postura
- **Filtrado temporal optimizado**: Balance entre sensibilidad y estabilidad (5 frames, 40% umbral)
- **Control inteligente de ventanas**: La ventana 3D respeta el cierre manual del usuario

### Métricas Específicas Detectadas
- ✅ **Cabeza adelantada**: Detecta proyección frontal usando coordenadas Z
- ✅ **Cabeza inclinada hacia abajo**: Detecta cuando miras demasiado hacia la pantalla
- ✅ **Hombros levantados**: Identifica elevación excesiva comparando con calibración
- ✅ **Hombros desalineados**: Detecta diferencias de altura entre hombros
- ✅ **Columna encorvada**: Analiza ángulo de inclinación del torso
- ✅ **Cuerpo inclinado hacia adelante**: Detecta encorvamiento frontal
- ✅ **Ángulo cervical**: Mide la posición de la cabeza respecto al cuello

## Funcionalidades
- Análisis de postura corporal en tiempo real mediante cámara
- **🎯 Calibración personal automática (2 segundos)**
- **📐 Detección precisa con ángulos y coordenadas 3D**
- **🔍 Identificación específica de hombros levantados**
- **🕒 Filtrado temporal para mayor precisión**
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

## Uso Mejorado

### Proceso de Calibración
1. Al ejecutar, mantén una **POSTURA CORRECTA** durante 2 segundos:
   - Espalda recta contra el respaldo
   - Hombros relajados y nivelados
   - Cabeza alineada (no adelantada)
   - Sin encorvarse

2. El sistema se calibrará automáticamente y aprenderá tu postura ideal

3. Después de la calibración, detectará cambios específicos en tu postura

### Ventanas del Sistema
- **Ventana principal**: Cámara en tiempo real con análisis de postura
- **Visualizador 3D**: Aparece cuando se detecta mala postura persistente
- Presiona 'q' para salir del programa

## Mejoras en Precisión

### Antes vs Ahora
| Característica | Versión Anterior | Versión Mejorada |
|---|---|---|
| **Calibración** | ❌ Sin calibración | ✅ Calibración personal automática |
| **Detección cabeza** | ❌ Solo distancia X | ✅ Coordenadas 3D + ángulos |
| **Hombros levantados** | ❌ No detectaba | ✅ Detección específica |
| **Umbrales** | ❌ Fijos para todos | ✅ Adaptativos por usuario |
| **Filtrado** | ❌ Sin filtrado | ✅ Filtrado temporal |
| **Falsos positivos** | ❌ Frecuentes | ✅ Minimizados |

### Tipos de Mala Postura Detectados
- **Cabeza muy adelantada**: Proyección frontal excesiva
- **Cabeza inclinada hacia abajo**: Mirando demasiado hacia la pantalla
- **Hombros desalineados/elevados**: Asimetría o tensión
- **Columna encorvada**: Inclinación excesiva del torso
- **Hombros muy levantados**: Elevación por estrés/tensión
- **Cuerpo inclinado hacia adelante**: Encorvamiento frontal general

### Control de Ventana 3D
- ✅ **Cierre manual respetado**: Si cierras la ventana, no se reabrirá por 10 segundos
- ✅ **Control inteligente**: El usuario decide cuándo ver la guía 3D
- ✅ **Sin spam de ventanas**: Evita múltiples ventanas abriéndose

## 🎮 Controles Avanzados (Ventana 3D)
Cuando hay múltiples modelos disponibles:
- **N**: Siguiente modelo
- **P**: Modelo anterior  
- **Espacio**: Pausar/reanudar alternancia automática
- **Mouse**: Rotar vista, zoom con rueda, pan con click derecho

## Modelos 3D
Si deseas usar un modelo 3D más realista, coloca archivos .obj, .ply o .stl en la carpeta `models/`
