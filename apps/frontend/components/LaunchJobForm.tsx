'use client';

import { useState } from 'react';
import { launchJob } from '@/lib/api';

interface LaunchJobFormProps {
  onJobLaunched: () => void;
}

export default function LaunchJobForm({ onJobLaunched }: LaunchJobFormProps) {
  const [command, setCommand] = useState('');
  const [isLaunching, setIsLaunching] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setSuccess(null);

    if (!command.trim()) {
      setError('Command cannot be empty');
      return;
    }

    // Parse command into array (simple split by spaces, could be improved)
    const commandArray = command.trim().split(/\s+/);

    setIsLaunching(true);

    try {
      const result = await launchJob(commandArray);
      setSuccess(`✅ Job launched: ${result.job_id}`);
      setCommand('');
      setTimeout(() => setSuccess(null), 3000);
      onJobLaunched();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to launch job');
    } finally {
      setIsLaunching(false);
    }
  };

  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
      <h2 className="text-xl font-bold mb-4 text-gray-800 dark:text-white">🚀 Launch New Job</h2>
      
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label htmlFor="command" className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
            Command
          </label>
          <input
            id="command"
            type="text"
            value={command}
            onChange={(e) => setCommand(e.target.value)}
            placeholder="e.g., python script.py or sleep 60"
            className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-md 
                     bg-white dark:bg-gray-700 text-gray-900 dark:text-white
                     focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            disabled={isLaunching}
          />
          <p className="mt-1 text-xs text-gray-500 dark:text-gray-400">
            Enter the command and arguments separated by spaces
          </p>
        </div>

        {error && (
          <div className="p-3 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-md">
            <p className="text-sm text-red-600 dark:text-red-400">❌ {error}</p>
          </div>
        )}

        {success && (
          <div className="p-3 bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-800 rounded-md">
            <p className="text-sm text-green-600 dark:text-green-400">{success}</p>
          </div>
        )}

        <button
          type="submit"
          disabled={isLaunching || !command.trim()}
          className="w-full px-4 py-2 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 
                   text-white font-medium rounded-md transition-colors
                   focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
        >
          {isLaunching ? 'Launching...' : 'Launch Job'}
        </button>
      </form>

      <div className="mt-4 p-3 bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-md">
        <p className="text-xs text-blue-800 dark:text-blue-300 font-medium mb-1">💡 Example commands:</p>
        <ul className="text-xs text-blue-700 dark:text-blue-400 space-y-1">
          <li>• <code className="bg-blue-100 dark:bg-blue-900 px-1 rounded">sleep 30</code> - Sleep for 30 seconds</li>
          <li>• <code className="bg-blue-100 dark:bg-blue-900 px-1 rounded">python3 -c "import time; time.sleep(60)"</code> - Python sleep</li>
          <li>• <code className="bg-blue-100 dark:bg-blue-900 px-1 rounded">ping -c 10 google.com</code> - Ping 10 times</li>
        </ul>
      </div>
    </div>
  );
}
