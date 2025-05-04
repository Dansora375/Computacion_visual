import React, { useEffect, useState } from 'react';
import * as THREE from 'three';
import { OBJLoader, STLLoader, GLTFLoader } from 'three-stdlib';

const ModelInfo = ({ modelType }) => {
  const [info, setInfo] = useState({ vertices: 0, format: modelType });

  useEffect(() => {
    const load = async () => {
      let vertices = 0;

      if (modelType === 'obj') {
        const obj = await new OBJLoader().loadAsync('/models/goat.obj');
        const mesh = obj.children.find((c) => c.isMesh);
        vertices = mesh.geometry.attributes.position.count;

      } else if (modelType === 'stl') {
        const geo = await new STLLoader().loadAsync('/models/skull.stl');
        vertices = geo.attributes.position.count;

      } else if (modelType === 'gltf') {
        const gltf = await new GLTFLoader().loadAsync('/models/sol.gltf');
        let mesh = null;
        gltf.scene.traverse((child) => {
          if (child.isMesh) mesh = child;
        });

        if (!mesh) {
          console.error('No se encontró mesh en el GLTF');
          return;
        }

        vertices = mesh.geometry.attributes.position.count;
      }

      setInfo({ vertices, format: modelType.toUpperCase() });
    };

    load();
  }, [modelType]);

  return (
    <div style={{
      position: 'absolute',
      bottom: 20,
      left: 20,
      background: 'rgba(0,0,0,0.6)',
      padding: '10px',
      color: 'white',
      borderRadius: '8px',
      fontFamily: 'monospace'
    }}>
      <div><strong>Formato:</strong> {info.format}</div>
      <div><strong>Vértices:</strong> {info.vertices}</div>
    </div>
  );
};

export default ModelInfo;
