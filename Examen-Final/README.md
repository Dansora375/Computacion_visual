# 📋 EXAMEN FINAL - COMPUTACIÓN VISUAL
## Sistema Inteligente de Detección y Corrección de Postura Corporal

---

## 👤 Datos del Estudiante

**Nombre completo:** Daniel Felipe Soracipa Torres

**Número de documento:** 1001051472

**Correo institucional:** dsoracipa@unal.edu.co

---

## 📌 Introducción del Problema y Contexto

### Contexto Global y Relevancia Actual
La digitalización masiva del trabajo y la educación, acelerada por la pandemia global, ha transformado radicalmente nuestros hábitos laborales. Millones de personas pasan entre 8-12 horas diarias frente a pantallas, convirtiendo el escritorio en el nuevo "campo de batalla" para la salud postural.

### Problema Identificado: La Crisis Postural Silenciosa
En la era digital actual, el trabajo prolongado frente a computadores ha generado una **epidemia silenciosa de problemas posturales** que afecta a más del 86% de trabajadores de oficina según estudios recientes. Las malas posturas durante largas jornadas laborales y de estudio generan:

#### Impactos Físicos Inmediatos:
- **Dolor cervical y lumbar crónico** (presente en 75% de trabajadores remotos)
- **Síndrome del túnel carpiano** y lesiones por esfuerzo repetitivo
- **Fatiga visual y dolores de cabeza** (síndrome visual del computador)
- **Problemas de circulación sanguínea** y entumecimiento de extremidades
- **Tensión muscular** en hombros, cuello y espalda

#### Consecuencias a Largo Plazo:
- **Deformaciones permanentes** de la columna vertebral
- **Reducción de la productividad y concentración** hasta en un 40%
- **Aumento de ausentismo laboral** por problemas músculo-esqueléticos
- **Costos médicos elevados** para individuos y empresas
- **Deterioro de la calidad de vida** y bienestar general


---

## 🎯 Justificación de la Solución

### ¿Por qué Computación Visual es la Respuesta?

#### 1. **Revolución en la Accesibilidad**
La computación visual democratiza el acceso a la corrección postural. Mientras que las soluciones tradicionales requieren:
- Equipos especializados costosos ($500-$2000)
- Consultas médicas periódicas
- Sensores corporales invasivos

**Nuestra solución solo necesita:**
- Una cámara web estándar (presente en 95% de dispositivos)
- Software gratuito y de código abierto
- Sin hardware adicional ni instalaciones complejas

#### 2. **Ventajas Tecnológicas Únicas**

##### ⚡ **Detección en Tiempo Real**
- **Monitoreo continuo**: Supervisión sin interrumpir el flujo de trabajo
- **Respuesta instantánea**: Alertas en menos de 200ms cuando se detecta mala postura
- **Adaptación dinámica**: El sistema aprende y se ajusta a los patrones del usuario

##### 🔍 **Análisis No Invasivo**
- **Privacidad preservada**: Todo el procesamiento es local, sin envío de datos

##### 🎯 **Precisión Científica**
- **33 puntos corporales**: Análisis detallado usando MediaPipe de Google

##### 🧠 **Inteligencia Adaptativa**
- **Aprendizaje automático**: Reduce falsos positivos con el tiempo
- **Filtrado temporal**: Evita alertas por movimientos momentáneos

#### 3. **Innovación en Retroalimentación Visual**

##### 🏗️ **Modelos 3D Interactivos**
- **Referencia visual clara**: Comparación directa entre postura actual e ideal
- **Múltiples ángulos**: Navegación 360° para comprensión completa

#### 4. **Impacto Social y Económico**

##### 💪 **Prevención vs. Tratamiento**
- **Educación continua**: Enseña buenos hábitos posturales de forma natural
- **Reducción de costos médicos**: Prevención temprana evita tratamientos costosos


---

## 🧠 Selección e Integración de Talleres

### Talleres Seleccionados y su Rol en la Solución

#### 1. 📹 **Taller: Cámara en Vivo con YOLO y OpenCV**
**Integración en el proyecto:**
- **Captura de video en tiempo real**: Implementación del sistema de cámara web para monitoreo continuo
- **Procesamiento de frames**: Aplicación de técnicas de OpenCV para el análisis frame por frame
- **Detección de objetos**: Adaptación de conceptos de detección para identificar puntos corporales clave
- **Interacción por teclado**: Control del sistema mediante eventos de teclado para calibración y configuración

#### 2. 🔄 **Taller: Jerarquías y Transformaciones**
**Integración en el proyecto:**
- **Transformaciones 3D**: Aplicación de rotaciones y traslaciones en los modelos 3D de postura correcta
- **Estructuras jerárquicas**: Organización de las articulaciones corporales en relaciones padre-hijo (cuello-cabeza, torso-hombros)
- **Movimiento relativo**: Análisis de cómo el movimiento de una articulación afecta la posición de las articulaciones dependientes
- **Control interactivo**: Implementación de controles para rotar y manipular la visualización 3D de referencia

