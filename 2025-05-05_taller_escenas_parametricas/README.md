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
├── modelos/<br>
├── entorno/python/<br>
│   └── generacion_y_exportacion_3d.ipynb<br>
├── resultados/<br>
│   └── [espacio para guardar los modelos generados y capturas/GIFs]<br>
└── README.md<br>

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

# 🌐 Taller - Tres Dimensiones con React: Three.js y React Three Fiber

📅 Fecha  
[2025-05-05] – Fecha de realización

---

🎯 Objetivo del Taller  
- Configurar una escena básica con React Three Fiber.
- Renderizar múltiples objetos 3D a partir de una estructura de datos (array de objetos).
- Controlar dinámicamente la posición, escala, color y rotación de cada objeto 3D basándose en las propiedades definidas en los datos.
- Utilizar `map()` de JavaScript/React para iterar sobre los datos y generar componentes 3D correspondientes.
- Integrar `leva` para crear un panel de control interactivo y modificar parámetros globales (como escala o velocidad de rotación) que afecten a los objetos en tiempo real.

---

🧠 Conceptos Aprendidos

✅ Configuración de una escena 3D interactiva con React Three Fiber (`@react-three/fiber`, `@react-three/drei`).  
✅ Renderizado de múltiples objetos 3D a partir de un array de datos utilizando `map()`.  
✅ Parametrización de propiedades de objetos (posición, escala, color, rotación) directamente desde los datos de entrada.  
✅ Implementación de animación en objetos 3D usando el hook `useFrame`.  
✅ Integración de un panel de control interactivo con `leva` para modificar parámetros en tiempo real (`useControls`).  
✅ Desarrollo de componentes reutilizables para objetos 3D (ej. `BoxItem`).  
✅ Concepto de renderizado "data-driven" en un entorno 3D web.

---

🔧 Herramientas y Entornos

- React
- React Three Fiber (`@react-three/fiber`)
- Three.js
- Drei (`@react-three/drei`)
- Leva (`leva`)
- Node.js y gestor de paquetes (npm/yarn)
- Entorno de desarrollo web (VS Code, navegador)

---

📁 Estructura del Proyecto

mi_taller_r3f/<br>
├── node_modules/<br>
├── public/<br>
│   └── index.html<br>
├── src/<br>
│   ├── components/<br>
│   │   ├── BoxItem.jsx<br>
│   │   └── Scene.jsx<br>
│   ├── App.jsx<br>
│   └── index.js (o .jsx)<br>
├── package.json<br>
└── README.md

---

🧪 Implementación

🔹 Etapas realizadas

1.  Configuración inicial de un proyecto React con React Three Fiber.
2.  Definición de una estructura de datos (array de objetos) que contiene las propiedades deseadas para cada objeto 3D.
3.  Creación de un componente React (`BoxItem`) que representa un objeto 3D individual (un cubo en este caso) y acepta propiedades como posición, color, escala y un flag de rotación.
4.  En el componente principal de la escena (`Scene`), se utiliza el método `map()` para iterar sobre el array de datos y renderizar una instancia de `BoxItem` por cada elemento en el array.
5.  Las propiedades de cada objeto 3D son asignadas dinámicamente desde el elemento correspondiente en el array de datos y pasadas como props a cada `BoxItem`.
6.  Implementación de lógica condicional o basada en datos dentro del componente `BoxItem` (o a través de props) para determinar si el objeto debe rotar. Uso del hook `useFrame` para la animación.
7.  Integración de la librería `leva` para crear un panel de control (`useControls`) que permite ajustar parámetros globales (como la escala general o la velocidad de rotación) en tiempo real desde la interfaz.
8.  Conexión de los controles de `leva` con las propiedades de los objetos 3D renderizados, permitiendo la modificación dinámica de la escena.

---

### 🌐 Tres Dimensiones con React: Three.js y React Three Fiber

**Descripción:**  
Este taller exploró la **generación y control dinámico de objetos 3D** en un entorno web utilizando React Three Fiber. La idea central fue tomar una lista de objetos JavaScript (`data`), donde cada objeto define las características de un elemento 3D (su posición `x`, `color`, `scale`, y si debe `rotate`). Utilizando la función `map()` de JavaScript, iteramos sobre este array. Por cada objeto en `data`, renderizamos un componente React que representa un cubo 3D (`<BoxItem>`). Las propiedades de este cubo (como su posición en el eje X, su color y su escala inicial) se derivan directamente de los valores correspondientes en el objeto del array `data`. Además, un flag `rotate` en los datos determina si el cubo aplicará una animación de rotación.

