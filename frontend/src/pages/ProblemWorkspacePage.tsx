import { useEffect, useMemo, useState } from 'react';
import { ArrowLeft, BookOpen, CheckCircle2, ExternalLink, FileText, PlayCircle, RotateCcw, Save, Sparkles } from 'lucide-react';
import { useNavigate, useParams } from 'react-router-dom';
import { problemApi } from '../api/problemApi';
import { CodeEditor } from '../components/editor/CodeEditor';
import { LanguageSelector } from '../components/editor/LanguageSelector';
import { Badge } from '../components/ui/Badge';
import { Button } from '../components/ui/Button';
import { Card, CardTitle } from '../components/ui/Card';
import { ConfettiBurst } from '../components/common/ConfettiBurst';
import { ErrorState } from '../components/common/ErrorState';
import { LoadingScreen } from '../components/common/LoadingScreen';
import { DIFFICULTY_STYLES } from '../lib/constants';
import { apiErrorMessage } from '../lib/utils';
import type { Problem, ProgressStatus } from '../types/api';

export function ProblemWorkspacePage() {
  const { problemId } = useParams();
  const navigate = useNavigate();
  const [problem, setProblem] = useState<Problem | null>(null);
  const [status, setStatus] = useState<ProgressStatus>('todo');
  const [notes, setNotes] = useState('');
  const [bookmarked, setBookmarked] = useState(false);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [celebrating, setCelebrating] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    if (!problemId) return;
    void Promise.all([problemApi.get(problemId), problemApi.progress()])
      .then(([nextProblem, progress]) => {
        setProblem(nextProblem);
        const existing = progress.find((item) => item.problem_id === problemId);
        if (existing) {
          setStatus(existing.status);
          setNotes(existing.notes);
          setBookmarked(existing.bookmarked);
        }
      })
      .catch((err) => setError(apiErrorMessage(err, 'Could not open this problem.')))
      .finally(() => setLoading(false));
  }, [problemId]);

  const languages = useMemo(() => problem ? Object.keys(problem.starter_templates) : ['python'], [problem]);

  async function save(nextStatus = status) {
    if (!problemId) return;
    setSaving(true);
    setError('');
    try {
      await problemApi.updateProgress(problemId, {
        status: nextStatus,
        notes,
        bookmarked,
        attempts: 1,
        hints_used: 0,
        total_time_seconds: 0,
        score: nextStatus === 'solved' ? 1 : 0,
      });
      setStatus(nextStatus);
      if (nextStatus === 'solved' && status !== 'solved') {
        setCelebrating(true);
        window.setTimeout(() => setCelebrating(false), 1500);
      }
    } catch (err) {
      setError(apiErrorMessage(err, 'Could not save progress.'));
    } finally {
      setSaving(false);
    }
  }

  if (loading) return <LoadingScreen label="Opening the workspace..." />;
  if (error && !problem) return <ErrorState message={error} />;
  if (!problem) return <ErrorState message="Problem not found" />;

  const statusButton = (value: ProgressStatus, label: string, icon: React.ReactNode, activeClass: string) => (
    <button onClick={() => void save(value)} className={`rounded-xl border px-3 py-3 text-xs font-semibold transition ${status === value ? activeClass : 'border-white/[.08] text-slate-500 hover:border-white/20 hover:text-white'}`}>
      <span className="mx-auto mb-2 flex justify-center">{icon}</span>{label}
    </button>
  );

  return <>
    <ConfettiBurst show={celebrating} />
    <div className="space-y-6">
      <button onClick={() => navigate(-1)} className="inline-flex items-center gap-2 text-sm text-slate-500 transition hover:text-white"><ArrowLeft size={15} />Back to sheet</button>
      {error && <div className="rounded-xl border border-coral/25 bg-coral/10 p-3 text-sm text-coral">{error}</div>}
      <div className="grid gap-5 xl:grid-cols-[1.1fr_.9fr]">
        <div className="space-y-5">
          <Card>
            <div className="flex flex-wrap items-center gap-2"><Badge className={DIFFICULTY_STYLES[problem.difficulty]}>{problem.difficulty}</Badge><Badge>{problem.estimated_minutes} min</Badge>{problem.tags.map((tag) => <Badge key={tag}>#{tag}</Badge>)}</div>
            <h1 className="mt-5 font-display text-3xl font-bold tracking-tight">{problem.title}</h1>
            <div className="mt-4 flex flex-wrap items-center gap-4 text-xs text-slate-500"><span>{problem.topic_name}</span><span>Companies: {problem.companies.join(', ')}</span><a href={problem.external_url} target="_blank" rel="noreferrer" className="inline-flex items-center gap-1 text-cyan hover:underline">Open original <ExternalLink size={12} /></a></div>
            <div className="mt-7 grid gap-2 sm:grid-cols-4">
              {statusButton('todo', 'Todo', <FileText size={15} />, 'border-slate-400/30 bg-white/[.08] text-white')}
              {statusButton('in_progress', 'In progress', <PlayCircle size={15} />, 'border-cyan/30 bg-cyan/10 text-cyan')}
              {statusButton('solved', 'Solved', <CheckCircle2 size={15} />, 'border-mint/30 bg-mint/10 text-mint')}
              {statusButton('revisit', 'Revisit', <RotateCcw size={15} />, 'border-amber/30 bg-amber/10 text-amber')}
            </div>
          </Card>
          <Card>
            <div className="flex items-center justify-between"><div><CardTitle>Scratchpad</CardTitle><p className="mt-1 text-xs text-slate-500">Starter code is a blank canvas; execution is intentionally local-only.</p></div><LanguageSelector options={languages} /></div>
            <div className="mt-4"><CodeEditor templates={problem.starter_templates} /></div>
          </Card>
        </div>
        <div className="space-y-5">
          <Card><div className="flex items-center justify-between"><div><CardTitle>Approach signal</CardTitle><p className="mt-1 text-xs text-slate-500">Read this before opening an editorial.</p></div><Sparkles size={18} className="text-violet" /></div><p className="mt-5 text-sm leading-7 text-slate-300">{problem.approach_explanations.python ?? Object.values(problem.approach_explanations)[0]}</p></Card>
          <Card><div className="flex items-center justify-between"><CardTitle>Working notes</CardTitle><button onClick={() => setBookmarked((value) => !value)} className={`text-xs ${bookmarked ? 'text-amber' : 'text-slate-500'}`}>{bookmarked ? 'Bookmarked' : 'Bookmark'}</button></div><textarea value={notes} onChange={(event) => setNotes(event.target.value)} placeholder="What invariant did you find? What would you forget tomorrow?" className="mt-4 min-h-44 w-full resize-y rounded-xl border border-white/[.08] bg-black/10 p-3 text-sm leading-6 text-slate-200 outline-none focus:border-violet" /><Button onClick={() => void save()} loading={saving} className="mt-3 w-full"><Save size={15} />Save progress</Button></Card>
          <Card><div className="flex items-center gap-3"><BookOpen className="text-cyan" size={18} /><div><CardTitle className="text-base">Prerequisite pulse</CardTitle><p className="mt-1 text-xs text-slate-500">{problem.prerequisites.length ? problem.prerequisites.join(' · ') : 'No prerequisite topics listed.'}</p></div></div></Card>
        </div>
      </div>
    </div>
  </>;
}
