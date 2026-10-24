import { NavLink } from 'react-router-dom';
import { BarChart3, BookOpen, Boxes, CalendarClock, LogOut, Map, ShieldCheck, Sparkles } from 'lucide-react';
import { cn } from '../../lib/utils';
import { useAuthStore } from '../../store/authStore';

const links = [
  { to: '/app', label: 'Command Center', icon: BarChart3 },
  { to: '/app/sheet', label: 'Practice Sheet', icon: Boxes },
  { to: '/app/a2z', label: 'A2Z Roadmap', icon: Map },
  { to: '/app/revision', label: 'Revision Queue', icon: CalendarClock },
  { to: '/app/resources', label: 'Knowledge Base', icon: BookOpen },
];

export function Sidebar() {
  const { user, signOut } = useAuthStore();
  return <aside className="hidden min-h-screen w-72 shrink-0 border-r border-white/[.08] bg-black/10 px-5 py-6 lg:block"><div className="mb-10 flex items-center gap-3 px-2"><div className="flex h-10 w-10 items-center justify-center rounded-2xl bg-violet shadow-neon"><Sparkles size={20} /></div><div><div className="font-display text-lg font-bold">AlgoForge</div><div className="text-[10px] uppercase tracking-[.25em] text-slate-500">adaptive DSA</div></div></div><nav className="space-y-1">{links.map(({ to, label, icon: Icon }) => <NavLink key={to} to={to} end={to === '/app'} className={({ isActive }) => cn('flex items-center gap-3 rounded-xl px-3 py-3 text-sm transition', isActive ? 'bg-violet/15 text-white shadow-[inset_2px_0_0_#8b5cf6]' : 'text-slate-400 hover:bg-white/[.05] hover:text-white')}><Icon size={18} />{label}</NavLink>)}{user?.is_admin && <NavLink to="/app/admin" className={({ isActive }) => cn('mt-8 flex items-center gap-3 rounded-xl px-3 py-3 text-sm transition', isActive ? 'bg-cyan/10 text-cyan' : 'text-slate-400 hover:bg-white/[.05] hover:text-white')}><ShieldCheck size={18} />Admin studio</NavLink>}</nav><div className="mt-auto pt-16"><div className="mb-3 rounded-2xl border border-white/[.08] bg-white/[.03] p-3"><div className="flex items-center gap-3"><div className="flex h-9 w-9 items-center justify-center rounded-xl bg-gradient-to-br from-violet to-cyan font-bold">{user?.display_name.slice(0, 1).toUpperCase()}</div><div className="min-w-0"><div className="truncate text-sm font-semibold">{user?.display_name}</div><div className="truncate text-xs text-slate-500">{user?.email}</div></div></div></div><button onClick={() => void signOut()} className="flex w-full items-center gap-3 rounded-xl px-3 py-3 text-sm text-slate-400 transition hover:bg-coral/10 hover:text-coral"><LogOut size={17} />Sign out</button></div></aside>;
}
