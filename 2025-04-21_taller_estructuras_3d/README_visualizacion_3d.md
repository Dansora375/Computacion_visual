
# 🧪 Visualización y Análisis de Modelos 3D

📅 Fecha  
2025-04-25 – Fecha de entrega

---

🎯 Objetivo del Taller  
Explorar el manejo, visualización y análisis de modelos 3D en diferentes entornos de programación. Se trabajan herramientas de renderizado, estructuras de malla y animaciones aplicadas a modelos en formatos como `.OBJ`, `.STL` o `.GLTF`.

---

🧠 Conceptos Aprendidos

- ✅ Lectura y manipulación de mallas 3D (vértices, caras, aristas).
- ✅ Uso de herramientas como `trimesh`, `vedo` y `React Three Fiber` para cargar y visualizar modelos.
- ✅ Generación de animaciones 3D y exportación a GIF.
- Bonus: renderizado interactivo y cambio de visualización con controles.

---

🔧 Herramientas y Entornos

- Python: `trimesh`, `vedo`, `numpy`, `matplotlib`
- React Three Fiber (Three.js), @react-three/drei
- Vite como entorno base para el proyecto React

---

📁 Estructura del Proyecto

2025-04-25_taller3_visualizacion_3d/  
├── python/  
│   ├── estructuras_3d_python.ipynb  
│   ├── animacion_malla.gif <!-- Agregar el gif -->  
│   └── models/eyeball.obj  
├── react-three-fiber/  
│   ├── src/  
│   │   ├── App.jsx  
│   │   ├── App.css  
│   │   └── main.jsx  
│   ├── public/candle.obj  
│   └── images/visualizacion_three.gif <!-- Agregar el gif -->  
├── README.md  

---

🧪 Implementación

### 🧩 Python – Visualización y Análisis con Trimesh y Vedo

**Descripción:**  
Se carga un modelo `.obj` usando `trimesh`, se extrae su geometría y se visualiza con `vedo` usando distintos colores para vértices (rojo), aristas (verde) y caras (azul). Además, se genera una animación de rotación exportada como `.gif`.

**Código relevante:**
```python
vedo_mesh = vedo.Mesh([mesh.vertices, mesh.faces])
point_cloud = vedo.Points(mesh.vertices, r=8, c="red")
wireframe = vedo_mesh.wireframe().lw(2)
surface = vedo_mesh.clone().c("blue").alpha(0.7)
```

**GIF de resultado:**  
![Visualización Python](python/animacion_malla.gif)

---

### 🎞️ Python – Animación de Malla 3D

**Descripción:**  
La animación rotacional de la malla 3D se genera usando `vedo`, girando progresivamente el modelo sobre el eje Z. El resultado se exporta como `.gif`.

**Código relevante:**
```python
def rotate():
    vedo_mesh.rotate_z(5)
    return vedo_mesh

vedo.io.Video("animacion_malla.gif").action(rotate, duration=10, rate=30)
```

**GIF de animación:**  
![Animación Python](python/animacion_malla.gif)

---

### 🌐 React Three Fiber – Visualización Interactiva

**Descripción:**  
Se crea un componente en React que carga un modelo `.obj` con `@react-three/drei` y lo visualiza usando `OrbitControls`. El usuario puede alternar entre vistas de vértices, aristas y caras mediante una interfaz básica de botones.

**Código relevante (JSX):**
```jsx
<mesh geometry={geometry}>
  {mode === 'faces' && <meshStandardMaterial color="lightblue" />}
  {mode === 'edges' && <Edges />}
  {mode === 'points' && (
    <points>
      <bufferGeometry attach="geometry" {...geometry} />
      <pointsMaterial color="red" size={0.01} />
    </points>
  )}
</mesh>
```

**GIF del visor interactivo:**  
![Visualización Three.js](react-three-fiber/images/visualizacion_three.gif)

---

🧩 Prompts Usados

- "Carga un modelo 3D `.obj` en Python y visualízalo usando `vedo` con colores distintos por tipo de componente."
- "Genera una animación rotando el modelo 3D cargado con `vedo` y exporta el resultado como `.gif`."
- "Crea una aplicación en React Three Fiber que cargue un `.obj`, permita orbitar la cámara y cambiar entre vista de caras, aristas y puntos."

---

💬 Reflexión Final  

Este taller fue clave para afianzar el proceso completo de carga, visualización y animación de modelos 3D. Python resultó ideal para análisis estructural y exportación rápida, mientras que React Three Fiber destacó en interactividad y experiencia visual.

El reto más grande fue coordinar los diferentes formatos de geometría y hacerlos compatibles entre librerías. También fue necesario entender bien las diferencias entre `Scene` y `Mesh` en `trimesh`, y configurar los controles visuales en React. Me gustaría seguir explorando visualización con texturas y shaders personalizados en ambos entornos.
