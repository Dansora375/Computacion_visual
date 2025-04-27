import { useRef } from "react";
import { useFrame } from "@react-three/fiber";
import { useControls } from "leva";

export default function Scene() {
  const parentRef = useRef();
  const childRef = useRef();
  const grandchildRef = useRef(); // Tercer nivel (bonus)

  const { rotationY, positionX } = useControls({
    rotationY: { value: 0, min: -Math.PI, max: Math.PI, step: 0.01 },
    positionX: { value: 0, min: -5, max: 5, step: 0.1 },
  });

  useFrame(() => {
    if (parentRef.current) {
      parentRef.current.rotation.y = rotationY;
      parentRef.current.position.x = positionX;
    }
  });

  return (
    <group ref={parentRef}>
      {/* Nodo padre */}
      <mesh position={[0, 0, 0]}>
        <boxGeometry args={[2, 2, 2]} />
        <meshStandardMaterial color="orange" />
      </mesh>

      {/* Nodo hijo */}
      <group ref={childRef} position={[4, 0, 0]}>
        <mesh>
          <sphereGeometry args={[0.5, 32, 32]} />
          <meshStandardMaterial color="skyblue" />
        </mesh>

        {/* Nodo nieto (tercer nivel) */}
        <group ref={grandchildRef} position={[2, 0, 0]}>
          <mesh>
            <coneGeometry args={[0.5, 1, 32]} />
            <meshStandardMaterial color="limegreen" />
          </mesh>
        </group>
      </group>
    </group>
  );
}
