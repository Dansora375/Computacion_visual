# 🌐 Taller - Modelos 3D con React Three Fiber

📅 Fecha
[Fecha del Taller,  2025-05-03] – Fecha de realización

---

🎯 Objetivo del Taller
Explorar la carga y visualización de diferentes formatos de modelos 3D (.OBJ, .STL, .GLTF) en una aplicación web utilizando React Three Fiber y Three.js. Se compararán las características de renderizado de cada formato y se implementará interactividad básica (cambio de modelo, control de cámara).

---

🧠 Conceptos Aprendidos

✅ Integración de Three.js con React mediante `@react-three/fiber`.
✅ Carga de modelos 3D en formatos .OBJ, .STL y .GLTF utilizando `@react-three/drei`.
✅ Uso de `OrbitControls` para navegación interactiva de la cámara.
✅ Gestión del estado en React para alternar entre diferentes modelos cargados.
✅ Observación y comparación de características visuales entre formatos 3D (suavidad, materiales, texturas, tamaño del archivo - implícito).
✅ Acceso y visualización de propiedades básicas del modelo (número de vértices, formato).

---

🔧 Herramientas y Entornos

- Node.js y npm/yarn
- React
- `@react-three/fiber`
- `@react-three/drei`
- Three.js
- Un entorno de desarrollo web (VS Code, etc.)

---

📁 Estructura del Proyecto

2025-05-03_taller_r3f_modelos3d/<br>
├── public/<br>
│   └── models/<br>
│       ├── modelo.obj<br>
│       ├── modelo.stl<br>
│       └── modelo.gltf<br>
├── src/<br>
│   ├── ModelInfo<br>
│   ├── ModelViewer<br>
│   ├── App.js<br>            
│   └── main.js<br>
└── README.md

---

### 🔄 Flujo de Conversión y Análisis

**Breve explicación del flujo:**

El taller parte de un modelo 3D original (asumimos un formato fuente como .blend, .fbx, etc.). Este modelo ha sido **previamente convertido** a los tres formatos objetivo: `.obj`, `.stl`, y `.gltf` utilizando software externo de modelado 3D o herramientas de conversión.

El **flujo de análisis** se centra en cargar estos *archivos ya convertidos* dentro de una aplicación web construida con React Three Fiber. La aplicación permite al usuario seleccionar cuál de los tres modelos convertidos desea visualizar en la escena 3D. El usuario interactúa con el modelo (orbitando a su alrededor con OrbitControls) y **analiza visualmente** las diferencias en cómo se renderiza cada formato, prestando atención a la fidelidad de los materiales, la suavidad de la malla, y la presencia de texturas, así como observando la información técnica básica del modelo (número de vértices). Este proceso de carga, selección e inspección visual constituye el análisis práctico dentro del taller.

---

🧪 Implementación

🔹 Etapas realizadas

1.  Configuración inicial de un proyecto React con las dependencias `@react-three/fiber` y `@react-three/drei`.
2.  Creación de un componente `ModelViewer` que envuelve la escena 3D usando `<Canvas>`.
3.  Implementación de lógica para cargar los modelos (.OBJ, .STL, .GLTF) de forma condicional basada en un estado de React que representa el formato seleccionado (usando `useLoader`).
4.  Adición de `OrbitControls` dentro del `<Canvas>` para permitir la interacción del usuario con la cámara.
5.  Desarrollo de un componente `UIControls` con botones o un selector para cambiar el estado del formato del modelo a mostrar en tiempo real.
6.  Integración de los componentes `ModelViewer` y `UIControls` en `App.js`.
7.  Implementación de la funcionalidad bonus para obtener el número de vértices del modelo cargado y mostrarlo junto con el formato actual.
8.  Ejecución y observación de la escena para identificar las diferencias visuales entre los modelos cargados.

---

**Código relevante :**

