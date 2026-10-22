export interface Instance {
  id: string;
  name: string;
  version: string;
  loader?: string;
  loader_version?: string;
  java_version?: string;
  memory_min: number;
  memory_max: number;
  game_dir?: string;
  resolution_width: number;
  resolution_height: number;
  fullscreen: boolean;
  status: 'created' | 'downloading' | 'ready' | 'launching' | 'running' | 'error';
  created_at: string;
  updated_at: string;
  last_played?: string;
  play_time_seconds: number;
}

export interface InstanceListResponse {
  instances: Instance[];
  total: number;
  page: number;
  page_size: number;
}

export interface InstanceCreate {
  name: string;
  version: string;
  loader?: string;
  loader_version?: string;
  java_version?: string;
  memory_min?: number;
  memory_max?: number;
  game_dir?: string;
  resolution_width?: number;
  resolution_height?: number;
  fullscreen?: boolean;
}

export interface InstanceUpdate {
  name?: string;
  version?: string;
  loader?: string;
  loader_version?: string;
  java_version?: string;
  memory_min?: number;
  memory_max?: number;
  game_dir?: string;
  resolution_width?: number;
  resolution_height?: number;
  fullscreen?: boolean;
}