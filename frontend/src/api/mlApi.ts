import { client } from './client';

export const mlApi = {
  estimate: async (payload: Record<string, unknown>) => (await client.post('/ml/estimate', payload)).data,
};
