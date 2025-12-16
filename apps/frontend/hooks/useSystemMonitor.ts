// hooks/useSystemMonitor.ts
'use client';

import { useEffect, useState } from 'react';
import { apiClient, SystemStats, Job } from '@/lib/api';

export function useSystemMonitor(refreshInterval: number = 2000) {
  const [systemStats, setSystemStats] = useState<SystemStats | null>(null);
  const [jobs, setJobs] = useState<Job[]>([]);
  const [isConnected, setIsConnected] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let isMounted = true;

    const fetchData = async () => {
      try {
        const [stats, jobsList] = await Promise.all([
          apiClient.getSystemStats(),
          apiClient.getJobs(),
        ]);

        if (isMounted) {
          setSystemStats(stats);
          setJobs(jobsList);
          setIsConnected(true);
          setError(null);
        }
      } catch (err) {
        if (isMounted) {
          setIsConnected(false);
          setError(err instanceof Error ? err.message : 'Unknown error');
        }
      }
    };

    fetchData();
    const interval = setInterval(fetchData, refreshInterval);

    return () => {
      isMounted = false;
      clearInterval(interval);
    };
  }, [refreshInterval]);

  return { systemStats, jobs, isConnected, error };
}
