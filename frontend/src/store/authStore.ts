import { create } from 'zustand';
import { authApi } from '../api/authApi';
import { clearTokens, readAccessToken, saveTokens } from '../lib/storage';
import type { Profile, User } from '../types/api';

interface AuthState {
  user: User | null;
  profile: Profile | null;
  isLoading: boolean;
  accessToken: string | null;
  signIn: (email: string, password: string) => Promise<void>;
  signUp: (email: string, password: string, displayName: string) => Promise<void>;
  hydrate: () => Promise<void>;
  setProfile: (profile: Profile) => void;
  signOut: () => Promise<void>;
}

export const useAuthStore = create<AuthState>((set) => ({
  user: null,
  profile: null,
  isLoading: true,
  accessToken: readAccessToken(),
  signIn: async (email, password) => {
    const response = await authApi.login({ email, password });
    saveTokens(response.access_token, response.refresh_token);
    const profile = await authApi.profile();
    set({ user: response.user, profile, accessToken: response.access_token, isLoading: false });
  },
  signUp: async (email, password, displayName) => {
    const response = await authApi.register({ email, password, display_name: displayName });
    saveTokens(response.access_token, response.refresh_token);
    const profile = await authApi.profile();
    set({ user: response.user, profile, accessToken: response.access_token, isLoading: false });
  },
  hydrate: async () => {
    if (!readAccessToken()) {
      set({ isLoading: false });
      return;
    }
    try {
      const [user, profile] = await Promise.all([authApi.me(), authApi.profile()]);
      set({ user, profile, accessToken: readAccessToken(), isLoading: false });
    } catch {
      clearTokens();
      set({ user: null, profile: null, accessToken: null, isLoading: false });
    }
  },
  setProfile: (profile) => set({ profile }),
  signOut: async () => {
    const refresh = typeof window !== 'undefined' ? window.localStorage.getItem('algoforge.refresh') : null;
    if (refresh) {
      try {
        await authApi.logout(refresh);
      } catch {
        // The local session is still cleared if the server is unavailable.
      }
    }
    clearTokens();
    set({ user: null, profile: null, accessToken: null });
  },
}));
