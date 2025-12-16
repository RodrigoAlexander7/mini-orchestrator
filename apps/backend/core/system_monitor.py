import threading
import time
from typing import Dict, Optional
import psutil  # get a process and stadistics (from operative system to script)
from core.process_manager import ProcessManager

class SystemMonitor:
   def get_system_stats(self) -> Dict:
      """
      Retun:
      - CPU total (%)
      - RAM total / usage / porcent %
      """
      ram = psutil.virtual_memory()

      return {
         "cpu_percent": psutil.cpu_percent(),
         "ram_total_mb": ram.total / (1024 * 1024),
         "ram_used_mb": ram.used / (1024 * 1024),
         "ram_percent": ram.percent,
         "timestamp": time.time(),
      }