import React, { useEffect, useRef, useState } from 'react';
import { useLoader, useFrame } from '@react-three/fiber';
import { OBJLoader } from 'three-stdlib';
import { STLLoader } from 'three-stdlib';
import { GLTFLoader } from 'three-stdlib';

const ModelViewer = ({ type }) => {
  const meshRef = useRef();
  const [geometry, setGeometry] = useState(null);
  const [material, setMaterial] = useState(null);

  useEffect(() => {
    const loadModel = async () => {
      if (type === 'obj') {
        const obj = await new OBJLoader().loadAsync('/models/goat.obj');
        const child = obj.children.find((c) => c.isMesh);
        setGeometry(child.geometry);
        setMaterial(child.material);
      } else if (type === 'stl') {
        const geo = await new STLLoader().loadAsync('/models/skull.stl');
        setGeometry(geo);
        setMaterial(null);
      } else if (type === 'gltf') {
        const gltf = await new GLTFLoader().loadAsync('/models/sol.gltf');
        // const mesh = gltf.scene.children.find((c) => c.isMesh);
        let mesh = null;
        gltf.scene.traverse((child) => {
          if (child.isMesh) {
            mesh = child;
          }
        });
        if (!mesh) {
          console.error('No se encontró mesh en el GLTF');
          return; // evita seguir si no hay mesh
        }
        
        // Luego puedes usar:
        setGeometry(mesh.geometry);
        setMaterial(mesh.material);
        // setGeometry(mesh.geometry);
        // setMaterial(mesh.material);
      }
    };

    loadModel();
  }, [type]);

  useFrame(() => {
    if (meshRef.current) meshRef.current.rotation.y += 0.005;
  });

  if (!geometry) return null;

  return (
    <mesh ref={meshRef} geometry={geometry} material={material || undefined}>
      {!material && <meshStandardMaterial color="orange" />}
    </mesh>
  );
};

export default ModelViewer;