```javascript
// src/components/ModelViewer.js (Extractos)
import React, { useRef, useState } from 'react';
import { Canvas, useLoader, useFrame } from '@react-three/fiber';
import { OrbitControls, useGLTF, useOBJ, useSTL } from '@react-three/drei';
import * as THREE from 'three'; // Necesario para GLTF vertex count

function Model({ format, url, setModelInfo }) {
  let model;
  let loader;
  let vertexCount = 0;

  // Carga condicional basada en el formato
  if (format === 'gltf') {
    model = useGLTF(url);
    loader = 'GLTF';
     // Contar vértices para GLTF (puede variar según la estructura del archivo)
     model.scene.traverse((child) => {
        if (child.isMesh) {
            if (child.geometry.attributes.position) {
                vertexCount += child.geometry.attributes.position.count;
            }
        }
     });

  } else if (format === 'obj') {
    model = useOBJ(url);
    loader = 'OBJ';
     // Contar vértices para OBJ (puede ser diferente)
     model.traverse((child) => {
        if (child.isMesh) {
            if (child.geometry.attributes.position) {
                 vertexCount += child.geometry.attributes.position.count;
            }
        }
     });

  } else if (format === 'stl') {
    const geometry = useSTL(url);
    // Para STL, useSTL devuelve directamente la geometría
    model = <mesh geometry={geometry}><meshStandardMaterial color="hotpink" /></mesh>; // Envolver en mesh
    loader = 'STL';
    if (geometry.attributes.position) {
        vertexCount = geometry.attributes.position.count;
    }
  } else {
      setModelInfo({ format: 'N/A', vertices: 0 });
      return null; // No model selected
  }

  // Actualizar información del modelo (usando useEffect o al cargar)
  // Esto es una simplificación; en un caso real, usarías useEffect.
  useState(() => {
      if(model) setModelInfo({ format: loader, vertices: vertexCount });
  }, [model, format, setModelInfo]); // Dependencias actualizadas

  if (!model) return null;

  // Renderizar el modelo (ajustar según el formato si useLoader devuelve algo diferente)
  return <primitive object={format === 'stl' ? model.props.geometry : model.scene || model} scale={format === 'stl' ? 0.1 : 1} />; // Ajustar escala si es necesario
}


function ModelViewer() {
    const [currentModel, setCurrentModel] = useState('gltf'); // Estado para el formato actual
    const [modelInfo, setModelInfo] = useState({ format: 'N/A', vertices: 0 });

    // ... lógica para cambiar currentModel desde UIControls ...

    return (
      <>
        {/* UI Controls component here, passing setCurrentModel */}
        <UIControls onSelectModel={setCurrentModel} />

        <div style={{ position: 'absolute', top: '10px', left: '10px', color: 'white', zIndex: 10 }}>
            Formato: {modelInfo.format}<br/>
            Vértices: {modelInfo.vertices}
        </div>

        <Canvas style={{ width: '100vw', height: '100vh' }}>
          <ambientLight intensity={0.5} />
          <spotLight position={[10, 10, 10]} angle={0.15} penumbra={1} decay={0} intensity={Math.PI} />
          <pointLight position={[-10, -10, -10]} decay={0} intensity={Math.PI} />
          <Model
             format={currentModel}
             url={`/models/modelo.${currentModel}`} // Asumimos que los modelos están en /public/models
             setModelInfo={setModelInfo}
           />
          <OrbitControls />
        </Canvas>
      </>
    );
}
```

🖼️ Visualización de Resultados

Descripción:  

Se observan en los gift los  diferentes modelos de un skull entre dos formatos en este caso OBJ y SLT con sus respectivos numeros de vertices.Ademas se visualiza un modelo en GLTF 

**GIF del visor interactivo:**

![gift modelos](resultados/modelos%203d.gif)

🧩 Prompts Usados (Si aplicable, si se usó IA para generar código o ideas específicas)

"Cómo cargar un modelo GLTF en React Three Fiber?"
"Ejemplo de uso de OrbitControls con useGLTF en R3F."
"Cómo cambiar de modelo 3D al hacer click en un botón en una escena de R3F?"
"Cómo obtener el número de vértices de un objeto cargado con useGLTF, useOBJ y useSTL en React Three Fiber?"
"Mostrar información de un modelo 3D en una interfaz de usuario en R3F."

💬 Reflexión Final

Este taller proporcionó una excelente introducción práctica a la carga y manejo de modelos 3D en un entorno web moderno con React. Utilizar React Three Fiber simplifica enormemente la integración de Three.js en un flujo de trabajo de componentes. Comparar los formatos .OBJ, .STL y .GLTF directamente en la aplicación web hizo muy claras sus diferencias: GLTF destaca por su capacidad de incluir materiales y texturas complejas en un solo archivo; STL es muy simple y eficiente para geometrías sin color ni textura; y OBJ, aunque versátil, a menudo requiere archivos de materiales (.MTL) separados. La implementación de OrbitControls y la lógica de alternancia de modelos demostró cómo añadir interactividad básica que es fundamental en cualquier visor 3D. Un desafío interesante fue obtener el número de vértices de manera consistente a través de los diferentes loaders, ya que la estructura de datos puede variar ligeramente. Este es un paso fundamental para construir aplicaciones web más complejas que involucren visualización 3D interactiva.










# 🌐 Taller - Importando el Mundo: Visualización y Conversión de Formatos 3D python

📅 Fecha  
[Fecha del Taller, 2025-05-04] – Fecha de realización

---

🎯 Objetivo del Taller  
Importar y visualizar modelos 3D en distintos formatos (.OBJ, .STL, .GLTF) utilizando Python. Analizar sus propiedades geométricas (vértices, caras, normales) y detectar duplicados. Comparar modelos entre sí y realizar conversiones entre formatos usando herramientas como `trimesh`, `open3d` y `assimp`.

