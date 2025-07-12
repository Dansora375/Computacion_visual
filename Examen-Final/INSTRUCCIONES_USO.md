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

### 3. Criterios de Detección

El sistema detecta:
- **Cabeza adelantada**: "Text neck" típico de pantallas
- **Hombros desalineados**: Un hombro más alto que otro
- **Columna encorvada**: Espalda muy inclinada hacia adelante

### 4. Cómo Lograr Postura Correcta

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

1. **Calibración**: Al iniciar, adopta una postura correcta por unos segundos
2. **Sensibilidad**: El sistema es sensible; pequeños movimientos pueden cambiar el estado
3. **Persistencia**: Solo se activa la alerta 3D después de 3 segundos de mala postura
4. **Multitarea**: Puedes usar el sistema mientras trabajas en otras ventanas

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
