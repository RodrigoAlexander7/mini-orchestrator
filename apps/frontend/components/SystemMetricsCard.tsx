'use client';

import { useEffect, useState } from 'react';
import { getSystemMetrics } from '@/lib/api';
import type { SystemMetrics } from '@/lib/types';

export default function SystemMetricsCard() {
  const [metrics, setMetrics] = useState<SystemMetrics | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const fetchMetrics = async () => {
      try {
        const data = await getSystemMetrics();
        setMetrics(data);
        setError(null);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to fetch metrics');
      } finally {
        setIsLoading(false);
      }
    };

    fetchMetrics();
    const interval = setInterval(fetchMetrics, 2000); // Update every 2 seconds

    return () => clearInterval(interval);
  }, []);

  if (isLoading) {
    return (
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
        <h2 className="text-xl font-bold mb-4 text-gray-800 dark:text-white">System Metrics</h2>
        <div className="animate-pulse space-y-4">
          <div className="h-4 bg-gray-200 dark:bg-gray-700 rounded w-3/4"></div>
          <div className="h-4 bg-gray-200 dark:bg-gray-700 rounded w-1/2"></div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
        <h2 className="text-xl font-bold mb-4 text-gray-800 dark:text-white">System Metrics</h2>
        <div className="text-red-500 dark:text-red-400">
          <p>❌ Error: {error}</p>
          <p className="text-sm mt-2">Make sure the backend is running on port 8000</p>
        </div>
      </div>
    );
  }

  if (!metrics) return null;

  const cpuColor = metrics.cpu_percent > 80 ? 'text-red-600' : metrics.cpu_percent > 50 ? 'text-yellow-600' : 'text-green-600';
  const ramColor = metrics.ram_percent > 80 ? 'text-red-600' : metrics.ram_percent > 50 ? 'text-yellow-600' : 'text-green-600';

  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
      <h2 className="text-xl font-bold mb-4 text-gray-800 dark:text-white flex items-center gap-2">
        📊 System Metrics
        <span className="text-xs font-normal text-gray-500">
          (Updated every 2s)
        </span>
      </h2>
      
      <div className="space-y-4">
        {/* CPU Usage */}
        <div>
          <div className="flex justify-between items-center mb-2">
            <span className="text-sm font-medium text-gray-700 dark:text-gray-300">CPU Usage</span>
            <span className={`text-sm font-bold ${cpuColor}`}>
              {metrics.cpu_percent.toFixed(1)}%
            </span>
          </div>
          <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2.5">
            <div
              className={`h-2.5 rounded-full transition-all duration-300 ${
                metrics.cpu_percent > 80 ? 'bg-red-600' : 
                metrics.cpu_percent > 50 ? 'bg-yellow-500' : 'bg-green-500'
              }`}
              style={{ width: `${Math.min(metrics.cpu_percent, 100)}%` }}
            ></div>
          </div>
        </div>

        {/* RAM Usage */}
        <div>
          <div className="flex justify-between items-center mb-2">
            <span className="text-sm font-medium text-gray-700 dark:text-gray-300">RAM Usage</span>
            <span className={`text-sm font-bold ${ramColor}`}>
              {metrics.ram_percent.toFixed(1)}% 
              <span className="text-xs font-normal text-gray-500 ml-1">
                ({(metrics.ram_used_mb / 1024).toFixed(1)} / {(metrics.ram_total_mb / 1024).toFixed(1)} GB)
              </span>
            </span>
          </div>
          <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2.5">
            <div
              className={`h-2.5 rounded-full transition-all duration-300 ${
                metrics.ram_percent > 80 ? 'bg-red-600' : 
                metrics.ram_percent > 50 ? 'bg-yellow-500' : 'bg-green-500'
              }`}
              style={{ width: `${Math.min(metrics.ram_percent, 100)}%` }}
            ></div>
          </div>
        </div>

        {/* Timestamp */}
        <div className="text-xs text-gray-500 dark:text-gray-400 text-right">
          Last update: {new Date(metrics.timestamp * 1000).toLocaleTimeString()}
        </div>
      </div>
    </div>
  );
}
