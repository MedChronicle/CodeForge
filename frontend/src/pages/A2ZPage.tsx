import { useEffect, useMemo, useState } from 'react';
import { AnimatePresence, motion } from 'framer-motion';
import { ArrowRight, ChevronDown, Flame, Map as MapIcon, Search, Sparkles, Trophy } from 'lucide-react';
import { Link } from 'react-router-dom';
import { problemApi } from '../api/problemApi';
import { resourceApi } from '../api/resourceApi';
import { ProblemCard } from '../components/problems/ProblemCard';
import { Badge } from '../components/ui/Badge';
import { Button } from '../components/ui/Button';
import { Card } from '../components/ui/Card';
import { EmptyState } from '../components/common/EmptyState';
import { ErrorState } from '../components/common/ErrorState';
import { LoadingScreen } from '../components/common/LoadingScreen';
import { A2Z_MODULES } from '../lib/constants';
import { apiErrorMessage, percentage } from '../lib/utils';
import type { Problem, Progress, Topic } from '../types/api';

type Module = typeof A2Z_MODULES[number];

function ModuleCard({ module, topic, problems, progress, open, onToggle }: { module: Module; topic?: Topic; problems: Problem[]; progress: Progress[]; open: boolean; onToggle: () => void }) {
  const progressMap = new Map(progress.map((item) => [item.problem_id, item]));
  const solved = problems.filter((problem) => progressMap.get(problem.id)?.status === 'solved').length;
  const completion = solved / Math.max(1, problems.length);
  return <motion.section layout className="overflow-hidden rounded-3xl border border-white/[.08] bg-white/[.025]" style={{ ['--module-accent' as string]: module.accent }}><button onClick={onToggle} className="group flex w-full items-center gap-4 p-5 text-left sm:p-6"><div className="relative flex h-14 w-14 shrink-0 items-center justify-center rounded-2xl border border-white/10 bg-white/[.04] font-mono text-sm font-semibold" style={{ color: module.accent, boxShadow: `0 0 28px ${module.accent}24` }}><span className="absolute -right-1 -top-1 h-2.5 w-2.5 rounded-full" style={{ background: module.accent, boxShadow: `0 0 12px ${module.accent}` }} />{module.stage}</div><div className="min-w-0 flex-1"><div className="flex flex-wrap items-center gap-2"><span className="text-[10px] font-bold uppercase tracking-[.2em] text-slate-500">{module.track}</span>{completion === 1 && <Badge className="border-mint/20 bg-mint/10 text-mint"><Trophy size={11} className="mr-1" />Complete</Badge>}</div><div className="mt-1 flex items-center gap-2"><h2 className="font-display text-xl font-semibold">{topic?.name ?? module.slug}</h2><span className="truncate text-xs text-slate-500">{module.tagline}</span></div><div className="mt-3 flex items-center gap-3"><div className="h-1.5 max-w-48 flex-1 overflow-hidden rounded-full bg-white/[.08]"><motion.div initial={false} animate={{ width: `${completion * 100}%` }} className="h-full rounded-full" style={{ background: module.accent }} /></div><span className="font-mono text-[11px] text-slate-500">{solved}/{problems.length}</span></div></div><motion.div animate={{ rotate: open ? 180 : 0 }} className="text-slate-500"><ChevronDown size={18} /></motion.div></button><AnimatePresence initial={false}>{open && <motion.div initial={{ height: 0, opacity: 0 }} animate={{ height: 'auto', opacity: 1 }} exit={{ height: 0, opacity: 0 }} transition={{ duration: .25 }}><div className="border-t border-white/[.07] p-5 sm:p-6"><div className="mb-5 flex flex-wrap items-center justify-between gap-3"><div className="text-sm text-slate-400">{topic?.description}</div><Link to={`/app/sheet?topic=${module.slug}`} className="inline-flex items-center gap-1 text-xs font-semibold text-cyan hover:underline">Open in catalog <ArrowRight size={13} /></Link></div>{problems.length ? <div className="grid gap-3 lg:grid-cols-2">{problems.map((problem) => { const item = progressMap.get(problem.id); return <ProblemCard key={problem.id} problem={problem} status={item?.status} bookmarked={item?.bookmarked} />; })}</div> : <EmptyState title="Problems are loading into this module" description="Seed the catalog or refresh the API to populate this A2Z stage." />}</div></motion.div>}</AnimatePresence></motion.section>;
}

