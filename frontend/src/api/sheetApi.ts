import { client } from './client';
import type { LearningSheet } from '../types/api';

export const sheetApi = {
  active: async () => (await client.get<LearningSheet>('/sheet/active')).data,
  generate: async (payload: { goal: string; timeline_days: number; daily_minutes: number; mastery: Record<string, number> }) =>
    (await client.post<LearningSheet>('/sheet/generate', payload)).data,
};
