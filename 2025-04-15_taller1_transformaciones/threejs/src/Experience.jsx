import { useRef } from 'react'
import { useFrame } from '@react-three/fiber'
import * as THREE from 'three'

export default function Experience() {
  const meshRef = useRef()

  useFrame(({ clock }) => {
    const t = clock.getElapsedTime()
    const mesh = meshRef.current

    // Movimiento circular
    mesh.position.x = Math.cos(t) * 2
    mesh.position.z = Math.sin(t) * 2

    // Rotación continua
    mesh.rotation.y += 0.01
    mesh.rotation.x += 0.005

    // Escalado suave
    const scale = 1 + 0.3 * Math.sin(t * 2)
    mesh.scale.set(scale, scale, scale)
  })

  return (
    <mesh ref={meshRef}>
      <boxGeometry args={[1, 1, 1]}/>
      <meshStandardMaterial color="orange" />
    </mesh>
  )
}
