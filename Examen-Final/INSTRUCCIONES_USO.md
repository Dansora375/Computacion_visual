# INSTRUCCIONES DE USO - Sistema de Detección de Postura

## 🚀 Instalación Rápida

### Opción 1: Instalación Automática (Windows)
```bash
# Hacer doble clic en:
install.bat
```

### Opción 2: Instalación Manual
```bash
# Instalar dependencias
pip install -r requirements.txt

# Probar sistema
python test_system.py

# Ejecutar programa principal
python main.py
```

## 📋 Antes de Empezar

1. **Verificar cámara**: Asegúrate de que tu cámara web funcione
2. **Iluminación**: Usa buena iluminación frontal (evita contraluz)
3. **Distancia**: Mantente a 60-100cm de la cámara
4. **Posición**: Asegúrate de que tu torso completo sea visible

## 🎯 Cómo Usar el Sistema

### 1. Iniciar el Programa
```bash
python main.py
```

### 2. Entender la Interfaz

**Ventana Principal (Cámara):**
- **Verde "POSTURA CORRECTA"**: Tu postura está bien ✅
- **Rojo "MALA POSTURA"**: Se detectan problemas ❌
- Lista de problemas específicos detectados

**Ventana 3D (aparece automáticamente):**
- Se abre cuando hay mala postura por >3 segundos
- Modelo interactivo de postura correcta
- **Mouse**: Rotar vista
- **Rueda**: Zoom in/out
- **N/P**: Cambiar entre modelos (si hay múltiples)
- **Espacio**: Pausar/reanudar alternancia automática

**Dashboard de Estadísticas:**
- Presiona **'S'** para abrir el dashboard
- Actualización automática cada segundo
- Gráficos de distribución de tiempo y problemas detectados
- Botón "Volver a Cámara" para regresar a la detección

### 3. Controles del Teclado

**Durante la detección:**
- **Q**: Salir del programa
- **S**: Abrir dashboard de estadísticas
- **R**: Reiniciar estadísticas de la sesión actual
### 4. Criterios de Detección

El sistema detecta:
- **Cabeza adelantada**: "Text neck" típico de pantallas
- **Cabeza inclinada hacia abajo**: Mirando demasiado hacia la pantalla  
- **Hombros desalineados**: Un hombro más alto que otro
- **Hombros levantados**: Elevación excesiva por tensión
- **Columna encorvada**: Espalda muy inclinada hacia adelante
- **Cuerpo inclinado hacia adelante**: Encorvamiento frontal general

### 5. Sistema de Calibración Personal

**Proceso automático (2 segundos):**
1. Al iniciar, mantén una **POSTURA CORRECTA**
2. El sistema aprende tu anatomía específica
3. Ajusta los umbrales de detección a tu cuerpo
4. Después detecta cambios basados en TU postura ideal

### 6. Dashboard de Estadísticas

**Cómo acceder:**
- Presiona **'S'** durante la detección
- Se pausa la cámara y se abre el dashboard

**Información mostrada:**
- Tiempo total de sesión
- Porcentaje de tiempo con buena/mala postura
- Número total de alertas
- Gráfico de tipos de problemas detectados
- Distribución de tiempo en forma circular

**Funciones disponibles:**
- **Actualización automática**: Cada segundo sin presionar botones
- **Exportar CSV**: Guardar datos para análisis posterior
- **Reiniciar**: Borrar estadísticas actuales
- **Volver a Cámara**: Regresar a la detección

### 7. Cómo Lograr Postura Correcta

**✅ Postura Ideal:**
- Cabeza alineada sobre los hombros
- Hombros relajados y nivelados
- Espalda recta contra el respaldo
- Pies planos en el suelo
- Codos a 90° (si están visibles)

**❌ Evitar:**
- Inclinar cabeza hacia pantalla
- Encorvarse hacia adelante
- Hombros elevados o desiguales
- Sentarse en el borde de la silla

## 🔧 Resolución de Problemas

### "No se puede abrir la cámara"
- Cerrar otras apps que usen la cámara (Zoom, Teams, etc.)
- Verificar permisos de cámara en Windows
- Probar con `python test_system.py`

### "Error importando MediaPipe"
- Ejecutar: `pip install --upgrade mediapipe`
- Si persiste: `pip install mediapipe==0.10.7`

### "La detección no funciona bien"
- Verificar iluminación (evitar sombras)
- Ajustar distancia a la cámara
- Asegurar que el torso completo sea visible

### "El modelo 3D no aparece"
- Esperar 3+ segundos con mala postura
- Verificar que Vedo se instaló correctamente
- Probar con `python test_system.py`

## ⚡ Consejos de Uso

1. **Calibración automática**: El sistema se calibra automáticamente en los primeros 2 segundos
2. **Sensibilidad personalizada**: Los umbrales se adaptan a tu anatomía específica
3. **Persistencia**: Solo se activa la alerta 3D después de 3 segundos de mala postura
4. **Multitarea**: Puedes usar el sistema mientras trabajas en otras ventanas
5. **Estadísticas**: Usa 'S' para ver tu progreso sin interrumpir la sesión
6. **Modelos múltiples**: Si tienes varios modelos 3D, usa N/P para alternar entre ellos

## 🎨 Personalización

### Modelos 3D Personalizados
- Ver archivo `MODELOS_3D_GUIA.md`
- Descargar modelos de Sketchfab, TurboSquid, etc.
- Colocar archivos .obj, .ply, .stl en carpeta `models/`

### Ajustar Sensibilidad
Editar valores en `posture_detector.py`:
```python
self.HEAD_FORWARD_THRESHOLD = 15  # Reducir para más sensibilidad
self.SHOULDER_SLOPE_THRESHOLD = 10
self.SPINE_CURVE_THRESHOLD = 20
```

## 📊 Información Técnica

- **Detección**: MediaPipe Pose (Google)
- **Procesamiento**: 30 FPS aproximadamente
- **Resolución**: 640x480 (ajustable)
- **Latencia**: <100ms típicamente
- **Precisión**: ~95% en condiciones ideales

## 🆘 Soporte

Si tienes problemas:
1. Ejecutar `python test_system.py` para diagnóstico
2. Verificar que todas las dependencias estén instaladas
3. Comprobar que la cámara funciona en otras aplicaciones
4. Revisar la documentación en README.md