Para añadir interactividad, integramos la librería `leva`. `leva` nos permitió crear un panel de control en la interfaz donde podemos ajustar parámetros globales, como una `globalScale` que multiplica la escala individual de cada cubo, o una `rotationSpeed` que afecta a todos los cubos que están configurados para rotar. Estos valores de `leva` se pasan como props a los componentes `BoxItem`, permitiendo modificar la apariencia y el comportamiento de la escena en tiempo real. Esto ilustra cómo combinar datos estáticos (el array inicial) con controles dinámicos (leva) para crear experiencias 3D flexibles y controlables.

**Código relevante:**

```javascript
// src/components/Scene.jsx - Configuración de la escena, datos y mapeo
import React from 'react';
import { useControls } from 'leva'; // Importa el hook de leva
import { Box } from '@react-three/drei'; // Puede ser útil para otras primitivas o helpers
import BoxItem from './BoxItem'; // Importa el componente para un solo objeto

// Array de datos que define las propiedades de cada objeto 3D
const data = [
  { id: 1, x: -2, color: 'red', scale: 1, rotate: false },
  { id: 2, x: 0, color: 'green', scale: 1.5, rotate: true },
  { id: 3, x: 2, color: 'blue', scale: 1, rotate: false },
];

function Scene() {
  // Define controles dinámicos usando leva
  const { globalScale, rotationSpeed } = useControls('Controls', {
    globalScale: { value: 1, min: 0.5, max: 2 },
    rotationSpeed: { value: 0.01, min: 0, max: 0.1 }
  });

  return (
    <>
      {/* Mapea el array de datos para renderizar BoxItem por cada elemento */}
      {data.map((item) => (
        <BoxItem
          key={item.id} // Clave única para la lista de React
          position={[item.x, 0, 0]} // Posición basada en el dato 'x'
          color={item.color} // Color basado en el dato 'color'
          scale={item.scale * globalScale} // Escala combinando dato y control de leva
          rotate={item.rotate} // Indica si debe rotar según el dato
          rotationSpeed={rotationSpeed} // Velocidad de rotación controlada por leva
        />
      ))}
    </>
  );
}

export default Scene;

[⚠️ Suspicious Content] // src/components/BoxItem.jsx - Componente para un objeto 3D individual
import React, { useRef } from 'react';
import { useFrame } from '@react-three/fiber'; // Hook para el loop de animación

// Componente funcional que recibe propiedades (props)
function BoxItem({ position, color, scale, rotate, rotationSpeed }) {
  const ref = useRef(); // Ref para acceder al objeto 3D en el loop

  // Hook useFrame se ejecuta en cada frame de animación
  useFrame(() => {
    // Condición: si la propiedad 'rotate' es verdadera Y la ref existe
    if (rotate && ref.current) {
      ref.current.rotation.y += rotationSpeed; // Incrementa la rotación en el eje Y
    }
  });

  return (
    // Malla base: geometría de caja y material estándar
    <mesh ref={ref} position={position} scale={scale}>
      <boxGeometry args={[1, 1, 1]} /> {/* Geometría de caja unitaria */}
      <meshStandardMaterial color={color} /> {/* Material con color especificado */}
    </mesh>
  );
}

export default BoxItem;
```

 Claro, aquí tienes el README completo en formato Markdown, listo para copiar y pegar. Incluye los detalles y fragmentos de código relevantes para el taller de Three.js con React Three Fiber, siguiendo la estructura exacta de tu template.

Markdown

# 🌐 Taller - Tres Dimensiones con React: Three.js y React Three Fiber

📅 Fecha  
[2025-05-05] – Fecha de realización

---

🎯 Objetivo del Taller  
- Configurar una escena básica con React Three Fiber.
- Renderizar múltiples objetos 3D a partir de una estructura de datos (array de objetos).
- Controlar dinámicamente la posición, escala, color y rotación de cada objeto 3D basándose en las propiedades definidas en los datos.
- Utilizar `map()` de JavaScript/React para iterar sobre los datos y generar componentes 3D correspondientes.
- Integrar `leva` para crear un panel de control interactivo y modificar parámetros globales (como escala o velocidad de rotación) que afecten a los objetos en tiempo real.

---

🧠 Conceptos Aprendidos

