import { Canvas } from '@react-three/fiber'
import { OrbitControls } from '@react-three/drei'
import Experience from './Experience'

export default function App() {
  return (
    <Canvas camera={{ position: [0, 2, 10], fov: 60 }}>
      <ambientLight intensity={0.5} />
      <directionalLight position={[5, 5, 5]} />
      <Experience />
      <OrbitControls />
    </Canvas>
  )
}
