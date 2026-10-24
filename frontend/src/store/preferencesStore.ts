import { create } from 'zustand';

type Theme = 'dark' | 'light';

interface PreferencesState {
  theme: Theme;
  language: string;
  toggleTheme: () => void;
  setLanguage: (language: string) => void;
}

function readStoredTheme(): Theme | null {
  if (typeof window === 'undefined') return null;
  return window.localStorage.getItem('algoforge.theme') as Theme | null;
}

function readStoredLanguage(): string | null {
  if (typeof window === 'undefined') return null;
  return window.localStorage.getItem('algoforge.language');
}

const storedTheme = readStoredTheme();
const storedLanguage = readStoredLanguage();

export const usePreferencesStore = create<PreferencesState>((set) => ({
  theme: storedTheme ?? 'dark',
  language: storedLanguage ?? 'python',
  toggleTheme: () =>
    set((state) => {
      const theme = state.theme === 'dark' ? 'light' : 'dark';
      localStorage.setItem('algoforge.theme', theme);
      document.documentElement.dataset.theme = theme;
      return { theme };
    }),
  setLanguage: (language) => {
    localStorage.setItem('algoforge.language', language);
    set({ language });
  },
}));
