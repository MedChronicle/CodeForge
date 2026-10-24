export interface OnboardingDraft {
  experience_level: string;
  self_ratings: Record<string, number>;
  preferred_languages: string[];
  goal: string;
  timeline_days: number;
  daily_minutes: number;
}

export const ONBOARDING_TOPICS = [
  'arrays',
  'strings',
  'recursion',
  'linked-list',
  'trees',
  'graphs',
  'dynamic-programming',
  'greedy',
];
