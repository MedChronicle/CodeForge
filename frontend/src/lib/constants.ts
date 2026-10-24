export const API_URL = (import.meta as ImportMeta & { env?: Record<string, string | undefined> }).env?.VITE_API_URL ?? 'http://localhost:8000/api';

export const LANGUAGE_LABELS: Record<string, string> = {
  python: 'Python',
  cpp: 'C++',
  java: 'Java',
  javascript: 'JavaScript',
  go: 'Go',
  csharp: 'C#',
  kotlin: 'Kotlin',
};

export const DIFFICULTY_STYLES: Record<string, string> = {
  Easy: 'text-mint bg-mint/10 border-mint/20',
  Medium: 'text-amber bg-amber/10 border-amber/20',
  Hard: 'text-coral bg-coral/10 border-coral/20',
};

export const A2Z_MODULES = [
  { slug: 'arrays', stage: '01', track: 'Learn the basics', accent: '#8b5cf6', tagline: 'Build the indexing instinct.' },
  { slug: 'strings', stage: '02', track: 'Learn the basics', accent: '#ec4899', tagline: 'Read text as structured data.' },
  { slug: 'hashing', stage: '03', track: 'Learn the basics', accent: '#06b6d4', tagline: 'Trade memory for fast answers.' },
  { slug: 'two-pointers', stage: '04', track: 'Learn the basics', accent: '#14b8a6', tagline: 'Make two indices do one pass.' },
  { slug: 'sliding-window', stage: '05', track: 'Learn the basics', accent: '#22c55e', tagline: 'Turn contiguous constraints linear.' },
  { slug: 'binary-search', stage: '06', track: 'Learn the basics', accent: '#84cc16', tagline: 'Search the answer space.' },
  { slug: 'linked-list', stage: '07', track: 'Linear structures', accent: '#f59e0b', tagline: 'Own every pointer rewrite.' },
  { slug: 'stack-queue', stage: '08', track: 'Linear structures', accent: '#f97316', tagline: 'Process order with intent.' },
  { slug: 'recursion-backtracking', stage: '09', track: 'Recursion & trees', accent: '#ef4444', tagline: 'Explore choices and prune noise.' },
  { slug: 'trees', stage: '10', track: 'Recursion & trees', accent: '#e11d48', tagline: 'Decompose every subtree.' },
  { slug: 'bst', stage: '11', track: 'Recursion & trees', accent: '#db2777', tagline: 'Keep ordered structure honest.' },
  { slug: 'heaps', stage: '12', track: 'Advanced structures', accent: '#c026d3', tagline: 'Keep the best item at the root.' },
  { slug: 'tries', stage: '13', track: 'Advanced structures', accent: '#4f46e5', tagline: 'Make prefixes first-class.' },
  { slug: 'graphs', stage: '14', track: 'Graphs & paradigms', accent: '#9333ea', tagline: 'Traverse the relationships.' },
  { slug: 'dynamic-programming', stage: '15', track: 'Graphs & paradigms', accent: '#7c3aed', tagline: 'Name the state, earn the transition.' },
  { slug: 'greedy', stage: '16', track: 'Graphs & paradigms', accent: '#6366f1', tagline: 'Prove the local choice.' },
  { slug: 'bit-manipulation', stage: '17', track: 'Bit & math', accent: '#2563eb', tagline: 'Compress state into identities.' },
  { slug: 'math', stage: '18', track: 'Bit & math', accent: '#0ea5e9', tagline: 'Spot the invariant hiding in arithmetic.' },
] as const;
