import { cn } from '../../lib/utils';

export function ProgressBar({ value, color = 'bg-violet', className }: { value: number; color?: string; className?: string }) {
  return (
    <div className={cn('h-2 overflow-hidden rounded-full bg-white/[.08]', className)} aria-label={`${Math.round(value * 100)} percent complete`}>
      <div className={cn('h-full rounded-full transition-all duration-700', color)} style={{ width: `${Math.max(0, Math.min(1, value)) * 100}%` }} />
    </div>
  );
}
