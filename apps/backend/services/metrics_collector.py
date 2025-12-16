"""
Recolector de métricas del sistema y procesos
"""
import psutil
import time
from typing import Dict, List, Optional
from datetime import datetime, timedelta


class MetricsCollector:
    """Colecta y almacena métricas históricas del sistema"""
    
    def __init__(self, history_size: int = 1000):
        """
        Args:
            history_size: Número máximo de puntos históricos a mantener
        """
        self.history_size = history_size
        self.system_history: List[Dict] = []
        self.process_history: Dict[int, List[Dict]] = {}
    
    def collect_system_metrics(self) -> Dict:
        """
        Recolecta métricas generales del sistema
        
        Returns:
            Diccionario con métricas del sistema
        """
        cpu_percent = psutil.cpu_percent(interval=0.1)
        cpu_count = psutil.cpu_count()
        
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        net_io = psutil.net_io_counters()
        
        metrics = {
            "timestamp": time.time(),
            "datetime": datetime.now().isoformat(),
            "cpu": {
                "percent": cpu_percent,
                "count": cpu_count,
                "per_cpu": psutil.cpu_percent(percpu=True)
            },
            "memory": {
                "total_mb": memory.total / (1024 * 1024),
                "available_mb": memory.available / (1024 * 1024),
                "used_mb": memory.used / (1024 * 1024),
                "percent": memory.percent
            },
            "disk": {
                "total_gb": disk.total / (1024 ** 3),
                "used_gb": disk.used / (1024 ** 3),
                "free_gb": disk.free / (1024 ** 3),
                "percent": disk.percent
            },
            "network": {
                "bytes_sent": net_io.bytes_sent,
                "bytes_recv": net_io.bytes_recv,
                "packets_sent": net_io.packets_sent,
                "packets_recv": net_io.packets_recv
            }
        }
        
        # Guardar en historial
        self.system_history.append(metrics)
        if len(self.system_history) > self.history_size:
            self.system_history.pop(0)
        
        return metrics
    
    def collect_process_metrics(self, pid: int) -> Optional[Dict]:
        """
        Recolecta métricas de un proceso específico
        
        Args:
            pid: Process ID
            
        Returns:
            Diccionario con métricas del proceso o None si no existe
        """
        try:
            process = psutil.Process(pid)
            
            # Información básica
            with process.oneshot():
                cpu_percent = process.cpu_percent(interval=0.1)
                memory_info = process.memory_info()
                
                metrics = {
                    "timestamp": time.time(),
                    "datetime": datetime.now().isoformat(),
                    "pid": pid,
                    "name": process.name(),
                    "status": process.status(),
                    "cpu_percent": cpu_percent,
                    "memory": {
                        "rss_mb": memory_info.rss / (1024 * 1024),
                        "vms_mb": memory_info.vms / (1024 * 1024)
                    },
                    "num_threads": process.num_threads(),
                    "create_time": process.create_time()
                }
                
                # Intentar obtener IO (puede fallar en algunos sistemas)
                try:
                    io_counters = process.io_counters()
                    metrics["io"] = {
                        "read_bytes": io_counters.read_bytes,
                        "write_bytes": io_counters.write_bytes
                    }
                except (psutil.AccessDenied, AttributeError):
                    metrics["io"] = None
            
            # Guardar en historial del proceso
            if pid not in self.process_history:
                self.process_history[pid] = []
            
            self.process_history[pid].append(metrics)
            if len(self.process_history[pid]) > self.history_size:
                self.process_history[pid].pop(0)
            
            return metrics
            
        except psutil.NoSuchProcess:
            return None
        except psutil.AccessDenied:
            return {"error": "Access denied to process"}
    
    def get_system_history(self, minutes: int = 5) -> List[Dict]:
        """
        Obtiene historial de métricas del sistema
        
        Args:
            minutes: Minutos de historial a retornar
            
        Returns:
            Lista de métricas históricas
        """
        cutoff_time = time.time() - (minutes * 60)
        return [m for m in self.system_history if m["timestamp"] >= cutoff_time]
    
    def get_process_history(self, pid: int, minutes: int = 5) -> List[Dict]:
        """
        Obtiene historial de métricas de un proceso
        
        Args:
            pid: Process ID
            minutes: Minutos de historial a retornar
            
        Returns:
            Lista de métricas históricas del proceso
        """
        if pid not in self.process_history:
            return []
        
        cutoff_time = time.time() - (minutes * 60)
        return [m for m in self.process_history[pid] if m["timestamp"] >= cutoff_time]
    
    def cleanup_process_history(self, pid: int):
        """Elimina el historial de un proceso terminado"""
        if pid in self.process_history:
            del self.process_history[pid]


# Instancia global
metrics_collector = MetricsCollector()
