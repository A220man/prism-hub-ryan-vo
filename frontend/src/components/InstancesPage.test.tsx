import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';

vi.mock('../api/instances', () => ({
  instancesApi: {
    list: vi.fn(),
    create: vi.fn(),
    launch: vi.fn(),
    delete: vi.fn(),
  },
}));

import InstancesPage from './InstancesPage';
import { instancesApi } from '../api/instances';

const renderWithRouter = (component: React.ReactNode) => {
  return render(<BrowserRouter>{component}</BrowserRouter>);
};

describe('InstancesPage', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('renders loading state initially', () => {
    instancesApi.list.mockImplementation(() => new Promise(() => {}));
    renderWithRouter(<InstancesPage />);
    expect(screen.getByText('Loading instances...')).toBeInTheDocument();
  });

  it('renders empty state when no instances', async () => {
    instancesApi.list.mockResolvedValue({ data: { instances: [], total: 0, page: 1, page_size: 20 } });
    renderWithRouter(<InstancesPage />);
    await waitFor(() => {
      expect(screen.getByText(/Create your first instance/)).toBeInTheDocument();
    });
  });

  it('renders instance cards', async () => {
    const mockInstances = [
      { id: '1', name: 'Test Instance', version: '1.20.1', loader: 'fabric', loader_version: '0.15.11', memory_min: 1024, memory_max: 4096, resolution_width: 854, resolution_height: 480, fullscreen: false, status: 'ready', created_at: new Date().toISOString(), updated_at: new Date().toISOString(), play_time_seconds: 0 },
    ];
    instancesApi.list.mockResolvedValue({ data: { instances: mockInstances, total: 1, page: 1, page_size: 20 } });
    renderWithRouter(<InstancesPage />);
    await waitFor(() => {
      expect(screen.getByText('Test Instance')).toBeInTheDocument();
      expect(screen.getByText('1.20.1')).toBeInTheDocument();
    });
  });

  it('opens create modal on button click', async () => {
    instancesApi.list.mockResolvedValue({ data: { instances: [], total: 0, page: 1, page_size: 20 } });
    renderWithRouter(<InstancesPage />);
    await waitFor(() => {
      expect(screen.getByRole('button', { name: 'Create Instance' })).toBeInTheDocument();
    });
    fireEvent.click(screen.getByRole('button', { name: 'Create Instance' }));
    await waitFor(() => {
      expect(screen.getByRole('heading', { name: 'Create Instance' })).toBeInTheDocument();
    });
  });
});