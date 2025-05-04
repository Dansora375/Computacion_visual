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

