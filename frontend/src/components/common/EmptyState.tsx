import { Sparkles } from 'lucide-react';
import { Card } from '../ui/Card';

export function EmptyState({ title, description }: { title: string; description: string }) {
  return <Card className="flex flex-col items-center justify-center py-14 text-center"><Sparkles className="mb-4 text-cyan" /><h3 className="font-display text-lg font-semibold">{title}</h3><p className="mt-2 max-w-md text-sm text-slate-400">{description}</p></Card>;
}
