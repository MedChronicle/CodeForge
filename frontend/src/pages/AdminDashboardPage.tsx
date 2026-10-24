import { useEffect, useState } from 'react';
import { Database, FileText, LibraryBig, ShieldCheck, Users } from 'lucide-react';
import { client } from '../api/client';
import { Card, CardTitle } from '../components/ui/Card';
import { ErrorState } from '../components/common/ErrorState';
import { LoadingScreen } from '../components/common/LoadingScreen';

interface AdminStats { users: number; problems: number; topics: number; resources: number; active_sheets: number; }

export function AdminDashboardPage() {
  const [stats, setStats] = useState<AdminStats | null>(null);
  const [error, setError] = useState('');
  useEffect(() => { void client.get<AdminStats>('/admin/stats').then((response) => setStats(response.data)).catch((err) => setError(err instanceof Error ? err.message : 'Could not load admin metrics.')); }, []);
  if (!stats && !error) return <LoadingScreen label="Loading admin studio..." />;
  if (error) return <ErrorState message={error} />;
  const cards = [{ label: 'Learners', value: stats?.users ?? 0, icon: Users, color: 'text-cyan bg-cyan/10' }, { label: 'Problems', value: stats?.problems ?? 0, icon: FileText, color: 'text-violet bg-violet/10' }, { label: 'Topics', value: stats?.topics ?? 0, icon: Database, color: 'text-mint bg-mint/10' }, { label: 'Resources', value: stats?.resources ?? 0, icon: LibraryBig, color: 'text-amber bg-amber/10' }];
  return <div className="space-y-7"><div><div className="mb-3 flex items-center gap-2 text-xs font-bold uppercase tracking-[.25em] text-cyan"><ShieldCheck size={14} /> Admin studio</div><h1 className="font-display text-4xl font-bold tracking-tight">Keep the forge sharp.</h1><p className="mt-3 text-sm text-slate-400">Catalog health and lightweight content operations for AlgoForge.</p></div><div className="grid gap-3 sm:grid-cols-2 xl:grid-cols-4">{cards.map(({ label, value, icon: Icon, color }) => <Card key={label}><div className={`mb-5 flex h-10 w-10 items-center justify-center rounded-xl ${color}`}><Icon size={18} /></div><div className="font-display text-3xl font-bold">{value}</div><div className="mt-1 text-xs text-slate-500">{label}</div></Card>)}</div><Card><CardTitle>Content operations</CardTitle><p className="mt-3 max-w-2xl text-sm leading-7 text-slate-400">The API exposes CRUD endpoints for topics, problems, and resources. This dashboard intentionally keeps the admin surface small and reviewable; use the API docs to manage individual records during development.</p><div className="mt-5 rounded-xl border border-white/[.08] bg-white/[.03] p-4 text-sm text-slate-300">{stats?.active_sheets ?? 0} active learning sheets currently reference the catalog.</div></Card></div>;
}
