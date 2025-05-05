# 🏗️ Taller - Construyendo el Mundo: Generación y Exportación de Objetos 3D con Python

📅 Fecha  
[Fecha del Taller, 2025-05-04] – Fecha de realización

---

🎯 Objetivo del Taller  
Generar programáticamente primitivas 3D (cubos, esferas, cilindros) a partir de una lista de coordenadas. Variar sus propiedades (posición, tamaño, color) utilizando lógica básica (bucles, condicionales). Exportar los objetos generados y/o la escena completa en distintos formatos estándar (.OBJ, .STL, .PLY) utilizando librerías como `vedo`, `trimesh` y `open3d`. Explorar la lectura de datos desde archivos para automatizar la generación.

---

🧠 Conceptos Aprendidos

✅ Creación programática de primitivas 3D (`vedo`).  
✅ Manipulación de propiedades de objetos 3D (posición, color).  
✅ Exportación de mallas 3D a formatos comunes (.OBJ, .STL, .PLY) usando `vedo`, `trimesh` y `open3d`.  
✅ Uso de bucles y condicionales para generar múltiples objetos con variaciones basadas en datos.  
✅ (Bonus) Lectura de datos desde archivos (.csv, .json) para automatizar la generación de geometrías.  
✅ Conversión básica entre representaciones de mallas para compatibilidad con diferentes librerías de exportación.

---

🔧 Herramientas y Entornos

- Python (Colab o Jupyter Notebook)
- `vedo`
- `trimesh`
- `open3d`
- `numpy`
- `json`
- `csv`
- `os`

---

📁 Estructura del Proyecto

2025-05-04_taller_generacion_exportacion_3D/<br>
├── modelos/            # Opcional: Puede usarse para datos de entrada (.csv, .json) o para guardar algunos modelos generados
├── entorno/python/<br>
│   └── generacion_y_exportacion_3d.ipynb # Notebook con el código del taller
├── resultados/<br>
│   └── [espacio para guardar los modelos generados y capturas/GIFs]
└── README.md

---

🧪 Implementación

🔹 Etapas realizadas

1.  Definición programática de una lista de coordenadas para puntos 3D iniciales.
2.  Generación de primitivas 3D (cubos, esferas, cilindros) basadas en estas coordenadas utilizando la librería `vedo`.
3.  Aplicación de lógica simple (bucles `for`, condicionales `if/elif/else`) para variar dinámicamente la forma y el color de las primitivas generadas según su posición o índice en la lista de coordenadas.
4.  Exportación de la escena completa de objetos generados a formato .OBJ usando `vedo.write()`.
5.  Conversión de objetos de `vedo` a un formato compatible con `trimesh` y exportación a .STL usando `trimesh.Scene(...).export()`.
6.  Conversión de objetos de `vedo` a una representación compatible con `open3d` (usando `numpy` para adaptar los vértices y caras) y exportación a .PLY usando `open3d.io.write_triangle_mesh()`.
7.  (Bonus) Implementación de lectura de coordenadas desde un archivo .csv para demostrar la automatización del proceso de generación a partir de datos externos.

---

### 🏗️ Generación y Exportación de Objetos 3D

**Descripción:**  
Este taller se centró en la **creación de objetos 3D a partir de datos**. La explicación clave de **"cómo se generaron los objetos desde datos"** reside en tomar una estructura de datos simple, como una lista de coordenadas tridimensionales `coords = [[x1, y1, z1], [x2, y2, z2], ...]`, e iterar sobre ella. En cada iteración, se utiliza la coordenada actual `[x, y, z]` para determinar la **posición** donde se creará una nueva primitiva 3D (un cubo, una esfera o un cilindro).

Se emplearon bucles (`for`) para procesar cada punto en la lista de datos y condicionales (`if/elif/else`) basadas en el índice del punto para variar las propiedades de la primitiva generada en esa posición (por ejemplo, crear un cubo rojo en el primer punto, una esfera verde en el segundo, un cilindro azul en el tercero, y repetir el ciclo). Esto demuestra cómo los datos de entrada controlan directamente la geometría y apariencia de los objetos generados.

Finalmente, los objetos resultantes se exportaron a formatos estándar de modelos 3D (.OBJ, .STL, .PLY) utilizando diferentes librerías, mostrando los pasos necesarios para adaptar la representación de la malla a los requisitos de cada biblioteca de exportación (como la triangulación o el formato de datos NumPy).

**Código relevante:**

