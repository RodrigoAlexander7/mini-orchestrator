// components/SystemStats.tsx
'use client';

import { SystemStats as SystemStatsType } from '@/lib/api';

interface Props {
  stats: SystemStatsType | null;
  isConnected: boolean;
}

export default function SystemStats({ stats, isConnected }: Props) {
  if (!stats) {
    return (
      <div className="rounded-lg border border-gray-200 bg-white p-6 shadow-sm dark:border-gray-800 dark:bg-gray-900">
        <h2 className="text-lg font-semibold text-gray-900 dark:text-gray-100">
          System Metrics
        </h2>
        <p className="mt-4 text-gray-500 dark:text-gray-400">Loading...</p>
      </div>
    );
  }

  const cpuColor = stats.cpu_percent > 80 ? 'text-red-600' : stats.cpu_percent > 50 ? 'text-yellow-600' : 'text-green-600';
  const ramColor = stats.ram_percent > 80 ? 'text-red-600' : stats.ram_percent > 50 ? 'text-yellow-600' : 'text-green-600';

  return (
    <div className="rounded-lg border border-gray-200 bg-white p-6 shadow-sm dark:border-gray-800 dark:bg-gray-900">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-lg font-semibold text-gray-900 dark:text-gray-100">
          System Metrics
        </h2>
        <div className="flex items-center gap-2">
          <div className={`h-2 w-2 rounded-full ${isConnected ? 'bg-green-500' : 'bg-red-500'}`} />
          <span className="text-sm text-gray-500 dark:text-gray-400">
            {isConnected ? 'Connected' : 'Disconnected'}
          </span>
        </div>
      </div>

      <div className="grid grid-cols-1 gap-4 md:grid-cols-2">
        {/* CPU */}
        <div className="rounded-lg border border-gray-100 bg-gray-50 p-4 dark:border-gray-800 dark:bg-gray-800">
          <div className="flex items-center justify-between mb-2">
            <span className="text-sm font-medium text-gray-600 dark:text-gray-400">CPU Usage</span>
            <span className={`text-2xl font-bold ${cpuColor}`}>
              {stats.cpu_percent.toFixed(1)}%
            </span>
          </div>
          <div className="h-2 overflow-hidden rounded-full bg-gray-200 dark:bg-gray-700">
            <div
              className={`h-full transition-all duration-300 ${
                stats.cpu_percent > 80 ? 'bg-red-500' : stats.cpu_percent > 50 ? 'bg-yellow-500' : 'bg-green-500'
              }`}
              style={{ width: `${Math.min(stats.cpu_percent, 100)}%` }}
            />
          </div>
        </div>

        {/* RAM */}
        <div className="rounded-lg border border-gray-100 bg-gray-50 p-4 dark:border-gray-800 dark:bg-gray-800">
          <div className="flex items-center justify-between mb-2">
            <span className="text-sm font-medium text-gray-600 dark:text-gray-400">RAM Usage</span>
            <span className={`text-2xl font-bold ${ramColor}`}>
              {stats.ram_percent.toFixed(1)}%
            </span>
          </div>
          <div className="h-2 overflow-hidden rounded-full bg-gray-200 dark:bg-gray-700">
            <div
              className={`h-full transition-all duration-300 ${
                stats.ram_percent > 80 ? 'bg-red-500' : stats.ram_percent > 50 ? 'bg-yellow-500' : 'bg-green-500'
              }`}
              style={{ width: `${Math.min(stats.ram_percent, 100)}%` }}
            />
          </div>
          <p className="mt-2 text-xs text-gray-500 dark:text-gray-400">
            {(stats.ram_used_mb / 1024).toFixed(1)} GB / {(stats.ram_total_mb / 1024).toFixed(1)} GB
          </p>
        </div>
      </div>
    </div>
  );
}
