import axios from 'axios';
import type { Instance, InstanceListResponse, InstanceCreate, InstanceUpdate } from '../types/api';

const api = axios.create({
  baseURL: '/api/v1',
  headers: {
    'Content-Type': 'application/json',
  },
});

export const instancesApi = {
  list: (params?: { page?: number; page_size?: number; status?: string }) =>
    api.get<InstanceListResponse>('/instances', { params }),

  get: (id: string) =>
    api.get<Instance>(`/instances/${id}`),

  create: (data: InstanceCreate) =>
    api.post<Instance>('/instances', data),

  update: (id: string, data: InstanceUpdate) =>
    api.patch<Instance>(`/instances/${id}`, data),

  delete: (id: string) =>
    api.delete(`/instances/${id}`),

  launch: (id: string) =>
    api.post<Instance>(`/instances/${id}/launch`),
};

export default api;