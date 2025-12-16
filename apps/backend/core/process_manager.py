import subprocess # set a process (from script to Operative System)
from typing import Dict, Optional

class ProcessManager:
   def __init__(self):
      self.jobs: Dict[int, subprocess.Popen] = {}

   def start_job(self, command:list) -> int:
      process = subprocess.Popen(
         command,
         stdin=subprocess.PIPE,   # be able to sent data
         stdout=subprocess.PIPE,  # to read the output
         stderr=subprocess.PIPE, # to see errors
         text = True
      )
      pid = process.pid
      self.jobs[pid]=process
      return pid
   
   def stop_job(self, pid:int) -> bool:
      """
      Determine if the process exist, return true if the process is stoped
      """
      process = self.jobs[pid]
      if not process:
         return False
      process.terminate()
      
      try:
         process.wait(timeout=5)
      except subprocess.TimeoutExpired:
         # force kill
         process.kill()   

      del self.jobs[pid]
      return True
   

   def get_job(self, pid:int) -> Optional[subprocess.Popen]:
      return self.jobs[pid]

   def list_jobs(self) -> Dict[int, subprocess.Popen]:
      return self.jobs
