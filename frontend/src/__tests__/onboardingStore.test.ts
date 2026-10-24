import { act } from '@testing-library/react';
import { useOnboardingStore } from '../store/onboardingStore';
import { ONBOARDING_TOPICS } from '../types/onboarding';

describe('onboarding store', () => {
  beforeEach(() => useOnboardingStore.getState().reset());

  it('keeps at least one selected language', () => {
    act(() => useOnboardingStore.getState().toggleLanguage('python'));
    expect(useOnboardingStore.getState().preferred_languages).toEqual(['python']);
    act(() => useOnboardingStore.getState().toggleLanguage('java'));
    expect(useOnboardingStore.getState().preferred_languages).toEqual(['python', 'java']);
    act(() => useOnboardingStore.getState().toggleLanguage('python'));
    expect(useOnboardingStore.getState().preferred_languages).toEqual(['java']);
  });

  it('starts with a zero rating for every assessment topic so a cold start is submittable', () => {
    const ratings = useOnboardingStore.getState().self_ratings;
    expect(Object.keys(ratings)).toEqual(ONBOARDING_TOPICS);
    expect(Object.values(ratings).every((rating) => rating === 0)).toBe(true);
  });
});
