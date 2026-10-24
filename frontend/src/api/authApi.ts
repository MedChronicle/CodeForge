import { client } from './client';
import type { AuthResponse } from '../types/auth';
import type { Profile, User } from '../types/api';
import type { OnboardingDraft } from '../types/onboarding';

export const authApi = {
  register: async (payload: { email: string; password: string; display_name: string }) =>
    (await client.post<AuthResponse>('/auth/register', payload)).data,
  login: async (payload: { email: string; password: string }) => (await client.post<AuthResponse>('/auth/login', payload)).data,
  refresh: async (refresh_token: string) => (await client.post<AuthResponse>('/auth/refresh', { refresh_token })).data,
  logout: async (refresh_token: string) => (await client.post('/auth/logout', { refresh_token })).data,
  me: async () => (await client.get<User>('/auth/me')).data,
  profile: async () => (await client.get<Profile>('/users/me/profile')).data,
  onboard: async (payload: OnboardingDraft) => (await client.post<Profile>('/users/me/onboarding', payload)).data,
};
