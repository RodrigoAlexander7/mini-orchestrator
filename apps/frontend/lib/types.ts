/**
 * TypeScript types for the application
 */

export interface SystemMetrics {
  cpu_percent: number;
  ram_total_mb: number;
  ram_used_mb: number;
  ram_percent: number;
  timestamp: number;
}

export interface Job {
  job_id: string;
  command: string[];
  status: 'pending' | 'running' | 'completed' | 'failed' | 'stopped';
  pid: number | null;
  exit_code: number | null;
  created_at: number;
  started_at: number | null;
  finished_at: number | null;
}

export interface JobMetrics {
  job_id: string;
  pid: number;
  cpu_percent: number;
  memory_mb: number;
  memory_percent: number;
  status: string;
}

export interface JobLogs {
  job_id: string;
  logs: string[];
  total_lines: number;
}
