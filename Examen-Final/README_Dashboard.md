# 🎯 Sistema de Detección de Postura Corporal con Dashboard de Estadísticas

📅 **Fecha:** Julio 2025

## 🔍 Objetivo del Proyecto

Este sistema integra detección de postura corporal en tiempo real con un sistema completo de estadísticas y visualización. Utiliza MediaPipe para análisis postural, incluye calibración personal, y proporciona un dashboard interactivo para monitorear el progreso y los hábitos posturales del usuario.

## 🧠 Conceptos Aplicados

* **Detección de postura en tiempo real**: Usando MediaPipe para análisis de pose 3D
* **Calibración personal**: Sistema adaptativo que aprende la postura correcta del usuario
* **Análisis estadístico**: Recolección y análisis de datos posturales durante la sesión
* **Dashboard interactivo**: Interfaz gráfica con Tkinter y Matplotlib para visualización
* **Procesamiento multihilo**: Separación de detección, visualización 3D y dashboard
* **Exportación de datos**: Sistema automático de generación de reportes en CSV

## 🔧 Herramientas y Entorno

* **Python 3.8+**
* **Frameworks y bibliotecas**:
  * OpenCV - Captura y procesamiento de video
  * MediaPipe - Detección de pose y landmarks 3D
  * Vedo - Visualización 3D interactiva
  * Tkinter - Interfaz gráfica del dashboard
  * Matplotlib - Gráficos y visualización de estadísticas
  * NumPy - Procesamiento numérico

## 📁 Estructura del Proyecto

```
Examen-Final/
├── main.py                    - Script principal del sistema
├── posture_detector.py        - Módulo de detección de postura
├── pose_3d_visualizer.py      - Visualizador 3D de postura correcta
├── posture_statistics.py      - Sistema de recolección de estadísticas
├── dashboard.py               - Dashboard visual interactivo
├── requirements.txt           - Dependencias del proyecto
├── estadisticas/              - Carpeta para archivos CSV exportados
│   └── posture_stats_YYYYMMDD_HHMMSS.csv
├── models/                    - Modelos 3D
│   ├── correct_posture.ply
│   └── correct_posture_optimized.ply
└── README.md                  - Esta documentación
```

## 🚀 Cómo Ejecutar el Sistema

1. **Instalar las dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Ejecutar el sistema**:
   ```bash
   python main.py
   ```

3. **Interactuar con el sistema**:
   * Siéntate con postura correcta al iniciar para calibración
   * El sistema detectará automáticamente cambios posturales
   * Usa las teclas para controlar el sistema:
     - `q` - Salir del sistema
     - `s` - Abrir dashboard de estadísticas  
     - `r` - Reiniciar estadísticas de la sesión

## 📊 Sistema de Estadísticas

### 🔹 Métricas Recolectadas

El sistema registra automáticamente durante la sesión:

* **Tiempo total de sesión**
* **Tiempo en postura correcta vs incorrecta** (con porcentajes)
* **Frecuencia de eventos de mala postura**
* **Tipos específicos de problemas detectados**:
  - Cabeza inclinada hacia abajo
  - Inclinación hacia adelante (encorvamiento)
  - Elevación de hombros
  - Cabeza inclinada lateral
  - Hombros asimétricos
  - Cabeza muy adelantada
* **Número de alertas generadas** (ventanas 3D abiertas)

### 🔹 Dashboard Visual

El dashboard proporciona una interfaz completa con:

1. **Panel Superior - Resumen en Tiempo Real**:
   - Duración de la sesión actual
   - Porcentajes de tiempo en buena/mala postura
   - Contador de alertas generadas

2. **Gráfico de Barras - Tipos de Problemas**:
   - Frecuencia de cada tipo de problema postural detectado
   - Identificación visual de patrones problemáticos

3. **Gráfico Circular - Distribución de Tiempo**:
   - Visualización proporcional del tiempo en buena vs mala postura
   - Indicadores de color para evaluación rápida

4. **Controles del Dashboard**:
   - Actualización manual
   - Exportación de datos a CSV
   - Reinicio de estadísticas
   - Cierre del dashboard

## 💻 Código Relevante

### 📌 Sistema de Estadísticas