---

🧠 Conceptos Aprendidos

✅ Carga de modelos 3D en diferentes formatos con `trimesh` y `open3d`.  
✅ Extracción de propiedades geométricas como cantidad de vértices, caras y normales.  
✅ Verificación de duplicados y estado de watertight de las mallas.  
✅ Visualización básica de modelos 3D directamente en Python.  
✅ Conversión entre formatos usando `trimesh.exchange` y `pyassimp`.  
✅ Automatización de análisis para múltiples modelos.

---

🔧 Herramientas y Entornos

- Python
- `trimesh`
- `open3d`
- `numpy`
- `pyassimp`
- `scipy` (recomendado, pero se manejan errores si no está presente)

---

📁 Estructura del Proyecto

2025-05-04_taller_modelos_3D/<br>
├── modelos/<br>
│   └── modelo.obj, modelo.stl, modelo.gltf (rutas personalizables)<br>
├── entorno/python/<br>
│   └── conversion_y_analisis_3d.ipynb<br>
├── resultados/<br>
│   └── [espacio para guardar modelos convertidos y capturas]<br>
└── README.md

---

🧪 Implementación

🔹 Etapas realizadas

1.  Carga de modelos 3D en formatos .OBJ, .STL y .GLTF usando `trimesh` y `open3d`.
2.  Visualización de cada modelo para verificar su estructura básica.
3.  Extracción de métricas geométricas (vértices, caras, normales).
4.  Detección de mallas con vértices duplicados o no watertight.
5.  Conversión entre formatos usando `trimesh.exchange.export` y `pyassimp.export`.
6.  Comparación entre diferentes modelos y verificación post-conversión.
7.  Automatización con una función de comparación entre múltiples modelos.

---

### 📊 Análisis y Conversión de Modelos

**Descripción:**  
El taller se centró en la comparación estructural entre modelos cargados en distintos formatos. Se analizaron sus vértices, caras y normales, verificando también si la malla estaba cerrada (`watertight`). Luego se realizó una conversión entre formatos para verificar si la estructura se mantenía tras el cambio. Se incluyeron estrategias para manejar errores comunes como la falta de `scipy` o la incompatibilidad con `pyassimp`.

**Código relevante:**

```python
def analyze_trimesh(mesh):
    try:
        normals_count = len(mesh.vertex_normals)
    except Exception:
        normals_count = 0  # Evita error si falta scipy

    info = {
        'vertices': len(mesh.vertices),
        'faces': len(mesh.faces),
        'normals': normals_count,
        'has_duplicate_vertices': not mesh.is_watertight
    }
    return info


  def convert_format(input_path, output_path, file_type='stl'):
    mesh = trimesh.load(input_path)
    mesh.export(output_path, file_type=file_type)


  def compare_models(mesh1, mesh2):
      return {
          'vertices_equal': np.allclose(mesh1.vertices, mesh2.vertices),
          'faces_equal': np.array_equal(mesh1.faces, mesh2.faces),
          'same_volume': np.isclose(mesh1.volume, mesh2.volume)
      }
```

🖼️ Visualización de Resultados

Descripción:
Se visualizaron modelos importados en su forma original y convertida, mostrando sus propiedades (vértices, caras, normales) y permitiendo comprobar si las conversiones conservaron la geometría.

GIF de comparación visual de modelos cargados y convertidos

![gift modelos](resultados/taller%20modelos%203d%20python.gif)

🧩 Prompts Usados

"Importa y visualiza un modelo .OBJ usando trimesh en Python."
"Analiza cantidad de vértices, caras, y normales de un modelo 3D."
"Convierte un archivo .STL a .GLTF usando pyassimp y exporta el resultado."
"Compara la geometría de dos modelos 3D distintos y evalúa si son iguales."
"Muestra una malla en pantalla usando open3d para ver su forma."
"Detecta si una malla está cerrada (is_watertight) en trimesh."
"Automatiza la comparación de varios modelos y genera un resumen de diferencias."

💬 Reflexión Final

Este taller facilitó una comprensión profunda del manejo de modelos 3D desde una perspectiva programática. Cargar modelos en distintos formatos y comparar sus propiedades permitió apreciar las diferencias sutiles entre estándares como OBJ, STL y GLTF. El uso de librerías como trimesh y open3d resultó clave para visualizar e inspeccionar los modelos de forma rápida, mientras que pyassimp ofreció una solución flexible para la conversión entre formatos. El análisis estructurado de geometría (vértices, caras, normales) demostró ser una herramienta esencial para validar integridad y consistencia. Automatizar este análisis nos preparó para manejar flujos de trabajo con múltiples modelos, y nos acercó a prácticas más profesionales en la gestión de datos 3D.
