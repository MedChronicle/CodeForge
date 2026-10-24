import { render } from '@testing-library/react';
import type { ReactElement } from 'react';
import { BrowserRouter } from 'react-router-dom';

export function renderWithRouter(element: ReactElement) {
  return render(<BrowserRouter>{element}</BrowserRouter>);
}
