// components/JobCard.tsx
'use client';

import { useState } from 'react';
import { Job, apiClient } from '@/lib/api';

interface Props {
  job: Job;
  onUpdate: () => void;
}

export default function JobCard({ job, onUpdate }: Props) {
  const [isExpanded, setIsExpanded] = useState(false);
  const [logs, setLogs] = useState<string[]>([]);
  const [isLoadingLogs, setIsLoadingLogs] = useState(false);
  const [isKilling, setIsKilling] = useState(false);

  const statusColor = {
    running: 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200',
    completed: 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200',
    failed: 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200',
  };

  const handleLoadLogs = async () => {
    if (logs.length > 0) {
      setIsExpanded(!isExpanded);
      return;
    }

    setIsLoadingLogs(true);
    try {
      const response = await apiClient.getJobLogs(job.job_id, 50);
      setLogs(response.logs);
      setIsExpanded(true);
    } catch (error) {
      console.error('Failed to load logs:', error);
    } finally {
      setIsLoadingLogs(false);
    }
  };

  const handleKillJob = async () => {
    if (!confirm(`Are you sure you want to kill job ${job.job_id}?`)) return;

    setIsKilling(true);
    try {
      await apiClient.killJob(job.job_id);
      onUpdate();
    } catch (error) {
      console.error('Failed to kill job:', error);
      alert('Failed to kill job');
    } finally {
      setIsKilling(false);
    }
  };

  const formatTime = (timestamp: number) => {
    return new Date(timestamp * 1000).toLocaleString();
  };

  const getRuntime = () => {
    if (!job.start_time) return 'N/A';
    const endTime = job.end_time || Date.now() / 1000;
    const runtime = endTime - job.start_time;
    return `${Math.floor(runtime)}s`;
  };

  return (
    <div className="rounded-lg border border-gray-200 bg-gray-50 p-4 dark:border-gray-700 dark:bg-gray-800">
      <div className="flex items-start justify-between">
        <div className="flex-1">
          <div className="flex items-center gap-3">
            <span className={`rounded-full px-2 py-1 text-xs font-medium ${statusColor[job.status]}`}>
              {job.status}
            </span>
            <code className="text-xs text-gray-600 dark:text-gray-400">
              {job.job_id}
            </code>
            {job.pid && (
              <span className="text-xs text-gray-500 dark:text-gray-500">
                PID: {job.pid}
              </span>
            )}
          </div>

          <div className="mt-2">
            <code className="text-sm font-medium text-gray-900 dark:text-gray-100">
              {job.command.join(' ')}
            </code>
          </div>

          <div className="mt-2 flex flex-wrap gap-4 text-xs text-gray-500 dark:text-gray-400">
            <span>Started: {formatTime(job.start_time)}</span>
            <span>Runtime: {getRuntime()}</span>
            {job.exit_code !== undefined && (
              <span>Exit Code: {job.exit_code}</span>
            )}
            {job.metrics && (
              <>
                <span>CPU: {job.metrics.cpu_percent.toFixed(1)}%</span>
                <span>RAM: {job.metrics.memory_mb.toFixed(0)} MB</span>
              </>
            )}
          </div>
        </div>

        <div className="flex gap-2">
          <button
            onClick={handleLoadLogs}
            disabled={isLoadingLogs}
            className="rounded bg-gray-200 px-3 py-1 text-xs font-medium text-gray-700 transition-colors hover:bg-gray-300 dark:bg-gray-700 dark:text-gray-300 dark:hover:bg-gray-600"
          >
            {isLoadingLogs ? '...' : isExpanded ? '▲ Logs' : '▼ Logs'}
          </button>
          {job.status === 'running' && (
            <button
              onClick={handleKillJob}
              disabled={isKilling}
              className="rounded bg-red-100 px-3 py-1 text-xs font-medium text-red-700 transition-colors hover:bg-red-200 dark:bg-red-900 dark:text-red-200 dark:hover:bg-red-800"
            >
              {isKilling ? '...' : 'Kill'}
            </button>
          )}
        </div>
      </div>

      {isExpanded && logs.length > 0 && (
        <div className="mt-4 rounded-lg bg-black p-4 text-xs">
          <pre className="overflow-x-auto text-green-400">
            {logs.map((line, i) => (
              <div key={i}>{line || ' '}</div>
            ))}
          </pre>
        </div>
      )}
    </div>
  );
}