✅ Configuración de una escena 3D interactiva con React Three Fiber (`@react-three/fiber`, `@react-three/drei`).  
✅ Renderizado de múltiples objetos 3D a partir de un array de datos utilizando `map()`.  
✅ Parametrización de propiedades de objetos (posición, escala, color, rotación) directamente desde los datos de entrada.  
✅ Implementación de animación en objetos 3D usando el hook `useFrame`.  
✅ Integración de un panel de control interactivo con `leva` para modificar parámetros en tiempo real (`useControls`).  
✅ Desarrollo de componentes reutilizables para objetos 3D (ej. `BoxItem`).  
✅ Concepto de renderizado "data-driven" en un entorno 3D web.

---

🔧 Herramientas y Entornos

- React
- React Three Fiber (`@react-three/fiber`)
- Three.js
- Drei (`@react-three/drei`)
- Leva (`leva`)
- Node.js y gestor de paquetes (npm/yarn)
- Entorno de desarrollo web (VS Code, navegador)

---

📁 Estructura del Proyecto

mi_taller_r3f/<br>
├── node_modules/<br>
├── public/<br>
│   └── index.html<br>
├── src/<br>
│   ├── components/<br>
│   │   ├── BoxItem.jsx<br>
│   │   └── Scene.jsx<br>
│   ├── App.jsx<br>
│   └── index.js (o .jsx)<br>
├── package.json<br>
└── README.md

---

🧪 Implementación

🔹 Etapas realizadas

1.  Configuración inicial de un proyecto React con React Three Fiber.
2.  Definición de una estructura de datos (array de objetos) que contiene las propiedades deseadas para cada objeto 3D.
3.  Creación de un componente React (`BoxItem`) que representa un objeto 3D individual (un cubo en este caso) y acepta propiedades como posición, color, escala y un flag de rotación.
4.  En el componente principal de la escena (`Scene`), se utiliza el método `map()` para iterar sobre el array de datos y renderizar una instancia de `BoxItem` por cada elemento en el array.
5.  Las propiedades de cada objeto 3D son asignadas dinámicamente desde el elemento correspondiente en el array de datos y pasadas como props a cada `BoxItem`.
6.  Implementación de lógica condicional o basada en datos dentro del componente `BoxItem` (o a través de props) para determinar si el objeto debe rotar. Uso del hook `useFrame` para la animación.
7.  Integración de la librería `leva` para crear un panel de control (`useControls`) que permite ajustar parámetros globales (como la escala general o la velocidad de rotación) en tiempo real desde la interfaz.
8.  Conexión de los controles de `leva` con las propiedades de los objetos 3D renderizados, permitiendo la modificación dinámica de la escena.

---

### 🌐 Tres Dimensiones con React: Three.js y React Three Fiber

**Descripción:**  
Este taller exploró la **generación y control dinámico de objetos 3D** en un entorno web utilizando React Three Fiber. La idea central fue tomar una lista de objetos JavaScript (`data`), donde cada objeto define las características de un elemento 3D (su posición `x`, `color`, `scale`, y si debe `rotate`). Utilizando la función `map()` de JavaScript, iteramos sobre este array. Por cada objeto en `data`, renderizamos un componente React que representa un cubo 3D (`<BoxItem>`). Las propiedades de este cubo (como su posición en el eje X, su color y su escala inicial) se derivan directamente de los valores correspondientes en el objeto del array `data`. Además, un flag `rotate` en los datos determina si el cubo aplicará una animación de rotación.

Para añadir interactividad, integramos la librería `leva`. `leva` nos permitió crear un panel de control en la interfaz donde podemos ajustar parámetros globales, como una `globalScale` que multiplica la escala individual de cada cubo, o una `rotationSpeed` que afecta a todos los cubos que están configurados para rotar. Estos valores de `leva` se pasan como props a los componentes `BoxItem`, permitiendo modificar la apariencia y el comportamiento de la escena en tiempo real. Esto ilustra cómo combinar datos estáticos (el array inicial) con controles dinámicos (leva) para crear experiencias 3D flexibles y controlables.

**Código relevante:**

