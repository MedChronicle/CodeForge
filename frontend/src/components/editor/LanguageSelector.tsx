import { LANGUAGE_LABELS } from '../../lib/constants';
import { usePreferencesStore } from '../../store/preferencesStore';

export function LanguageSelector({ options }: { options: string[] }) {
  const { language, setLanguage } = usePreferencesStore();
  return <label className="flex items-center gap-2 text-xs text-slate-500">Language<select value={options.includes(language) ? language : options[0] ?? 'python'} onChange={(event) => setLanguage(event.target.value)} className="rounded-lg border border-white/10 bg-panel px-2 py-1.5 text-xs text-slate-200 outline-none focus:border-violet">{options.map((value) => <option key={value} value={value}>{LANGUAGE_LABELS[value] ?? value}</option>)}</select></label>;
}
