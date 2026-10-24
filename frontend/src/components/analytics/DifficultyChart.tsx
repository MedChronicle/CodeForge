import { Cell, Pie, PieChart, ResponsiveContainer, Tooltip } from 'recharts';

const colors = ['#34d399', '#fbbf24', '#fb7185'];

export function DifficultyChart({ data }: { data: { difficulty: string; count: number }[] }) {
  return <div className="h-64 w-full"><ResponsiveContainer><PieChart><Pie data={data} dataKey="count" nameKey="difficulty" innerRadius={58} outerRadius={86} paddingAngle={4}>{data.map((item, index) => <Cell key={item.difficulty} fill={colors[index % colors.length]} />)}</Pie><Tooltip contentStyle={{ background: '#111426', border: '1px solid rgba(255,255,255,.1)', borderRadius: 12 }} /></PieChart></ResponsiveContainer></div>;
}
