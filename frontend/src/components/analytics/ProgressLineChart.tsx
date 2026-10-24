import { CartesianGrid, Line, LineChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts';

export function ProgressLineChart({ data }: { data: { date: string; solved: number }[] }) {
  return <div className="h-64 w-full"><ResponsiveContainer><LineChart data={data}><CartesianGrid stroke="rgba(255,255,255,.06)" vertical={false} /><XAxis dataKey="date" tick={{ fill: '#64748b', fontSize: 10 }} tickFormatter={(value) => value.slice(5)} axisLine={false} tickLine={false} /><YAxis allowDecimals={false} tick={{ fill: '#64748b', fontSize: 10 }} axisLine={false} tickLine={false} /><Tooltip contentStyle={{ background: '#111426', border: '1px solid rgba(255,255,255,.1)', borderRadius: 12, color: '#fff' }} /><Line type="monotone" dataKey="solved" stroke="#22d3ee" strokeWidth={3} dot={{ fill: '#22d3ee', r: 3 }} activeDot={{ r: 5 }} /></LineChart></ResponsiveContainer></div>;
}
