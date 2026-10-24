import { useMemo } from 'react';
import { Canvas } from '@react-three/fiber';
import { Float, Line, OrbitControls } from '@react-three/drei';
import type { Topic } from '../../types/api';

function Constellation({ topics }: { topics: { topic: string; mastery: number }[] }) {
  const points = useMemo(() => topics.slice(0, 12).map((item, index) => {
    const angle = (index / Math.max(1, topics.length)) * Math.PI * 2;
    const radius = 1.8 + (index % 3) * .5;
    return { ...item, position: [Math.cos(angle) * radius, Math.sin(angle) * radius, (index % 2) * .35] as [number, number, number] };
  }), [topics]);
  return <group>{points.map((point, index) => <group key={point.topic}><mesh position={point.position} scale={.18 + point.mastery * .4}><sphereGeometry args={[1, 16, 16]} /><meshStandardMaterial color={point.mastery > .7 ? '#34d399' : point.mastery > .4 ? '#fbbf24' : '#fb7185'} emissive={point.mastery > .7 ? '#34d399' : '#8b5cf6'} emissiveIntensity={2} toneMapped={false} /></mesh>{index > 0 && <Line points={[points[index - 1].position, point.position]} color="#8b5cf6" transparent opacity={.25} lineWidth={.6} />}</group>)}</group>;
}

export function SkillConstellation({ topics }: { topics: Array<{ topic: string; mastery: number }> | Topic[] }) {
  const normalized = topics.map((topic) => 'mastery' in topic ? topic : { topic: topic.name, mastery: 0 });
  return <div className="h-64 overflow-hidden rounded-2xl bg-mesh"><Canvas camera={{ position: [0, 0, 7], fov: 50 }}><ambientLight intensity={.5} /><pointLight position={[3, 2, 4]} color="#8b5cf6" intensity={16} /><Float speed={1} floatIntensity={.6}><Constellation topics={normalized} /></Float><OrbitControls enableZoom={false} enablePan={false} autoRotate autoRotateSpeed={.5} /></Canvas></div>;
}
