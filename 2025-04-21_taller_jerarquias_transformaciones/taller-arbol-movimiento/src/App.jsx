import { Canvas } from "@react-three/fiber";
import Scene from "./components/Scene";

function App() {
  return (
    <Canvas camera={{ position: [0, 5, 10], fov: 60 }}>
      <ambientLight />
      <pointLight position={[10, 10, 10]} />
      <Scene />
    </Canvas>
  );
}

export default App;
