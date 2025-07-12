# Guía de Modelos 3D para el Sistema de Postura

## Modelos 3D Incluidos
El sistema incluye un modelo 3D generado por código que muestra:
- Esqueleto humano básico en postura correcta sentada
- Articulaciones marcadas en amarillo
- Columna vertebral en rojo
- Brazos en azul, piernas en verde
- Silla de referencia en marrón

## Cómo Agregar Modelos 3D Personalizados

### 1. Dónde Conseguir Modelos
**Gratuitos:**
- **Sketchfab**: https://sketchfab.com/3d-models/human-anatomy
  - Buscar "human pose", "sitting posture", "anatomical"
- **TurboSquid Free**: https://www.turbosquid.com/Search/3D-Models/free/human
- **Free3D**: https://free3d.com/3d-models/human
- **CGTrader Free**: https://www.cgtrader.com/free-3d-models/character/anatomy

**Modelos Recomendados:**
- "Sitting Human Pose"
- "Office Worker Posture"
- "Ergonomic Sitting Position"
- "Human Spine Model"

### 2. Formatos Soportados
El sistema puede cargar:
- `.obj` (más común)
- `.ply` 
- `.stl`
- `.vtk`

### 3. Cómo Instalar un Modelo Personalizado

1. **Descargar el modelo** en uno de los formatos soportados

2. **Renombrar el archivo** (opcional):
   ```
   correct_posture.obj
   sitting_pose.ply
   human_model.stl
   ```

3. **Colocar en la carpeta models**:
   ```
   Examen-Final/
   ├── models/
   │   ├── correct_posture.obj  ← Aquí
   │   └── texture.jpg          ← Texturas (opcional)
   ├── main.py
   └── ...
   ```

4. **Ejecutar el programa**: 
   - El sistema detectará automáticamente el modelo
   - Si hay múltiples modelos, usará el primero que encuentre

### 4. Ejemplo de Descarga (Sketchfab)

1. Ir a https://sketchfab.com
2. Buscar "sitting human pose free"
3. Seleccionar un modelo con licencia CC (Creative Commons)
4. Hacer clic en "Download"
5. Elegir formato .obj
6. Extraer el archivo .obj del ZIP descargado
7. Copiarlo a la carpeta `models/`

### 5. Optimización de Modelos

Si el modelo es muy pesado (>50MB):
- Usar Blender para reducir polígonos
- Convertir a formato más ligero
- Redimensionar si es necesario

### 6. Licencias
⚠️ **Importante**: Verificar siempre la licencia del modelo:
- CC0: Uso libre
- CC BY: Requiere atribución
- Comercial: Solo para uso educativo

### 7. Múltiples Modelos con Alternancia

**Nueva Funcionalidad:** El sistema puede alternar entre múltiples modelos automáticamente.

**Cómo agregar múltiples modelos:**
1. Colocar 2 o más modelos en la carpeta `models/`:
   ```
   Examen-Final/
   ├── models/
   │   ├── postura1.obj     ← Modelo 1
   │   ├── postura2.ply     ← Modelo 2
   │   ├── postura3.stl     ← Modelo 3 (opcional)
   │   └── texturas/        ← Carpeta para texturas
   ├── main.py
   └── ...
   ```

2. **Comportamiento del sistema:**
   - Si hay 1 modelo: Se muestra ese modelo
   - Si hay 2+ modelos: Alterna automáticamente cada 5 segundos
   - Si no hay modelos: Usa el esqueleto generado por código

3. **Controles durante alternancia:**
   - `Espacio`: Pausar/reanudar alternancia
   - `N`: Siguiente modelo manualmente
   - `P`: Modelo anterior
   - `R`: Reiniciar alternancia automática

4. **Recomendaciones para múltiples modelos:**
   - Usar modelos de tamaño similar
   - Preferir el mismo formato (.obj recomendado)
   - Nombrar descriptivamente: `postura_correcta_1.obj`, `postura_correcta_2.obj`

## Resolución de Problemas

**El modelo no se carga:**
- Verificar formato de archivo
- Comprobar que no esté corrupto
- Revisar la consola para errores

**El modelo se ve muy grande/pequeño:**
- El sistema usa el modelo tal como está
- Redimensionar en Blender si es necesario

**Textura no aparece:**
- Colocar archivos de textura (.jpg, .png) en la misma carpeta
- Algunos formatos no soportan texturas automáticamente
