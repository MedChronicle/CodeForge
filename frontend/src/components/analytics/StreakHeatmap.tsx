export function StreakHeatmap({ data }: { data: { date: string; solved: number }[] }) {
  return <div className="grid grid-cols-7 gap-1.5 sm:grid-cols-14">{data.map((item) => <div key={item.date} title={`${item.date}: ${item.solved} solved`} className={`aspect-square rounded-sm ${item.solved >= 3 ? 'bg-mint' : item.solved === 2 ? 'bg-mint/60' : item.solved === 1 ? 'bg-mint/30' : 'bg-white/[.07]'}`} />)}</div>;
}
