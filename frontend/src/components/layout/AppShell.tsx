import { useState, type ReactNode } from 'react';
import { X } from 'lucide-react';
import { motion } from 'framer-motion';
import { Sidebar } from './Sidebar';
import { Topbar } from './Topbar';

export function AppShell({ children }: { children: ReactNode }) {
  const [mobileOpen, setMobileOpen] = useState(false);
  return <div className="min-h-screen bg-ink text-white"><div className="flex min-h-screen"><Sidebar /><div className="min-w-0 flex-1"><Topbar onMenu={() => setMobileOpen(true)} /><motion.main initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: .35, ease: 'easeOut' }} className="mx-auto max-w-[1500px] px-5 py-8 lg:px-10">{children}</motion.main></div></div>{mobileOpen && <div className="fixed inset-0 z-50 bg-black/60 backdrop-blur-sm lg:hidden" onClick={() => setMobileOpen(false)}><div className="h-full w-80 bg-panel p-5" onClick={(event) => event.stopPropagation()}><div className="mb-8 flex items-center justify-between"><span className="font-display font-bold">Navigation</span><button onClick={() => setMobileOpen(false)} aria-label="Close navigation"><X /></button></div><Sidebar /></div></div>}</div>;
}
