import { AlertTriangle } from 'lucide-react';
import { Card } from '../ui/Card';

export function ErrorState({ message }: { message: string }) {
  return <Card className="border-coral/20 bg-coral/[.06] text-coral"><div className="flex items-start gap-3"><AlertTriangle size={18} /><div><h3 className="font-semibold">Something went off-route</h3><p className="mt-1 text-sm text-coral/80">{message}</p></div></div></Card>;
}
