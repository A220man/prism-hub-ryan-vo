import '@testing-library/jest-dom'
import { vi, expect } from 'vitest'

// Set global expect for jest-dom
globalThis.expect = expect

vi.mock('react-router-dom', async () => {
  const actual = await vi.importActual('react-router-dom');
  return {
    ...actual,
    useNavigate: () => vi.fn(),
    useParams: () => ({}),
  };
})