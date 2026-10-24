import { client } from './client';
import type { Problem, ProblemPage, Progress } from '../types/api';

export const problemApi = {
  list: async (params: Record<string, string | number | undefined>) => (await client.get<ProblemPage>('/problems', { params })).data,
  get: async (id: string) => (await client.get<Problem>(`/problems/${id}`)).data,
  updateProgress: async (id: string, payload: Partial<Progress> & { status: string; score?: number }) =>
    (await client.put<Progress>(`/progress/${id}`, payload)).data,
  progress: async () => (await client.get<Progress[]>('/progress')).data,
};
