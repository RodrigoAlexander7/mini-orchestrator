// components/JobsList.tsx
'use client';

import { useState } from 'react';
import { Job } from '@/lib/api';
import JobCard from './JobCard';
import CreateJobModal from './CreateJobModal';

interface Props {
  jobs: Job[];
  onRefresh: () => void;
}

export default function JobsList({ jobs, onRefresh }: Props) {
  const [isCreateModalOpen, setIsCreateModalOpen] = useState(false);

  const runningJobs = jobs.filter((j) => j.status === 'running');
  const completedJobs = jobs.filter((j) => j.status === 'completed');
  const failedJobs = jobs.filter((j) => j.status === 'failed');

  return (
    <div className="rounded-lg border border-gray-200 bg-white p-6 shadow-sm dark:border-gray-800 dark:bg-gray-900">
      <div className="mb-6 flex items-center justify-between">
        <div>
          <h2 className="text-lg font-semibold text-gray-900 dark:text-gray-100">
            Jobs Management
          </h2>
          <div className="mt-2 flex gap-4 text-sm">
            <span className="text-green-600 dark:text-green-400">
              ▶ Running: {runningJobs.length}
            </span>
            <span className="text-blue-600 dark:text-blue-400">
              ✓ Completed: {completedJobs.length}
            </span>
            <span className="text-red-600 dark:text-red-400">
              ✗ Failed: {failedJobs.length}
            </span>
          </div>
        </div>
        <button
          onClick={() => setIsCreateModalOpen(true)}
          className="rounded-lg bg-blue-600 px-4 py-2 text-sm font-medium text-white transition-colors hover:bg-blue-700"
        >
          + New Job
        </button>
      </div>

      {jobs.length === 0 ? (
        <div className="py-12 text-center text-gray-500 dark:text-gray-400">
          No jobs found. Create your first job!
        </div>
      ) : (
        <div className="space-y-3">
          {jobs.map((job) => (
            <JobCard key={job.job_id} job={job} onUpdate={onRefresh} />
          ))}
        </div>
      )}

      <CreateJobModal
        isOpen={isCreateModalOpen}
        onClose={() => setIsCreateModalOpen(false)}
        onSuccess={() => {
          setIsCreateModalOpen(false);
          onRefresh();
        }}
      />
    </div>
  );
}
