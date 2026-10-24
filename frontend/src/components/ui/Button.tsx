import { forwardRef, type ButtonHTMLAttributes, type ReactNode } from 'react';
import { Loader2 } from 'lucide-react';
import { cn } from '../../lib/utils';

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  children: ReactNode;
  variant?: 'primary' | 'secondary' | 'ghost' | 'danger';
  size?: 'sm' | 'md' | 'lg';
  loading?: boolean;
}

export const Button = forwardRef<HTMLButtonElement, ButtonProps>(function Button(
  { children, variant = 'primary', size = 'md', loading = false, className, disabled, ...props },
  ref,
) {
  const variants = {
    primary: 'bg-violet text-white shadow-neon hover:bg-violet/90',
    secondary: 'border border-white/10 bg-white/[.06] text-white hover:bg-white/[.1]',
    ghost: 'text-slate-300 hover:bg-white/[.06] hover:text-white',
    danger: 'border border-coral/25 bg-coral/10 text-coral hover:bg-coral/20',
  };
  const sizes = { sm: 'px-3 py-2 text-xs', md: 'px-4 py-2.5 text-sm', lg: 'px-6 py-3.5 text-base' };
  return (
    <button
      ref={ref}
      className={cn('inline-flex items-center justify-center gap-2 rounded-xl font-semibold transition focus:outline-none focus:ring-2 focus:ring-cyan/70 disabled:cursor-not-allowed disabled:opacity-50', variants[variant], sizes[size], className)}
      disabled={disabled || loading}
      {...props}
    >
      {loading && <Loader2 size={16} className="animate-spin" />}
      {children}
    </button>
  );
});
