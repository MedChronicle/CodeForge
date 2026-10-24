import { client } from './client';
import type { Resource, Topic } from '../types/api';

export const resourceApi = {
  topics: async () => (await client.get<Topic[]>('/topics')).data,
  topic: async (slug: string) => (await client.get<Topic>(`/topics/${slug}`)).data,
  list: async (topic?: string) => (await client.get<Resource[]>('/resources', { params: { topic } })).data,
};