#### 3. 🎯 **Taller: Estructuras y Modelos 3D**
**Integración en el proyecto:**
- **Carga de modelos .OBJ**: Implementación en Python usando bibliotecas como Vedo para cargar modelos de posturas correctas
- **Manipulación de mallas 3D**: Gestión de vértices, caras y aristas para la visualización de referencias posturales
- **Visualización interactiva**: Creación de un entorno 3D navegable que muestra la postura ideal
- **Alternancia de modelos**: Sistema que permite cambiar entre diferentes modelos 3D de referencia

#### 4. 📊 **Taller: Sistema de Monitoreo Inteligente con Dashboard**
**Integración en el proyecto:**
- **Detección inteligente con cámara**: Adaptación de técnicas de detección de objetos para identificar posturas incorrectas
- **Panel de estadísticas**: Implementación de un dashboard que muestra métricas de sesión y análisis postural
- **Registro de eventos**: Sistema de logging que documenta detecciones de mala postura y patrones temporales
- **Interfaz de monitoreo**: Creación de una interfaz que permite supervisar el estado postural en tiempo real

#### 5. 📈 **Taller: Visualización de Datos en Tiempo Real**
**Integración en el proyecto:**
- **Gráficos de estadísticas**: Implementación de visualizaciones que muestran distribución de tiempo en posturas correctas/incorrectas
- **Representación visual de datos**: Creación de gráficos de barras y circulares para análisis de patrones posturales
- **Actualización de datos**: Sistema que permite actualizar y visualizar nuevas estadísticas de sesión
- **Dashboard interactivo**: Interface que combina múltiples tipos de gráficos para análisis comprehensivo

---

## 🏗️ Arquitectura de Solución

### Propuesta General del Sistema

El sistema funciona mediante un flujo de trabajo integrado que combina:

1. **Captura y análisis en tiempo real** de la postura del usuario
2. **Calibración personal** para establecer umbrales adaptativos
3. **Detección inteligente** de múltiples tipos de mala postura
4. **Retroalimentación visual inmediata** mediante modelos 3D
5. **Análisis estadístico** del comportamiento postural del usuario

### Diagrama de Funcionamiento

### Diagrama de Arquitectura (Mermaid)

```mermaid
flowchart TD
  subgraph "Interface de Usuario"
    PDB[PostureDashboard<br/>(dashboard.py)]
  end

  subgraph "Visualización 3D"
    P3DV[Pose3DVisualizer<br/>(pose_3d_visualizer.py)]
  end

  subgraph "Detección"
    PD[PostureDetector<br/>(posture_detector.py)]
  end

  subgraph "Estadísticas"
    PS[PostureStatistics<br/>(posture_statistics.py)]
  end

  subgraph "Core"
    PAS[PostureAnalysisSystem<br/>(main.py)]
    CAM[Cámara Web<br/>(Video Stream)]
  end

  CAM -->|frames| PD
  PD -->|update_posture_state()| PS
  PD -->|start_session(), end_session()| PS
  PD -->|detect_posture()| PAS
  PAS -->|show() / pause_camera_and_show_stats()| PDB
  PAS -->|show_correct_posture()| P3DV
  PDB -->|get_statistics_summary()| PS
  PDB -->|export_to_csv()| PS

  %% Relaciones de control
  PAS -->|setup_camera()| PD
  PAS -->|resume_camera_detection()| PDB
  PAS -->|start_session()| PS
  PAS -->|end_session()| PS
  PD -->|detect_posture()| PAS
  PS -->|update_statistics()| PDB
  PDB -->|show_statistics()| PS
  P3DV -->|show_correct_posture()| PAS
```

### Relación entre Módulos

- **main.py**: Coordinador principal que integra todos los módulos
- **posture_detector.py**: Motor de detección usando MediaPipe y OpenCV
- **pose_3d_visualizer.py**: Sistema de visualización 3D con Vedo
- **posture_statistics.py**: Recolección y análisis de datos estadísticos
- **dashboard.py**: Interface gráfica para visualización de estadísticas

---

## 🎬 Evidencia de Funcionamiento

### Detección de Postura en Tiempo Real con aviso de mala postura y Modelo 3D
[ESPACIO PARA AGREGAR GIF DE DETECCIÓN DE POSTURA]

### Dashboard de Estadísticas
[ESPACIO PARA AGREGAR GIF DEL DASHBOARD DE ESTADÍSTICAS]

### Video Demostrativo Completo
[ESPACIO PARA AGREGAR ENLACE AL VIDEO]

---

## ⚙️ Explicación Técnica del Funcionamiento

### Arquitectura del Sistema

#### Módulo de Detección (posture_detector.py)
- **MediaPipe Integration**: Utiliza MediaPipe Pose para detectar 33 puntos corporales clave
- **Calibración Personal**: Sistema de 2 segundos que establece la postura de referencia del usuario
- **Análisis de Coordenadas 3D**: Procesa coordenadas X, Y, Z para análisis spatial completo
- **Cálculo de Ángulos**: Determina ángulos entre articulaciones clave (cuello, columna, hombros)
- **Filtrado Temporal**: Implementa filtrado de 5 frames con umbral del 40% para reducir falsos positivos

