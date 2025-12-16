'use client';

import { useSystemMonitor } from '@/hooks/useSystemMonitor';
import SystemStats from '@/components/SystemStats';
import JobsList from '@/components/JobsList';
import { useState } from 'react';

export default function Home() {
  const [refreshKey, setRefreshKey] = useState(0);
  const { systemStats, jobs, isConnected, error } = useSystemMonitor(2000);

  const handleRefresh = () => {
    setRefreshKey((prev) => prev + 1);
  };

  return (
    <div className="min-h-screen bg-gray-100 dark:bg-gray-950">
      {/* Header */}
      <header className="border-b border-gray-200 bg-white shadow-sm dark:border-gray-800 dark:bg-gray-900">
        <div className="mx-auto max-w-7xl px-4 py-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-2xl font-bold text-gray-900 dark:text-gray-100">
                Mini Orchestrator
              </h1>
              <p className="mt-1 text-sm text-gray-500 dark:text-gray-400">
                System & Process Monitor
              </p>
            </div>
            <div className="flex items-center gap-4">
              {error && (
                <div className="rounded-lg bg-red-50 px-4 py-2 text-sm text-red-800 dark:bg-red-900/20 dark:text-red-200">
                  ⚠ {error}
                </div>
              )}
              <button
                onClick={handleRefresh}
                className="rounded-lg bg-blue-600 px-4 py-2 text-sm font-medium text-white transition-colors hover:bg-blue-700"
              >
                🔄 Refresh
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8">
        <div className="space-y-6">
          {/* System Stats */}
          <SystemStats stats={systemStats} isConnected={isConnected} />

          {/* Jobs List */}
          <JobsList jobs={jobs} onRefresh={handleRefresh} />
        </div>
      </main>

      {/* Footer */}
      <footer className="mt-12 border-t border-gray-200 bg-white py-6 dark:border-gray-800 dark:bg-gray-900">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <p className="text-center text-sm text-gray-500 dark:text-gray-400">
            Mini Orchestrator - Built with FastAPI & Next.js
          </p>
        </div>
      </footer>
    </div>
  );
}
