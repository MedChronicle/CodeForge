import { AnimatePresence, motion } from 'framer-motion';

const colors = ['#8b5cf6', '#22d3ee', '#34d399', '#fbbf24', '#fb7185'];

export function ConfettiBurst({ show }: { show: boolean }) {
  return <AnimatePresence>{show && <div aria-hidden="true" className="pointer-events-none fixed inset-0 z-50 overflow-hidden">{Array.from({ length: 28 }, (_, index) => <motion.span key={index} initial={{ opacity: 1, x: '50vw', y: '45vh', rotate: 0, scale: .4 }} animate={{ opacity: 0, x: `${50 + Math.cos(index * 1.9) * (18 + index % 7 * 4)}vw`, y: `${58 + Math.sin(index * 1.7) * 25}vh`, rotate: 360 + index * 45, scale: 1 }} transition={{ duration: 1.25, delay: index * .012, ease: 'easeOut' }} className="absolute h-2.5 w-1.5 rounded-sm" style={{ backgroundColor: colors[index % colors.length] }} />)}</div>}</AnimatePresence>;
}