```python
# Fragmento que muestra la generación de primitivas a partir de coordenadas usando vedo
# La lista 'coords' contiene las coordenadas de los puntos iniciales
vedo_objs = []
for i, coord in enumerate(coords):
    # Se usa la coordenada 'coord' para posicionar el objeto
    if i % 3 == 0:
        obj = vedo.Cube(pos=coord, side=1).color('red')
    elif i % 3 == 1:
        obj = vedo.Sphere(pos=coord, r=0.5).color('green')
    else:
        obj = vedo.Cylinder(pos=coord, r=0.3, height=1).color('blue')
    vedo_objs.append(obj)

# Exportación a .OBJ usando vedo
# Combinamos los objetos vedo en una escena para exportarlos juntos
scene_vedo = vedo.Assembly(vedo_objs)
vedo.write(scene_vedo, "scene_vedo.obj")

# Preparación y exportación a .STL usando trimesh
# Es necesario convertir los objetos vedo a un formato compatible con trimesh (Trimesh objects)
trimesh_objs = []
for vobj in vedo_objs:
    mesh_tri = vedo.Mesh(vobj).triangulate()  # Triangulamos para asegurar que las caras sean triángulos
    vertices = mesh_tri.points # Obtenemos los vértices como array NumPy
    faces = mesh_tri.faces()  # Obtenemos las caras como array NumPy
    # Creamos un objeto Trimesh a partir de los vértices y caras
    mesh = trimesh.Trimesh(vertices=vertices, faces=faces, process=False)
    trimesh_objs.append(mesh)

# Creamos una escena trimesh con todos los objetos y exportamos a .STL
scene_tri = trimesh.Scene(trimesh_objs)
scene_tri.export("scene_trimesh.stl")

# Preparación y exportación a .PLY usando Open3D
# Se muestra la conversión y exportación para uno de los objetos vedo (ej. el primero)
# La misma lógica se aplicaría a otros objetos si se exportaran individualmente o combinados
vobj_to_export_o3d = vedo_objs[0] # Tomamos el primer objeto vedo como ejemplo
mesh_tri_o3d = vedo.Mesh(vobj_to_export_o3d).triangulate() # Triangulamos

# Convertimos a formato NumPy adecuado para Open3D (dtype float64 para vértices, int32 para caras)
vertices_o3d = np.asarray(mesh_tri_o3d.points, dtype=np.float64)
faces_o3d = np.asarray(mesh_tri_o3d.faces(), dtype=np.int32)

# Creamos una malla Open3D (TriangleMesh) y le asignamos los vértices y triángulos
mesh_o3d = o3d.geometry.TriangleMesh()
mesh_o3d.vertices = o3d.utility.Vector3dVector(vertices_o3d)
mesh_o3d.triangles = o3d.utility.Vector3iVector(faces_o3d)
mesh_o3d.compute_vertex_normals() # Cálculo de normales, útil para visualización

# Exportamos la malla Open3D a un archivo .PLY
o3d.io.write_triangle_mesh("mesh_open3d.ply", mesh_o3d)

```



🖼️ Visualización de Resultados

Descripción:
Se visualizaron las primitivas 3D generadas directamente en el entorno Python para confirmar su correcta posición, forma y color, según los datos de entrada. Los resultados finales del taller son los archivos 3D exportados en diferentes formatos (.obj, .stl, .ply), listos para ser utilizados en otras aplicaciones de modelado o visualización 3D.Cabe mencionar que al correr el codigo se genera un archivo csv, que puede ser leido con coordenadas para generar los resultados como se han obtenido y se evidencia en el Gift.

GIF o imagen mostrando las primitivas generadas en su posición

![gift modelos](resultados/escenas%20parametricas%20.gif)

🧩 Prompts Usados

"Define una lista de coordenadas 3D en Python."
"Genera un cubo en una posición específica usando vedo."
"Crea una esfera y cámbiale el color usando vedo."
"Usa un bucle for para generar múltiples objetos en diferentes ubicaciones basadas en una lista de puntos."
"Utiliza condicionales (if/elif/else) para variar la forma y el color de los objetos generados."
"Exporta una escena de vedo que contiene varios objetos a un archivo .OBJ."
"Convierte un objeto de vedo a un formato compatible con trimesh para exportarlo a .STL."
"Prepara los datos de una malla (vértices y caras) para exportar con open3d a .PLY."
"Lee coordenadas desde un archivo .csv para automatizar la generación de objetos 3D."

💬 Reflexión Final

Este taller proporcionó una introducción fundamental a la generación programática de objetos 3D a partir de datos estructurados. Demostró cómo una simple lista de coordenadas puede ser el punto de partida para construir escenas 3D básicas, controlando la posición, forma y color de las primitivas mediante código. Exploramos la utilidad de librerías como vedo para la creación rápida de primitivas y el manejo inicial de mallas. Aprendimos sobre el proceso de exportación a formatos estándar, destacando la necesidad de adaptar los datos de la malla (como asegurar caras triangulares o convertir tipos de datos NumPy) para ser compatibles con diferentes herramientas de exportación como trimesh y open3d. Este enfoque "data-driven" para la creación de contenido 3D es una habilidad valiosa para la automatización en visualización, simulación y áreas creativas.