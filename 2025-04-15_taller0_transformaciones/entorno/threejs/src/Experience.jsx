import { useRef } from 'react'
import { useFrame } from '@react-three/fiber'
import * as THREE from 'three'

export default function Experience() {
  const meshRef = useRef()  // Reference to the mesh

  useFrame(({ clock }) => {
    const t = clock.getElapsedTime()
    const mesh = meshRef.current

    // Circular motion (X and Z positions follow sine and cosine)
    mesh.position.x = Math.cos(t) * 2
    mesh.position.z = Math.sin(t) * 2

    // Continuous rotation on Y and X axes
    mesh.rotation.y += 0.01
    mesh.rotation.x += 0.005

    // Smooth cyclic scaling using sine function
    const scale = 1 + 0.3 * Math.sin(t * 2)
    mesh.scale.set(scale, scale, scale)
  })

  return (
    // A simple orange cube with geometry and material
    <mesh ref={meshRef}>
      <boxGeometry args={[1, 1, 1]} />
      <meshStandardMaterial color="orange" />
    </mesh>
  )
}
