import React, { useEffect, useState } from 'react';
import { Canvas, useLoader } from '@react-three/fiber';
import { OrbitControls, Edges, Stats } from '@react-three/drei';
import * as THREE from 'three';
import { OBJLoader } from 'three/examples/jsm/loaders/OBJLoader';
import './App.css';

// Component that loads and displays the 3D model
function Model({ mode, setInfo }) {
  const obj = useLoader(OBJLoader, '/models/Candle.obj');

  useEffect(() => {
    let vertices = 0;
    let faces = 0;

    // Traverse the loaded object to process meshes
    obj.traverse((child) => {
      if (child.isMesh) {
        const geom = child.geometry;

        // Ensure geometry data is properly computed
        geom.computeVertexNormals();
        geom.computeBoundingBox();
        geom.computeBoundingSphere();

        // Center the model geometry by translating it
        const center = new THREE.Vector3();
        geom.boundingBox.getCenter(center);
        geom.translate(-center.x, -center.y, -center.z);

        // Count vertices and faces
        vertices += geom.attributes.position.count;
        if (geom.index) {
          faces += geom.index.count / 3;
        } else {
          faces += geom.attributes.position.count / 3;
        }
      }
    });

    // Update parent state with model info
    setInfo({ vertices, faces: Math.round(faces) });
  }, [obj, setInfo]);

  // Render the model using different materials depending on the selected view mode
  return (
    <group scale={[10, 10, 10]}>
      {obj.children.map((child, index) => {
        if (child.isMesh) {
          const geometry = child.geometry;

          return (
            <mesh key={index} geometry={geometry}>
              {mode === 'default' && (
                <meshStandardMaterial color="#d9bfa3" metalness={0.2} roughness={0.8} />
              )}
              {mode === 'edges' && (
                <>
                  <meshStandardMaterial color="#d9bfa3" />
                  <Edges geometry={geometry} color="red" />
                </>
              )}
              {mode === 'wireframe' && (
                <meshBasicMaterial wireframe color="orange" />
              )}
              {mode === 'points' && (
                <points geometry={geometry}>
                  <pointsMaterial size={0.02} color="blue" />
                </points>
              )}
            </mesh>
          );
        }
        return null;
      })}
    </group>
  );
}

// Main app component
export default function App() {
  const [mode, setMode] = useState('default');         // Current view mode (default, edges, wireframe, points)
  const [modelInfo, setModelInfo] = useState({         // Information about the model (used in UI)
    vertices: 0,
    faces: 0,
  });

  return (
    <>
      {/* Canvas sets up the 3D rendering environment */}
      <Canvas camera={{ position: [0, 0, 4] }}>
        {/* Lighting for the scene */}
        <ambientLight intensity={0.8} />
        <pointLight position={[10, 10, 10]} />
        <directionalLight position={[2, 2, 2]} intensity={0.5} />

        {/* OrbitControls allows the user to rotate the camera using mouse input */}
        <OrbitControls />

        {/* Load and render the model with selected visual mode */}
        <Model mode={mode} setInfo={setModelInfo} />

        {/* Show frame rate and render performance */}
        <Stats />
      </Canvas>

      {/* Interface to change rendering modes and display model stats */}
      <div className="controls">
        <h3>View Mode</h3>
        <button onClick={() => setMode('default')}>Default</button>
        <button onClick={() => setMode('edges')}>Edges</button>
        <button onClick={() => setMode('wireframe')}>Wireframe</button>
        <button onClick={() => setMode('points')}>Points</button>

        <div className="info">
          <h4>Model Info</h4>
          <p>Vertices: {modelInfo.vertices}</p>
          <p>Faces: {modelInfo.faces}</p>
        </div>
      </div>
    </>
  );
}
