import { PolarAngleAxis, PolarGrid, PolarRadiusAxis, Radar, RadarChart, ResponsiveContainer, Tooltip } from 'recharts';

export function MasteryRadar({ data }: { data: { topic: string; mastery: number }[] }) {
  return <div className="h-72 w-full"><ResponsiveContainer><RadarChart data={data.slice(0, 8)} outerRadius="70%"><PolarGrid stroke="rgba(255,255,255,.1)" /><PolarAngleAxis dataKey="topic" tick={{ fill: '#94a3b8', fontSize: 9 }} tickFormatter={(value) => value.replaceAll('-', ' ').slice(0, 12)} /><PolarRadiusAxis domain={[0, 1]} tick={false} axisLine={false} /><Radar name="Mastery" dataKey="mastery" stroke="#8b5cf6" fill="#8b5cf6" fillOpacity={.3} /><Tooltip contentStyle={{ background: '#111426', border: '1px solid rgba(255,255,255,.1)', borderRadius: 12 }} /></RadarChart></ResponsiveContainer></div>;
}
