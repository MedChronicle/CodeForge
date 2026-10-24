import { screen } from '@testing-library/react';
import { ProblemCard } from '../components/problems/ProblemCard';
import { renderWithRouter } from '../test/test-utils';
import type { Problem } from '../types/api';

const problem: Problem = {
  id: '1', topic_id: 'topic', topic_slug: 'arrays', topic_name: 'Arrays', slug: 'two-sum', title: 'Two Sum', difficulty: 'Easy', tags: ['hash-map'], companies: ['Google'], external_url: 'https://leetcode.com/problems/two-sum/', estimated_minutes: 20, prerequisites: [], starter_templates: {}, approach_explanations: {}, popularity_score: .9,
};

describe('ProblemCard', () => {
  it('shows problem metadata and links to the workspace', () => {
    renderWithRouter(<ProblemCard problem={problem} status="solved" bookmarked />);
    expect(screen.getByText('Two Sum')).toBeInTheDocument();
    expect(screen.getByText('Solved')).toBeInTheDocument();
    expect(screen.getByRole('link', { name: /Two Sum/i })).toHaveAttribute('href', '/app/problem/1');
  });
});