```python
class PostureStatistics:
    def __init__(self):
        self.session_start_time = None
        self.good_posture_time = 0.0
        self.bad_posture_time = 0.0
        self.problem_counts = defaultdict(int)
        self.alert_count = 0
    
    def update_posture_state(self, is_good_posture, problem_types=None):
        """Actualiza el estado actual de la postura"""
        # Lógica de actualización temporal y conteo de problemas
    
    def get_statistics_summary(self):
        """Retorna resumen completo de estadísticas"""
        # Cálculos de porcentajes y formateo de duración
```

### 📌 Dashboard Interactivo

```python
class PostureDashboard:
    def _create_charts_section(self):
        """Crea la sección de gráficos"""
        self.figure = Figure(figsize=(12, 6))
        self.ax1 = self.figure.add_subplot(121)  # Gráfico de barras
        self.ax2 = self.figure.add_subplot(122)  # Gráfico circular
    
    def _update_charts(self):
        """Actualiza los gráficos con datos actuales"""
        stats = self.statistics.get_statistics_summary()
        self._create_problems_chart(stats)
        self._create_time_distribution_chart(stats)
```

### 📌 Integración en el Sistema Principal

```python
def run(self):
    # Iniciar estadísticas
    self.statistics.start_session()
    
    while self.running:
        # Detectar postura
        processed_frame, is_bad_posture, posture_issues, calibration_status = self.detector.detect_posture(frame)
        
        # Actualizar estadísticas
        if not calibration_status['calibrating']:
            self.statistics.update_posture_state(not is_bad_posture, posture_issues)
        
        # Manejar controles de teclado
        if key == ord('s'):
            self.dashboard.show()
```

## 📸 Características del Sistema

### 🔹 Calibración Personal
- Calibración automática de 2 segundos al iniciar
- Aprendizaje de la postura correcta específica del usuario
- Umbrales adaptativos basados en medidas personales

### 🔹 Detección Avanzada
- Análisis de 6 tipos diferentes de problemas posturales
- Filtrado temporal para evitar falsos positivos
- Coordenadas 3D para análisis preciso de ángulos

### 🔹 Visualización 3D
- Modelo 3D interactivo de postura correcta
- Apertura automática después de 3 segundos de mala postura
- Control inteligente de ventana (requiere nueva detección después de cierre manual)

### 🔹 Sistema de Estadísticas
- Recolección transparente en tiempo real
- Dashboard con actualización automática cada 2 segundos
- Exportación automática al finalizar sesión
- Formato CSV legible y estructurado

## 📄 Ejemplo de Reporte CSV

```csv
RESUMEN DE SESIÓN
Métrica,Valor
Duración Total,15:32min
Tiempo Buena Postura,12:45min
Tiempo Mala Postura,2:47min
Porcentaje Buena Postura,82.1%
Porcentaje Mala Postura,17.9%
Total de Alertas,8

TIPOS DE PROBLEMAS DETECTADOS
Tipo de Problema,Cantidad
Cabeza Inclinada Hacia Abajo,12
Inclinación Hacia Adelante,8
Elevación de Hombros,5
```

## 🎮 Controles del Sistema

| Tecla | Función |
|-------|---------|
| `q` | Salir del sistema |
| `s` | Abrir dashboard de estadísticas |
| `r` | Reiniciar estadísticas de la sesión |

## 💬 Reflexión Final

Este sistema proporciona una solución completa para el monitoreo postural, combinando:

- **Detección precisa** con calibración personal
- **Análisis estadístico** para identificar patrones
- **Visualización interactiva** para motivación y corrección
- **Reportes automáticos** para seguimiento a largo plazo

La integración de estadísticas permite a los usuarios:
- Identificar sus problemas posturales más frecuentes
- Monitorear mejoras a lo largo del tiempo
- Establecer metas de tiempo en buena postura
- Generar reportes para profesionales de la salud

## 🔄 Flujo de Funcionamiento

1. **Inicio**: Calibración automática con postura correcta
2. **Monitoreo**: Detección continua y actualización de estadísticas
3. **Alertas**: Visualización 3D cuando se detecta mala postura
4. **Análisis**: Dashboard disponible en tiempo real
5. **Finalización**: Resumen automático y exportación de datos

Este enfoque integral hace del sistema una herramienta valiosa tanto para uso personal como profesional en el ámbito de la salud postural.
