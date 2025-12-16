// lib/api.ts - Cliente API para el backend
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export interface SystemStats {
  cpu_percent: number;
  ram_total_mb: number;
  ram_used_mb: number;
  ram_percent: number;
  timestamp: number;
}

export interface JobMetrics {
  cpu_percent: number;
  memory_mb: number;
  memory_percent: number;
  timestamp: number;
}

export interface Job {
  job_id: string;
  command: string[];
  status: 'running' | 'completed' | 'failed';
  pid?: number;
  start_time: number;
  end_time?: number;
  exit_code?: number;
  metrics?: JobMetrics;
}

export interface CreateJobRequest {
  command: string[];
  env?: Record<string, string>;
}

class APIClient {
  private baseURL: string;

  constructor(baseURL: string) {
    this.baseURL = baseURL;
  }

  // System Metrics
  async getSystemStats(): Promise<SystemStats> {
    const response = await fetch(`${this.baseURL}/metrics/system`);
    if (!response.ok) throw new Error('Failed to fetch system stats');
    return response.json();
  }

  // Jobs
  async getJobs(): Promise<Job[]> {
    const response = await fetch(`${this.baseURL}/jobs/`);
    if (!response.ok) throw new Error('Failed to fetch jobs');
    const data = await response.json();
    // El backend devuelve { total: number, jobs: Job[] }
    return data.jobs || [];
  }

  async getJob(jobId: string): Promise<Job> {
    const response = await fetch(`${this.baseURL}/jobs/${jobId}`);
    if (!response.ok) throw new Error('Failed to fetch job');
    return response.json();
  }

  async createJob(data: CreateJobRequest): Promise<Job> {
    const response = await fetch(`${this.baseURL}/jobs/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
    if (!response.ok) throw new Error('Failed to create job');
    return response.json();
  }

  async killJob(jobId: string): Promise<{ message: string }> {
    const response = await fetch(`${this.baseURL}/jobs/${jobId}/kill`, {
      method: 'POST',
    });
    if (!response.ok) throw new Error('Failed to kill job');
    return response.json();
  }

  async getJobLogs(jobId: string, lines?: number): Promise<{ job_id: string; logs: string[] }> {
    const url = new URL(`${this.baseURL}/logs/${jobId}`);
    if (lines) url.searchParams.append('lines', lines.toString());
    
    const response = await fetch(url.toString());
    if (!response.ok) throw new Error('Failed to fetch logs');
    return response.json();
  }

  async getJobMetrics(jobId: string): Promise<JobMetrics[]> {
    const response = await fetch(`${this.baseURL}/metrics/job/${jobId}`);
    if (!response.ok) throw new Error('Failed to fetch job metrics');
    return response.json();
  }

  // Health check
  async healthCheck(): Promise<{ status: string; system: SystemStats }> {
    const response = await fetch(`${this.baseURL}/health`);
    if (!response.ok) throw new Error('Failed to fetch health');
    return response.json();
  }
}

export const apiClient = new APIClient(API_BASE_URL);
