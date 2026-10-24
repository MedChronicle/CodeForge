export type Difficulty = 'Easy' | 'Medium' | 'Hard';
export type ProgressStatus = 'todo' | 'in_progress' | 'solved' | 'revisit';

export interface User {
  id: string;
  email: string;
  display_name: string;
  is_admin: boolean;
  created_at: string;
}

export interface Profile {
  experience_level: string;
  self_ratings: Record<string, number>;
  preferred_languages: string[];
  goal: string;
  timeline_days: number;
  daily_minutes: number;
  mastery: Record<string, number>;
  xp: number;
  level: number;
  current_streak: number;
  longest_streak: number;
  onboarding_complete: boolean;
}

export interface Topic {
  id: string;
  slug: string;
  name: string;
  description: string;
  order_index: number;
  prerequisites: string[];
  notes_markdown: string;
  color: string;
  problem_count: number;
  resource_count: number;
}

export interface Problem {
  id: string;
  topic_id: string;
  topic_slug?: string | null;
  topic_name?: string | null;
  slug: string;
  title: string;
  difficulty: Difficulty;
  tags: string[];
  companies: string[];
  external_url: string;
  estimated_minutes: number;
  prerequisites: string[];
  starter_templates: Record<string, string>;
  approach_explanations: Record<string, string>;
  popularity_score: number;
}

export interface Resource {
  id: string;
  topic_id: string;
  topic_name?: string | null;
  title: string;
  channel: string;
  url: string;
  kind: string;
  description: string;
}

export interface Pagination {
  page: number;
  page_size: number;
  total: number;
}

export interface ProblemPage {
  items: Problem[];
  pagination: Pagination;
}

export interface Progress {
  id: string;
  problem_id: string;
  status: ProgressStatus;
  notes: string;
  bookmarked: boolean;
  attempts: number;
  hints_used: number;
  total_time_seconds: number;
  last_score: number;
  solved_at?: string | null;
  next_review_at?: string | null;
  interval_days: number;
  repetition: number;
}

export interface SheetItem {
  id: string;
  position: number;
  problem: Problem;
}

export interface SheetDay {
  id: string;
  day_number: number;
  date: string;
  focus_topic: string;
  estimated_minutes: number;
  items: SheetItem[];
}

export interface LearningSheet {
  id: string;
  title: string;
  goal: string;
  timeline_days: number;
  daily_minutes: number;
  starts_on: string;
  days: SheetDay[];
}

export interface Analytics {
  total_problems: number;
  solved_problems: number;
  in_progress_problems: number;
  revisit_problems: number;
  xp: number;
  level: number;
  current_streak: number;
  longest_streak: number;
  solved_over_time: { date: string; solved: number }[];
  mastery_by_topic: { topic: string; mastery: number; solved: number }[];
  difficulty_distribution: { difficulty: string; count: number }[];
  recent_activity: { title: string; status: string; updated_at: string }[];
  badges: { name: string; description: string; unlocked: boolean }[];
}

export interface Recommendation {
  problem_id: string;
  title: string;
  topic: string;
  difficulty: Difficulty;
  score: number;
  reason: string;
}

export interface RevisionItem {
  progress_id: string;
  problem: Problem;
  due_at: string;
  interval_days: number;
  repetition: number;
}