export function A2ZPage() {
  const [topics, setTopics] = useState<Topic[]>([]);
  const [problems, setProblems] = useState<Problem[]>([]);
  const [progress, setProgress] = useState<Progress[]>([]);
  const [openModule, setOpenModule] = useState('arrays');
  const [query, setQuery] = useState('');
  const [onlyIncomplete, setOnlyIncomplete] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  useEffect(() => {
    void Promise.all([
      resourceApi.topics(),
      problemApi.list({ page: 1, page_size: 100 }),
      problemApi.list({ page: 2, page_size: 100 }),
      problemApi.progress(),
    ]).then(([nextTopics, firstPage, secondPage, nextProgress]) => {
      setTopics(nextTopics);
      setProblems([...firstPage.items, ...secondPage.items]);
      setProgress(nextProgress);
    }).catch((err) => setError(apiErrorMessage(err, 'Could not load the A2Z roadmap.'))).finally(() => setLoading(false));
  }, []);
  const visibleModules = useMemo(() => A2Z_MODULES.filter((module) => {
    const topic = topics.find((item) => item.slug === module.slug);
    const moduleProblems = problems.filter((problem) => problem.topic_slug === module.slug);
    const solved = moduleProblems.filter((problem) => progress.find((item) => item.problem_id === problem.id)?.status === 'solved').length;
    return (!onlyIncomplete || solved < moduleProblems.length) && (!query || `${topic?.name ?? module.slug} ${module.track} ${module.tagline}`.toLowerCase().includes(query.toLowerCase()));
  }), [onlyIncomplete, problems, progress, query, topics]);
  const totalSolved = problems.filter((problem) => progress.find((item) => item.problem_id === problem.id)?.status === 'solved').length;
  const completeModules = A2Z_MODULES.filter((module) => {
    const moduleProblems = problems.filter((problem) => problem.topic_slug === module.slug);
    return moduleProblems.length > 0 && moduleProblems.every((problem) => progress.find((item) => item.problem_id === problem.id)?.status === 'solved');
  }).length;
  if (loading) return <LoadingScreen label="Mapping your A2Z roadmap..." />;
  if (error) return <ErrorState message={error} />;
  return <div className="space-y-7"><div className="relative overflow-hidden rounded-[2rem] border border-violet/20 bg-mesh p-7 shadow-neon sm:p-10"><div className="pointer-events-none absolute -right-16 -top-24 h-64 w-64 rounded-full bg-cyan/20 blur-3xl" /><div className="pointer-events-none absolute -bottom-24 left-1/3 h-64 w-64 rounded-full bg-violet/20 blur-3xl" /><div className="relative"><div className="mb-4 flex items-center gap-2 text-xs font-bold uppercase tracking-[.25em] text-cyan"><MapIcon size={15} /> AlgoForge A2Z roadmap</div><h1 className="max-w-3xl font-display text-4xl font-bold tracking-tight sm:text-5xl">The structured path from first pattern to interview depth.</h1><p className="mt-4 max-w-2xl text-sm leading-7 text-slate-300/75">A Striver-style, stage-by-stage route built from AlgoForge’s curated metadata catalog. It is inspired by the progression model, not an official copy or endorsement.</p><div className="mt-8 grid gap-3 sm:grid-cols-3"><div className="rounded-2xl border border-white/10 bg-black/10 p-4"><div className="font-display text-2xl font-bold">{totalSolved}<span className="text-sm text-slate-500">/{problems.length}</span></div><div className="mt-1 text-xs text-slate-500">problems forged</div></div><div className="rounded-2xl border border-white/10 bg-black/10 p-4"><div className="font-display text-2xl font-bold">{completeModules}<span className="text-sm text-slate-500">/18</span></div><div className="mt-1 text-xs text-slate-500">modules complete</div></div><div className="rounded-2xl border border-white/10 bg-black/10 p-4"><div className="font-display text-2xl font-bold">{percentage(totalSolved / Math.max(1, problems.length))}</div><div className="mt-1 text-xs text-slate-500">roadmap momentum</div></div></div></div></div><Card className="flex flex-col gap-3 p-3 md:flex-row md:items-center"><label className="relative flex-1"><Search size={16} className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-500" /><input value={query} onChange={(event) => setQuery(event.target.value)} placeholder="Find a stage: graphs, DP, heaps..." className="w-full rounded-xl border border-white/[.08] bg-black/10 py-3 pl-9 pr-3 text-sm outline-none focus:border-violet" /></label><Button variant={onlyIncomplete ? 'primary' : 'secondary'} size="sm" onClick={() => setOnlyIncomplete((value) => !value)}><Flame size={15} />{onlyIncomplete ? 'Incomplete only' : 'Show all'}</Button><Button variant="ghost" size="sm" onClick={() => setOpenModule(openModule === 'arrays' ? '' : 'arrays')}><Sparkles size={15} />{openModule === 'arrays' ? 'Collapse first' : 'Open first'}</Button></Card><div className="space-y-4">{visibleModules.map((module) => <ModuleCard key={module.slug} module={module} topic={topics.find((topic) => topic.slug === module.slug)} problems={problems.filter((problem) => problem.topic_slug === module.slug)} progress={progress} open={openModule === module.slug} onToggle={() => setOpenModule((current) => current === module.slug ? '' : module.slug)} />)}</div>{visibleModules.length === 0 && <EmptyState title="No roadmap stages match" description="Try a broader search or switch back to all modules." />}</div>;
}
