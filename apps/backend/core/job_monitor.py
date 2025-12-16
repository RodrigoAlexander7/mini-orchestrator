import threading
import time
from typing import Dict, Optional
import psutil  # get a process and stadistics (from operative system to script)
from core.process_manager import ProcessManager

class JobMonitorManager:
   def __init__(self, process_manager: ProcessManager, interval: float = 1.0):
      self.pm = process_manager
      self.interval = interval
      self.stats:Dict[int, Dict] = {} #[PID, stats{}]
      self.running = True
      self.monitors:Dict[int, threading.Thread] = {}
      self.lock = threading.Lock()  # all the threads of the instance are loked
                                    # |-> so just one thread can acces one resource at the time

   def start_monitoring(self, pid:int):
      if pid in self.monitors:
         return   # is already monitorized
      
      # Crear y arrancar el thread de monitoreo
      thread = threading.Thread(target=self._monitor_job, args=(pid,), daemon=True)
      
      with self.lock:
         self.monitors[pid] = thread
      
      thread.start()
      
   def stop_monitoring(self, pid:int):
      if pid in self.stats:
         with self.lock: # ensure that we can acces the thread
            del self.stats[pid]
      if pid in self.monitors:
         with self.lock:
            del self.monitors[pid]


   def _monitor_job(self, pid:int):
      try:
         p = psutil.Process(pid)
      except psutil.NoSuchProcess:
         return

      while self.running:
         try:
            cpu = p.cpu_percent(interval=None) # none -> no wait for any second (interval)
            ram = p.memory_info().rss / (1024 * 1024) # from bytes to Mbytes
            status = p.status()

            with self.lock:  # access resource if the resource is free and not used by other????
               self.stats[pid] = {
                  "cpu":cpu,
                  "ram": ram,
                  "status": status,
                  "timestamp": time.time() # return the time (Actually return the time since unix 1970 in seconds)

               }
            if status in ("zombie", "dead", "stopped"):
               break

            time.sleep(self.interval) #??
         except psutil.NoSuchProcess:
            break
      # when no runing
      self.stop_monitoring(pid)

   def get_stats(self, pid: int) -> Optional[Dict]:
      return self.stats.get(pid)

   def get_all_stats(self) -> Dict[int, Dict]:
      return self.stats
   
   def shutdown(self):
      self.running = False