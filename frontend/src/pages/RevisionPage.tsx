import { useEffect, useState } from 'react';
import { Brain, Check, Clock3, RotateCcw, Sparkles } from 'lucide-react';
import { revisionApi } from '../api/revisionApi';
import { Badge } from '../components/ui/Badge';
import { Button } from '../components/ui/Button';
import { Card, CardTitle } from '../components/ui/Card';
import { EmptyState } from '../components/common/EmptyState';
import { ErrorState } from '../components/common/ErrorState';
import { LoadingScreen } from '../components/common/LoadingScreen';
import type { RevisionItem } from '../types/api';
import { formatDate } from '../lib/utils';

export function RevisionPage() {
  const [items, setItems] = useState<RevisionItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [reviewing, setReviewing] = useState<string | null>(null);
  useEffect(() => { void revisionApi.today().then(setItems).catch((err) => setError(err instanceof Error ? err.message : 'Could not load your revision queue.')).finally(() => setLoading(false)); }, []);
  async function review(id: string, quality: number) { setReviewing(id); try { await revisionApi.review(id, quality); setItems((current) => current.filter((item) => item.progress_id !== id)); } catch (err) { setError(err instanceof Error ? err.message : 'Could not schedule the next review.'); } finally { setReviewing(null); } }
  if (loading) return <LoadingScreen label="Checking what is due..." />;
  if (error) return <ErrorState message={error} />;
  return <div className="space-y-7"><div><div className="mb-3 flex items-center gap-2 text-xs font-bold uppercase tracking-[.25em] text-amber"><RotateCcw size={14} /> Memory loop</div><h1 className="font-display text-4xl font-bold tracking-tight">Today’s revision queue.</h1><p className="mt-3 max-w-2xl text-sm leading-7 text-slate-400">Rate the quality of your recall, not how familiar the title looks. AlgoForge uses that signal to schedule the next review.</p></div>{items.length === 0 ? <EmptyState title="Nothing due right now" description="That is a good sign. Solve another problem or come back tomorrow for the next memory check." /> : <div className="grid gap-4 lg:grid-cols-2">{items.map((item) => <Card key={item.progress_id}><div className="flex items-start justify-between gap-4"><div><div className="mb-2 flex items-center gap-2"><Badge className="border-amber/20 bg-amber/10 text-amber">Due {formatDate(item.due_at)}</Badge><span className="text-xs text-slate-600">Review {item.repetition + 1}</span></div><CardTitle>{item.problem.title}</CardTitle><p className="mt-2 text-xs text-slate-500">{item.problem.topic_name} · previous interval {item.interval_days || 0} days</p></div><div className="rounded-xl bg-amber/10 p-2.5 text-amber"><Brain size={18} /></div></div><div className="mt-7 grid grid-cols-3 gap-2"><Button size="sm" variant="danger" loading={reviewing === item.progress_id} onClick={() => void review(item.progress_id, 1)}>Again</Button><Button size="sm" variant="secondary" loading={reviewing === item.progress_id} onClick={() => void review(item.progress_id, 3)}>Good</Button><Button size="sm" loading={reviewing === item.progress_id} onClick={() => void review(item.progress_id, 5)}><Check size={14} />Easy</Button></div></Card>)}</div>}<Card className="flex items-start gap-4 border-cyan/15 bg-cyan/[.04]"><Clock3 className="mt-1 text-cyan" size={18} /><div><div className="font-semibold">Why this works</div><p className="mt-1 text-sm leading-6 text-slate-400">The SM-2 style scheduler gives successful recalls more spacing and brings difficult recalls back quickly. It is a practical memory aid, not a perfect model of forgetting.</p></div><Sparkles className="ml-auto shrink-0 text-cyan" size={17} /></Card></div>;
}
