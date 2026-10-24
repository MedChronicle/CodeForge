import type { ReactNode } from 'react';
import { cn } from '../../lib/utils';

export function Badge({ children, className }: { children: ReactNode; className?: string }) {
  return <span className={cn('inline-flex items-center rounded-full border border-white/10 bg-white/[.05] px-2.5 py-1 text-[11px] font-semibold text-slate-300', className)}>{children}</span>;
}
