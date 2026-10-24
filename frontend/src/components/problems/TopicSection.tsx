import { ChevronDown, ChevronRight } from 'lucide-react';
import { useState } from 'react';
import type { Problem, Progress } from '../../types/api';
import { ProgressBar } from '../ui/ProgressBar';
import { ProblemCard } from './ProblemCard';

export function TopicSection({ title, problems, progress }: { title: string; problems: Problem[]; progress: Progress[] }) {
  const [open, setOpen] = useState(true);
  const progressMap = new Map(progress.map((item) => [item.problem_id, item]));
  const solved = problems.filter((problem) => progressMap.get(problem.id)?.status === 'solved').length;
  return <section className="rounded-3xl border border-white/[.08] bg-white/[.02] p-4 sm:p-5"><button onClick={() => setOpen((value) => !value)} className="flex w-full items-center justify-between gap-4 text-left"><div className="flex min-w-0 items-center gap-3">{open ? <ChevronDown size={18} className="text-violet" /> : <ChevronRight size={18} className="text-violet" />}<div><h2 className="font-display text-lg font-semibold">{title}</h2><div className="mt-1 text-xs text-slate-500">{solved} of {problems.length} forged</div></div></div><div className="w-32"><ProgressBar value={solved / Math.max(1, problems.length)} /></div></button>{open && <div className="mt-5 grid gap-3 lg:grid-cols-2">{problems.map((problem) => { const item = progressMap.get(problem.id); return <ProblemCard key={problem.id} problem={problem} status={item?.status} bookmarked={item?.bookmarked} />; })}</div>}</section>;
}
