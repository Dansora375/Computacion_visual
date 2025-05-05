// Scene.jsx
import React from 'react';
import { useControls } from 'leva';
import { Box } from '@react-three/drei';
import BoxItem from './BoxItem';

const data = [
  { id: 1, x: -2, color: 'red', scale: 1, rotate: false },
  { id: 2, x: 0, color: 'green', scale: 1.5, rotate: true },
  { id: 3, x: 2, color: 'blue', scale: 1, rotate: false },
];

function Scene() {
  const { globalScale, rotationSpeed } = useControls('Controls', {
    globalScale: { value: 1, min: 0.5, max: 2 },
    rotationSpeed: { value: 0.01, min: 0, max: 0.1 }
  });

  return (
    <>
      {data.map((item) => (
        <BoxItem
          key={item.id}
          position={[item.x, 0, 0]}
          color={item.color}
          scale={item.scale * globalScale}
          rotate={item.rotate}
          rotationSpeed={rotationSpeed}
        />
      ))}
    </>
  );
}

export default Scene;
