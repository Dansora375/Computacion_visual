// BoxItem.jsx
import React, { useRef } from 'react';
import { useFrame } from '@react-three/fiber';

function BoxItem({ position, color, scale, rotate, rotationSpeed }) {
  const ref = useRef();

  useFrame(() => {
    if (rotate && ref.current) {
      ref.current.rotation.y += rotationSpeed;
    }
  });

  return (
    <mesh ref={ref} position={position} scale={scale}>
      <boxGeometry args={[1, 1, 1]} />
      <meshStandardMaterial color={color} />
    </mesh>
  );
}

export default BoxItem;
