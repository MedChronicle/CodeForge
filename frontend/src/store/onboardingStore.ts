import { create } from 'zustand';
import { ONBOARDING_TOPICS, type OnboardingDraft } from '../types/onboarding';

interface OnboardingState extends OnboardingDraft {
  step: number;
  setField: <K extends keyof OnboardingDraft>(key: K, value: OnboardingDraft[K]) => void;
  setRating: (topic: string, value: number) => void;
  toggleLanguage: (language: string) => void;
  next: () => void;
  previous: () => void;
  reset: () => void;
}

const initialDraft: OnboardingDraft = {
  experience_level: 'beginner',
  self_ratings: Object.fromEntries(ONBOARDING_TOPICS.map((topic) => [topic, 0])),
  preferred_languages: ['python'],
  goal: 'placements',
  timeline_days: 90,
  daily_minutes: 60,
};

export const useOnboardingStore = create<OnboardingState>((set) => ({
  ...initialDraft,
  step: 0,
  setField: (key, value) => set({ [key]: value } as Partial<OnboardingState>),
  setRating: (topic, value) => set((state) => ({ self_ratings: { ...state.self_ratings, [topic]: value } })),
  toggleLanguage: (language) =>
    set((state) => ({
      preferred_languages: state.preferred_languages.includes(language)
        ? state.preferred_languages.length > 1 ? state.preferred_languages.filter((item) => item !== language) : state.preferred_languages
        : [...state.preferred_languages, language],
    })),
  next: () => set((state) => ({ step: Math.min(3, state.step + 1) })),
  previous: () => set((state) => ({ step: Math.max(0, state.step - 1) })),
  reset: () => set({ ...initialDraft, step: 0 }),
}));
