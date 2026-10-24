import { client } from './client';
import type { Analytics, Recommendation } from '../types/api';

export const progressApi = {
  analytics: async () => (await client.get<Analytics>('/analytics/dashboard')).data,
  recommendations: async () => (await client.get<Recommendation[]>('/ml/recommend')).data,
};
