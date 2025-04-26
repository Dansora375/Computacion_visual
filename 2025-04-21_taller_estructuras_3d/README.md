
# 🧪 Visualización y Análisis de Estructuras 3D

📅 Fecha  
2025-04-25 – Fecha de entrega

---

🎯 Objetivo del Taller  
Aprender a cargar, visualizar y analizar modelos 3D utilizando bibliotecas especializadas en Python. Se busca comprender la estructura geométrica (vértices, aristas, caras) y producir visualizaciones animadas mediante rotaciones.

---

🧠 Conceptos Aprendidos

- ✅ Carga de modelos 3D en distintos formatos (.OBJ, .STL, .GLTF)
- ✅ Análisis estructural de mallas (número de vértices, caras y aristas únicas)
- ✅ Visualización 3D con `vedo`
- ✅ Generación de animaciones con `imageio`

---

🔧 Herramientas y Entornos

- Python (`trimesh`, `vedo`, `numpy`, `matplotlib`, `imageio`)
- Jupyter Notebook

---

📁 Estructura del Proyecto

```
2025-04-25_taller_visualizacion_3d/
├── models/
│   └── eyeball.obj
├── estructuras_3d_python.ipynb
├── animacion_malla.gif
└── README.md
```

---

🧪 Implementación

🔹 Etapas realizadas

1. Se cargó el modelo 3D utilizando `trimesh`, identificando si se trataba de una malla o una escena compuesta.
2. Se extrajo la información estructural del modelo: número de vértices, caras y aristas únicas.
3. Se generó una visualización 3D en `vedo` con colores distintos para vértices (rojo), aristas (verde) y caras (azul semi-transparente).
4. Se implementó una animación rotando el modelo y se exportó como GIF utilizando `imageio`.

🔹 Código relevante

**Carga del modelo y verificación de tipo (`trimesh`):**

```python
scene_or_mesh = trimesh.load(model_path)
if isinstance(scene_or_mesh, trimesh.Scene):
    mesh = scene_or_mesh.geometry[list(scene_or_mesh.geometry.keys())[0]]
else:
    mesh = scene_or_mesh
```

**Visualización en vedo:**

```python
vedo_mesh = vedo.Mesh([mesh.vertices, mesh.faces])
point_cloud = vedo.Points(mesh.vertices, r=8, c="red")
wireframe = vedo_mesh.wireframe().lw(2)
surface = vedo_mesh.clone().c("blue").alpha(0.7)

plotter = vedo.Plotter()
plotter.show(point_cloud, wireframe, surface)
```

**Generación de animación con imageio:**

```python
for i in range(72):
    vedo_mesh.rotate_z(5)
    plotter.show(vedo_mesh, interactive=False)
    plotter.screenshot(filename)
```

---

📊 Resultados Visuales

✅ Este taller requiere explícitamente un GIF animado. A continuación, se incluye la visualización final generada en Python:

### Python  
![Visualización malla 3D animada](animacion_malla.gif)

---

🧩 Prompts Usados

Este taller no incluyó prompts generativos, ya que todo el código fue escrito de forma manual y estructurada.

---

💬 Reflexión Final

Este ejercicio me permitió entender en profundidad cómo se representa una malla 3D y cómo visualizarla con distintas herramientas. Aprendí a diferenciar entre una `Scene` y una `Mesh` en `trimesh`, a manipular estructuras geométricas y a usar `vedo` para renderizar y animar.

Tuve algunas dificultades al principio con errores de atributos y métodos inexistentes (como `vedo.animate`), pero eso me llevó a investigar y encontrar una solución práctica con `imageio` para crear GIFs desde capturas de pantalla. Esto reforzó mis habilidades de depuración y búsqueda de alternativas.
