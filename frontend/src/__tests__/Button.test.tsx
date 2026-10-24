import { fireEvent, screen } from '@testing-library/react';
import { Button } from '../components/ui/Button';
import { renderWithRouter } from '../test/test-utils';

describe('Button', () => {
  it('renders its label and responds to clicks', () => {
    const onClick = vi.fn();
    renderWithRouter(<Button onClick={onClick}>Forge</Button>);
    fireEvent.click(screen.getByRole('button', { name: 'Forge' }));
    expect(onClick).toHaveBeenCalledTimes(1);
  });

  it('disables itself while loading', () => {
    renderWithRouter(<Button loading>Saving</Button>);
    expect(screen.getByRole('button', { name: /saving/i })).toBeDisabled();
  });
});
