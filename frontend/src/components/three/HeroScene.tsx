import { Suspense, useEffect, useMemo, useRef, useState } from 'react';
import { Canvas, useFrame, useThree } from '@react-three/fiber';
import { Float, Line, OrbitControls, Stars } from '@react-three/drei';
import * as THREE from 'three';

function DataNode({ position, color, scale = 1 }: { position: [number, number, number]; color: string; scale?: number }) {
  const ref = useRef<THREE.Mesh>(null);
  useFrame((_, delta) => {
    if (ref.current) ref.current.rotation.y += delta * 0.7;
  });
  return <mesh ref={ref} position={position} scale={scale}><sphereGeometry args={[0.18, 20, 20]} /><meshStandardMaterial color={color} emissive={color} emissiveIntensity={2.2} toneMapped={false} /></mesh>;
}

function ForgeGraph() {
  const group = useRef<THREE.Group>(null);
  const nodes: [number, number, number][] = useMemo(() => [
    [-2.4, 1.4, 0], [-1.2, 0.55, 0], [-3.6, 0.55, 0], [-.25, -.35, 0], [-2.1, -.35, 0], [-4.4, -.35, 0], [-3.1, -1.2, 0],
  ], []);
  useFrame((_, delta) => {
    if (group.current) group.current.rotation.y += delta * 0.12;
  });
  return <group ref={group}>
    <Line points={[nodes[0], nodes[1]]} color="#8b5cf6" lineWidth={1} transparent opacity={0.65} />
    <Line points={[nodes[0], nodes[2]]} color="#22d3ee" lineWidth={1} transparent opacity={0.65} />
    <Line points={[nodes[1], nodes[3]]} color="#8b5cf6" lineWidth={1} transparent opacity={0.55} />
    <Line points={[nodes[1], nodes[4]]} color="#22d3ee" lineWidth={1} transparent opacity={0.55} />
    <Line points={[nodes[2], nodes[5]]} color="#22d3ee" lineWidth={1} transparent opacity={0.55} />
    <Line points={[nodes[4], nodes[6]]} color="#34d399" lineWidth={1} transparent opacity={0.55} />
    {nodes.map((position, index) => <DataNode key={index} position={position} color={index % 2 ? '#22d3ee' : '#8b5cf6'} scale={index === 0 ? 1.35 : 1} />)}
  </group>;
}

function LinkedChain() {
  const points: [number, number, number][] = [[1.2, 1.05, .3], [2, .6, .15], [2.8, .2, 0], [3.6, -.2, -.1], [4.4, -.6, -.2]];
  return <group>{points.slice(0, -1).map((point, index) => <Line key={index} points={[point, points[index + 1]]} color="#34d399" lineWidth={1.2} transparent opacity={.6} />)}{points.map((point, index) => <DataNode key={index} position={point} color="#34d399" scale={.72} />)}</group>;
}

function CameraRig() {
  const { camera, pointer } = useThree();
  useFrame(() => {
    camera.position.x += (pointer.x * 0.35 - camera.position.x) * 0.03;
    camera.position.y += (pointer.y * 0.2 - camera.position.y) * 0.03;
    camera.lookAt(0, 0, 0);
  });
  return null;
}

export function HeroScene() {
  const [reduced, setReduced] = useState(false);
  useEffect(() => {
    const media = window.matchMedia('(prefers-reduced-motion: reduce)');
    const update = () => setReduced(media.matches || window.innerWidth < 700);
    update();
    media.addEventListener?.('change', update);
    window.addEventListener('resize', update);
    return () => { media.removeEventListener?.('change', update); window.removeEventListener('resize', update); };
  }, []);
  if (reduced) return <div className="relative h-full min-h-[360px] overflow-hidden rounded-[2rem] bg-mesh"><div className="absolute inset-8 rounded-full border border-violet/30 shadow-neon" /><div className="absolute left-1/2 top-1/2 h-24 w-24 -translate-x-1/2 -translate-y-1/2 rounded-3xl bg-violet/30 shadow-neon" /></div>;
  return <div className="h-full min-h-[360px] overflow-hidden rounded-[2rem] bg-mesh"><Canvas camera={{ position: [0, 0, 8], fov: 48 }} dpr={[1, 1.6]} gl={{ antialias: true, alpha: true }}><Suspense fallback={null}><ambientLight intensity={0.4} /><pointLight position={[2, 2, 5]} intensity={20} color="#8b5cf6" /><pointLight position={[-3, -2, 2]} intensity={15} color="#22d3ee" /><Stars radius={16} depth={12} count={500} factor={1.8} saturation={0} fade speed={.3} /><Float speed={1.2} rotationIntensity={.15} floatIntensity={.6}><ForgeGraph /><LinkedChain /></Float><CameraRig /><OrbitControls enableZoom={false} enablePan={false} autoRotate autoRotateSpeed={.3} /></Suspense></Canvas></div>;
}