```javascript
// src/components/Scene.jsx - Configuración de la escena, datos y mapeo
import React from 'react';
import { useControls } from 'leva'; // Importa el hook de leva
import { Box } from '@react-three/drei'; // Puede ser útil para otras primitivas o helpers
import BoxItem from './BoxItem'; // Importa el componente para un solo objeto

// Array de datos que define las propiedades de cada objeto 3D
const data = [
  { id: 1, x: -2, color: 'red', scale: 1, rotate: false },
  { id: 2, x: 0, color: 'green', scale: 1.5, rotate: true },
  { id: 3, x: 2, color: 'blue', scale: 1, rotate: false },
];

function Scene() {
  // Define controles dinámicos usando leva
  const { globalScale, rotationSpeed } = useControls('Controls', {
    globalScale: { value: 1, min: 0.5, max: 2 },
    rotationSpeed: { value: 0.01, min: 0, max: 0.1 }
  });

  return (
    <>
      {/* Mapea el array de datos para renderizar BoxItem por cada elemento */}
      {data.map((item) => (
        <BoxItem
          key={item.id} // Clave única para la lista de React
          position={[item.x, 0, 0]} // Posición basada en el dato 'x'
          color={item.color} // Color basado en el dato 'color'
          scale={item.scale * globalScale} // Escala combinando dato y control de leva
          rotate={item.rotate} // Indica si debe rotar según el dato
          rotationSpeed={rotationSpeed} // Velocidad de rotación controlada por leva
        />
      ))}
    </>
  );
}

export default Scene;
JavaScript

// src/components/BoxItem.jsx - Componente para un objeto 3D individual
import React, { useRef } from 'react';
import { useFrame } from '@react-three/fiber'; // Hook para el loop de animación

// Componente funcional que recibe propiedades (props)
function BoxItem({ position, color, scale, rotate, rotationSpeed }) {
  const ref = useRef(); // Ref para acceder al objeto 3D en el loop

  // Hook useFrame se ejecuta en cada frame de animación
  useFrame(() => {
    // Condición: si la propiedad 'rotate' es verdadera Y la ref existe
    if (rotate && ref.current) {
      ref.current.rotation.y += rotationSpeed; // Incrementa la rotación en el eje Y
    }
  });

  return (
    // Malla base: geometría de caja y material estándar
    <mesh ref={ref} position={position} scale={scale}>
      <boxGeometry args={[1, 1, 1]} /> {/* Geometría de caja unitaria */}
      <meshStandardMaterial color={color} /> {/* Material con color especificado */}
    </mesh>
  );
}

export default BoxItem;

```
🖼️ Visualización de Resultados

Descripción:  
La visualización muestra la escena 3D renderizada en el navegador. Se aprecian los cubos colocados en las posiciones definidas por el array de datos, cada uno con su color y escala correspondientes. Uno de los cubos (el verde en el centro) está rotando, según lo indicado en su propiedad rotate. Si la visualización incluye el panel de leva, se puede observar cómo interactuar con los sliders (globalScale, rotationSpeed) modifica la escala de todos los cubos y la velocidad de rotación del cubo animado en tiempo real.

GIF o imagen mostrando los objetos 3D generados y, si es posible, el panel de Leva interactuando.


![Resultados del Taller R3F](resultados/escenas%20parametricas%20threejs.gif)

🧩 Prompts Usados

"Cómo configurar una escena básica con React Three Fiber en un proyecto React."
"Renderizar múltiples primitivas 3D (ej. cubos) a partir de un array de datos en R3F."
"Pasar propiedades (posición, color, escala) de un objeto de un array a un componente 3D en React Three Fiber."
"Crear un componente React para un objeto 3D reutilizable (BoxItem)."
"Implementar rotación animada en un objeto R3F usando el hook useFrame."
"Controlar la rotación de un objeto R3F mediante una propiedad (rotate)."
"Integrar la librería leva para crear un panel de control interactivo en una escena R3F."
"Usar el hook useControls de leva para definir parámetros globales controlables (ej. escala, velocidad de rotación)."
"Conectar los valores del panel de leva con las propiedades de los objetos 3D renderizados para control dinámico."

💬 Reflexión Final

Este taller demostró la potencia de combinar React Three Fiber con estructuras de datos simples y herramientas de control como leva para crear escenas 3D web dinámicas y controlables. Aprendimos a generar programáticamente un conjunto de objetos 3D a partir de un array, utilizando map() para asignar propiedades individuales como posición, color y escala. La habilidad de parametrizar estas características basadas en datos es fundamental para crear visualizaciones o entornos 3D adaptativos. La integración de leva añadió una capa crucial de interactividad, permitiendo ajustar parámetros globales en tiempo real y observar los cambios inmediatamente. Este enfoque de renderizado "data-driven" combinado con controles interactivos abre muchas posibilidades para la creación de contenido 3D web.
