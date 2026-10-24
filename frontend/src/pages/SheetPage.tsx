import { useEffect, useMemo, useState } from 'react';
import { CalendarDays, ListFilter, Sparkles } from 'lucide-react';
import { problemApi } from '../api/problemApi';
import { resourceApi } from '../api/resourceApi';
import { sheetApi } from '../api/sheetApi';
import { ProblemFilters, type ProblemFilterState } from '../components/problems/ProblemFilters';
import { TopicSection } from '../components/problems/TopicSection';
import { Card, CardTitle } from '../components/ui/Card';
import { Button } from '../components/ui/Button';
import { ErrorState } from '../components/common/ErrorState';
import { LoadingScreen } from '../components/common/LoadingScreen';
import { EmptyState } from '../components/common/EmptyState';
import { useAuthStore } from '../store/authStore';
import type { Problem, Progress, Topic, LearningSheet } from '../types/api';

export function SheetPage() {
  const profile = useAuthStore((state) => state.profile);
  const [sheet, setSheet] = useState<LearningSheet | null>(null);
  const [problems, setProblems] = useState<Problem[]>([]);
  const [topics, setTopics] = useState<Topic[]>([]);
  const [progress, setProgress] = useState<Progress[]>([]);
  const [filters, setFilters] = useState<ProblemFilterState>({ search: '', topic: '', difficulty: '', status: '' });
  const [view, setView] = useState<'sheet' | 'catalog'>('sheet');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  useEffect(() => { void Promise.all([sheetApi.active().catch(() => null), problemApi.list({ page_size: 100 }), resourceApi.topics(), problemApi.progress()]).then(([nextSheet, nextProblems, nextTopics, nextProgress]) => { setSheet(nextSheet); setProblems(nextProblems.items); setTopics(nextTopics); setProgress(nextProgress); }).catch((err) => setError(err instanceof Error ? err.message : 'Could not load the practice sheet.')).finally(() => setLoading(false)); }, []);
  const filtered = useMemo(() => problems.filter((problem) => (!filters.search || problem.title.toLowerCase().includes(filters.search.toLowerCase())) && (!filters.topic || problem.topic_slug === filters.topic) && (!filters.difficulty || problem.difficulty === filters.difficulty) && (!filters.status || progress.find((item) => item.problem_id === problem.id)?.status === filters.status)), [filters, problems, progress]);
  const groups = useMemo(() => filtered.reduce<Record<string, Problem[]>>((accumulator, problem) => { const key = problem.topic_name ?? 'Core patterns'; (accumulator[key] ??= []).push(problem); return accumulator; }, {}), [filtered]);
  if (loading) return <LoadingScreen label="Loading your forge plan..." />;
  if (error) return <ErrorState message={error} />;
  return <div className="space-y-7"><div className="flex flex-col justify-between gap-5 sm:flex-row sm:items-end"><div><div className="mb-3 flex items-center gap-2 text-xs font-bold uppercase tracking-[.25em] text-cyan"><Sparkles size={14} /> Practice sheet</div><h1 className="font-display text-4xl font-bold tracking-tight">{sheet?.title ?? 'Your adaptive catalog'}</h1><p className="mt-3 max-w-2xl text-sm leading-7 text-slate-400">{sheet ? `${sheet.timeline_days} days · ${sheet.daily_minutes} minutes a day · generated around your ${profile?.goal ?? 'goal'}` : 'Complete onboarding to generate a plan, or explore the full catalog below.'}</p></div><div className="flex gap-2"><Button size="sm" variant={view === 'sheet' ? 'primary' : 'secondary'} onClick={() => setView('sheet')}><CalendarDays size={15} />Day plan</Button><Button size="sm" variant={view === 'catalog' ? 'primary' : 'secondary'} onClick={() => setView('catalog')}><ListFilter size={15} />Catalog</Button></div></div><ProblemFilters value={filters} topics={topics} onChange={setFilters} />{view === 'sheet' && sheet ? <div className="space-y-4">{sheet.days.map((day) => <Card key={day.id} className="p-5"><div className="flex items-center justify-between gap-3"><div><div className="text-xs font-bold uppercase tracking-[.18em] text-violet">Day {day.day_number} · {day.date}</div><h2 className="mt-2 font-display text-xl font-semibold">{day.focus_topic}</h2></div><div className="text-right text-xs text-slate-500">{day.items.length} reps<br /><span className="text-slate-300">{day.estimated_minutes} min</span></div></div><div className="mt-5 grid gap-3 lg:grid-cols-3">{day.items.map((item) => <div key={item.id} className="min-w-0"><div className="mb-2 text-[10px] uppercase tracking-[.15em] text-slate-600">Rep {item.position}</div><a href={`/app/problem/${item.problem.id}`} className="block rounded-xl border border-white/[.07] bg-white/[.025] p-3 text-sm font-semibold transition hover:border-violet/30 hover:text-cyan">{item.problem.title}<div className="mt-2 text-xs font-normal text-slate-500">{item.problem.difficulty} · {item.problem.estimated_minutes} min</div></a></div>)}</div></Card>)}</div> : view === 'sheet' ? <EmptyState title="No plan yet" description="Complete onboarding to generate your first day-wise sheet." /> : Object.keys(groups).length ? <div className="space-y-4">{Object.entries(groups).map(([title, items]) => <TopicSection key={title} title={title} problems={items} progress={progress} />)}</div> : <EmptyState title="No matching problems" description="Try widening your filters or searching for another pattern." />}</div>;
}