#### Sistema de Visualización 3D (pose_3d_visualizer.py)
- **Carga de Modelos**: Soporte para formatos .obj, .ply, .stl usando Vedo
- **Control Interactivo**: Navegación con mouse, zoom, y alternancia de modelos
- **Gestión Inteligente**: Respeta el cierre manual del usuario, evita spam de ventanas
- **Múltiples Referencias**: Sistema de alternancia automática entre diferentes modelos posturales

#### Dashboard de Estadísticas (dashboard.py)
- **Interface Tkinter**: Panel de control con botones para navegación
- **Integración Matplotlib**: Gráficos de barras y circulares para análisis visual
- **Exportación CSV**: Capacidad de exportar datos para análisis posterior
- **Control de Sesión**: Pausa y reanuda el sistema de detección

### Módulo de Estadísticas de Postura (posture_statistics.py)
- **Recolección de Datos**: Almacena información sobre la postura del usuario durante la sesión, incluyendo tiempos de buena y mala postura.
- **Historial de Postura**: Mantiene un registro de los últimos estados posturales para análisis.
- **Alertas Generadas**: Cuenta el número de alertas emitidas por mala postura.
- **Exportación de Datos**: Permite guardar las estadísticas en formato CSV para análisis posterior.
- **Resumen de Sesión**: Proporciona un resumen detallado de la sesión, incluyendo porcentajes de tiempo en buena y mala postura.

### Métricas de Detección Implementadas

#### Detecciones Específicas
- ✅ **Cabeza adelantada**: Análisis de coordenadas Z para proyección frontal
- ✅ **Cabeza inclinada**: Detección de ángulo cervical excesivo
- ✅ **Hombros levantados**: Comparación con valores de calibración personal
- ✅ **Hombros desalineados**: Análisis de diferencias de altura bilateral
- ✅ **Columna encorvada**: Cálculo de ángulo de inclinación del torso
- ✅ **Inclinación frontal**: Detección de encorvamiento general del cuerpo

---
## Uso 

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


## Modelos 3D
Si deseas usar un modelo 3D más realista, coloca archivos .obj, .ply o .stl en la carpeta `models/`

---

## 💡 Conclusiones y Reflexiones Personales

### Logros Técnicos Alcanzados

La implementación del sistema de detección y corrección de postura fue un desafío que requirió integrar múltiples disciplinas de computación visual. Desde la detección en tiempo real hasta la visualización 3D y el análisis estadístico, cada componente fue diseñado para trabajar en conjunto de manera eficiente. Este enfoque modular permitió desarrollar un sistema robusto y adaptable.

Uno de los mayores logros fue la personalización del sistema mediante la calibración automática. Este proceso asegura que los umbrales de detección se ajusten a las características únicas de cada usuario, mejorando la precisión y reduciendo los falsos positivos. Además, la capacidad de exportar datos en formato CSV facilita el análisis y seguimiento de las estadísticas posturales.

Finalmente, la arquitectura del sistema, basada en módulos independientes pero interconectados, demostró ser efectiva para el desarrollo y la futura expansión del proyecto. Cada módulo puede evolucionar sin afectar la funcionalidad general, lo que asegura la escalabilidad y mantenimiento del sistema.

### Reflexión Personal sobre el Proceso de Desarrollo

El desarrollo de este proyecto fue una experiencia enriquecedora que me permitió aplicar conocimientos de diferentes áreas de la computación visual. Aprendí la importancia de la interdisciplinariedad, combinando técnicas de visión por computador, diseño de interfaces gráficas y análisis de datos para crear una solución completa.

A lo largo del proceso, enfrenté desafíos como la sincronización de múltiples interfaces y la optimización del rendimiento en tiempo real. Estos obstáculos me enseñaron la importancia de la iteración y la flexibilidad en el diseño de software. Cada problema fue una oportunidad para aprender y mejorar la solución.

Además, este proyecto reforzó la importancia de documentar cada etapa del desarrollo. La documentación detallada no solo facilitó la implementación, sino que también ayudó a comunicar los resultados y decisiones técnicas de manera clara. En el futuro, espero seguir explorando tecnologías emergentes y contribuir al campo de la salud digital preventiva con soluciones innovadoras y accesibles.



---

## Tecnologías Utilizadas

### Bibliotecas y Frameworks
- **OpenCV**: Procesamiento de video y visión por computador
- **MediaPipe**: Detección de poses y landmarks corporales
- **Vedo**: Visualización 3D interactiva
- **Tkinter**: Interfaz gráfica de usuario
- **Matplotlib**: Visualización de datos y gráficos
- **NumPy**: Computación numérica y manejo de arrays
- **Pandas**: Análisis y manipulación de datos


