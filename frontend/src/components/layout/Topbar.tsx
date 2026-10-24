import { Moon, Sun, Bell, Menu } from 'lucide-react';
import { usePreferencesStore } from '../../store/preferencesStore';
import { useAuthStore } from '../../store/authStore';

export function Topbar({ onMenu }: { onMenu?: () => void }) {
  const { theme, toggleTheme } = usePreferencesStore();
  const profile = useAuthStore((state) => state.profile);
  return <header className="sticky top-0 z-20 flex h-20 items-center justify-between border-b border-white/[.08] bg-ink/70 px-5 backdrop-blur-xl lg:px-8"><div className="flex items-center gap-3"><button onClick={onMenu} className="rounded-lg p-2 text-slate-400 hover:bg-white/[.06] lg:hidden" aria-label="Open navigation"><Menu size={20} /></button><div className="text-xs font-semibold uppercase tracking-[.22em] text-slate-500">Your next edge</div></div><div className="flex items-center gap-2"><div className="hidden items-center gap-2 rounded-xl border border-white/[.08] bg-white/[.04] px-3 py-2 text-xs text-slate-400 sm:flex"><span className="h-2 w-2 rounded-full bg-mint shadow-[0_0_12px_#34d399]" />{profile?.current_streak ?? 0} day signal</div><button className="rounded-xl p-2.5 text-slate-400 hover:bg-white/[.06] hover:text-white" aria-label="Notifications"><Bell size={18} /></button><button onClick={toggleTheme} className="rounded-xl p-2.5 text-slate-400 hover:bg-white/[.06] hover:text-white" aria-label="Toggle theme">{theme === 'dark' ? <Sun size={18} /> : <Moon size={18} />}</button></div></header>;
}
