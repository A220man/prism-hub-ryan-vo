import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import App from '../App';

describe('App', () => {
  it('renders navbar with brand', () => {
    render(<BrowserRouter><App /></BrowserRouter>);
    expect(screen.getByText('Prism Hub')).toBeInTheDocument();
  });

  it('renders navigation links', () => {
    render(<BrowserRouter><App /></BrowserRouter>);
    expect(screen.getByText('Instances')).toBeInTheDocument();
    expect(screen.getByText('Settings')).toBeInTheDocument();
  });
});