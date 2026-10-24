import { useEffect, useMemo, useState } from 'react';
import { ExternalLink, FileText, LibraryBig, PlayCircle, Search, Sparkles } from 'lucide-react';
import { resourceApi } from '../api/resourceApi';
import { Card, CardTitle } from '../components/ui/Card';
import { Badge } from '../components/ui/Badge';
import { MarkdownNotes } from '../components/resources/MarkdownNotes';
import { ErrorState } from '../components/common/ErrorState';
import { LoadingScreen } from '../components/common/LoadingScreen';
import type { Resource, Topic } from '../types/api';

export function ResourcesPage() {
  const [topics, setTopics] = useState<Topic[]>([]);
  const [resources, setResources] = useState<Resource[]>([]);
  const [selected, setSelected] = useState('arrays');
  const [search, setSearch] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  useEffect(() => { void Promise.all([resourceApi.topics(), resourceApi.list()]).then(([nextTopics, nextResources]) => { setTopics(nextTopics); setResources(nextResources); if (nextTopics[0]) setSelected(nextTopics[0].slug); }).catch((err) => setError(err instanceof Error ? err.message : 'Could not load the knowledge base.')).finally(() => setLoading(false)); }, []);
  const topic = topics.find((item) => item.slug === selected);
  const visibleResources = useMemo(() => resources.filter((resource) => resource.topic_id === topic?.id && (!search || `${resource.title} ${resource.channel}`.toLowerCase().includes(search.toLowerCase()))), [resources, topic?.id, search]);
  if (loading) return <LoadingScreen label="Loading the knowledge base..." />;
  if (error) return <ErrorState message={error} />;
  return <div className="space-y-7"><div><div className="mb-3 flex items-center gap-2 text-xs font-bold uppercase tracking-[.25em] text-cyan"><LibraryBig size={14} /> Knowledge base</div><h1 className="font-display text-4xl font-bold tracking-tight">Learn the pattern, then forge the rep.</h1><p className="mt-3 max-w-2xl text-sm leading-7 text-slate-400">Accurate notes, complexity reminders, common traps, and links out to free educators. Curated metadata, not copied lessons.</p></div><div className="grid gap-5 lg:grid-cols-[.35fr_.65fr]"><Card className="h-fit"><CardTitle>Topics</CardTitle><div className="mt-4 space-y-1">{topics.map((item) => <button key={item.slug} onClick={() => setSelected(item.slug)} className={`flex w-full items-center justify-between rounded-xl px-3 py-3 text-left text-sm transition ${selected === item.slug ? 'bg-violet/15 text-white' : 'text-slate-400 hover:bg-white/[.05] hover:text-white'}`}><span>{item.name}</span><span className="text-xs text-slate-600">{item.problem_count}</span></button>)}</div></Card><div className="space-y-5"><Card><div className="flex flex-col justify-between gap-4 sm:flex-row sm:items-start"><div><div className="mb-2 flex items-center gap-2"><Sparkles size={17} className="text-violet" /><CardTitle>{topic?.name ?? 'Topic notes'}</CardTitle></div><p className="max-w-xl text-sm leading-6 text-slate-400">{topic?.description}</p></div><label className="relative"><Search size={15} className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-500" /><input value={search} onChange={(event) => setSearch(event.target.value)} placeholder="Search resources" className="rounded-xl border border-white/10 bg-black/10 py-2.5 pl-9 pr-3 text-sm outline-none focus:border-violet" /></label></div><div className="mt-7"><MarkdownNotes markdown={topic?.notes_markdown ?? '# Select a topic'} /></div></Card><div><div className="mb-3 flex items-center justify-between"><h2 className="font-display text-xl font-semibold">Curated resources</h2><span className="text-xs text-slate-500">{visibleResources.length} links</span></div><div className="grid gap-3 md:grid-cols-2">{visibleResources.map((resource) => <a key={resource.id} href={resource.url} target="_blank" rel="noreferrer" className="group rounded-2xl border border-white/[.08] bg-white/[.03] p-4 transition hover:-translate-y-0.5 hover:border-cyan/30"><div className="flex items-start justify-between gap-3"><div className="flex h-9 w-9 items-center justify-center rounded-xl bg-cyan/10 text-cyan">{resource.kind === 'video' ? <PlayCircle size={17} /> : <FileText size={17} />}</div><ExternalLink size={15} className="text-slate-600 transition group-hover:text-cyan" /></div><div className="mt-5 font-semibold">{resource.title}</div><div className="mt-1 flex items-center gap-2"><Badge>{resource.channel}</Badge><span className="text-xs capitalize text-slate-600">{resource.kind}</span></div><p className="mt-3 text-xs leading-5 text-slate-500">{resource.description}</p></a>)}</div></div></div></div></div>;
}
