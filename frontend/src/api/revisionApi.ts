import { client } from './client';
import type { RevisionItem } from '../types/api';

export const revisionApi = {
  today: async () => (await client.get<RevisionItem[]>('/revision/today')).data,
  review: async (progressId: string, quality: number) =>
    (await client.post<RevisionItem>(`/revision/${progressId}/review`, { quality })).data,
};
