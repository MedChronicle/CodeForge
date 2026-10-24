import { Link } from 'react-router-dom';
import { ArrowLeft, Sparkles } from 'lucide-react';
import { HeroScene } from '../three/HeroScene';

export function AuthLayout({ title, subtitle, children }: { title: string; subtitle: string; children: React.ReactNode }) {
  return <div className="min-h-screen bg-ink text-white"><div className="mx-auto grid min-h-screen max-w-7xl lg:grid-cols-[.9fr_1.1fr]"><div className="flex flex-col justify-between p-6 sm:p-10"><Link to="/" className="flex w-fit items-center gap-2 text-sm text-slate-400 hover:text-white"><ArrowLeft size={16} />Back to landing</Link><div className="mx-auto w-full max-w-md py-16"><div className="mb-8 flex items-center gap-3"><div className="flex h-11 w-11 items-center justify-center rounded-2xl bg-violet shadow-neon"><Sparkles size={20} /></div><span className="font-display text-xl font-bold">AlgoForge</span></div><h1 className="font-display text-4xl font-bold tracking-tight sm:text-5xl">{title}</h1><p className="mt-4 text-slate-400">{subtitle}</p><div className="mt-9">{children}</div></div><p className="text-xs text-slate-600">Built for deliberate practice, not endless tabs.</p></div><div className="hidden p-6 lg:block"><HeroScene /></div></div></div>;
}
