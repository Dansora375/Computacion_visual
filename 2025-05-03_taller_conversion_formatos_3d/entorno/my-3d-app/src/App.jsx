import React, { useState } from 'react';
import { Canvas } from '@react-three/fiber';
import { OrbitControls, Center } from '@react-three/drei';
import ModelViewer from './ModelViewer';
import ModelInfo from './ModelInfo';

const App = () => {
  const [modelType, setModelType] = useState('obj');

  return (
    <div style={{ width: '100vw', height: '100vh' }}>
      <select
        onChange={(e) => setModelType(e.target.value)}
        style={{ position: 'absolute', top: 20, left: 20, zIndex: 1 }}
      >
        <option value="obj">OBJ</option>
        <option value="stl">STL</option>
        <option value="gltf">GLTF</option>
      </select>

      <Canvas camera={{ position: [0, 0, 10], near: 0.1, far: 5000, fov: 60 }}>
        {/* Luces */}
        <ambientLight intensity={0.5} />
        <directionalLight position={[10, 10, 10]} intensity={1} />
        <pointLight position={[-10, -10, -10]} intensity={0.8} />

        {/* Controles y modelo */}
        <OrbitControls />
        <Center>
          <ModelViewer type={modelType} />
        </Center>
      </Canvas>

      <ModelInfo modelType={modelType} />
    </div>
  );
};

export default App;
