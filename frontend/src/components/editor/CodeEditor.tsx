import Editor from '@monaco-editor/react';
import { usePreferencesStore } from '../../store/preferencesStore';

const monacoLanguages: Record<string, string> = { python: 'python', cpp: 'cpp', java: 'java', javascript: 'javascript', go: 'go', csharp: 'csharp', kotlin: 'kotlin' };

export function CodeEditor({ templates, onChange }: { templates: Record<string, string>; onChange?: (value: string) => void }) {
  const language = usePreferencesStore((state) => state.language);
  const code = templates[language] ?? templates.python ?? '';
  return <div className="overflow-hidden rounded-2xl border border-white/[.08] bg-[#0b0e1a]"><Editor height="360px" theme="vs-dark" language={monacoLanguages[language] ?? 'plaintext'} value={code} onChange={(value) => onChange?.(value ?? '')} options={{ minimap: { enabled: false }, fontSize: 13, padding: { top: 16, bottom: 16 }, smoothScrolling: true, wordWrap: 'on', scrollBeyondLastLine: false }} /></div>;
}
