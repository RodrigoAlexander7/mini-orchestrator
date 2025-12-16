"""
Sistema de logging por job
"""
import logging
import os
from datetime import datetime
from pathlib import Path
from typing import Optional
from config import settings


class JobLogger:
    """Manejador de logs individuales por job"""
    
    def __init__(self, log_dir: str = ""):
        self.log_dir = Path(log_dir or settings.log_dir)
        self.log_dir.mkdir(exist_ok=True, parents=True)
        self.loggers = {}
    
    def get_logger(self, job_id: str) -> logging.Logger:
        """
        Obtiene o crea un logger para un job específico
        
        Args:
            job_id: ID del job
            
        Returns:
            Logger configurado para el job
        """
        if job_id in self.loggers:
            return self.loggers[job_id]
        
        # Crear logger
        logger = logging.getLogger(f"job.{job_id}")
        logger.setLevel(logging.DEBUG)
        
        # Evitar duplicados
        if logger.handlers:
            return logger
        
        # Archivo de log para este job
        log_file = self.log_dir / f"{job_id}.log"
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        
        # Formato
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(formatter)
        
        logger.addHandler(file_handler)
        self.loggers[job_id] = logger
        
        return logger
    
    def log_job_start(self, job_id: str, command: list, pid: int):
        """Registra el inicio de un job"""
        logger = self.get_logger(job_id)
        logger.info(f"Job iniciado - PID: {pid} - Comando: {' '.join(command)}")
    
    def log_job_end(self, job_id: str, pid: int, exit_code: Optional[int] = None):
        """Registra la finalización de un job"""
        logger = self.get_logger(job_id)
        logger.info(f"Job finalizado - PID: {pid} - Exit Code: {exit_code}")
    
    def log_job_error(self, job_id: str, error: str):
        """Registra un error del job"""
        logger = self.get_logger(job_id)
        logger.error(f"Error: {error}")
    
    def get_job_logs(self, job_id: str, lines: int = 100) -> list:
        """
        Lee las últimas N líneas del log de un job
        
        Args:
            job_id: ID del job
            lines: Número de líneas a leer (por defecto 100)
            
        Returns:
            Lista de líneas del log
        """
        log_file = self.log_dir / f"{job_id}.log"
        
        if not log_file.exists():
            return []
        
        try:
            with open(log_file, 'r', encoding='utf-8') as f:
                all_lines = f.readlines()
                return all_lines[-lines:] if len(all_lines) > lines else all_lines
        except Exception as e:
            return [f"Error leyendo logs: {str(e)}"]
    
    def cleanup_old_logs(self, days: int = 0):
        """
        Elimina logs antiguos
        
        Args:
            days: Días de retención (por defecto desde config)
        """
        retention_days = days or settings.log_retention_days
        cutoff_time = datetime.now().timestamp() - (retention_days * 86400)
        
        for log_file in self.log_dir.glob("*.log"):
            if log_file.stat().st_mtime < cutoff_time:
                try:
                    log_file.unlink()
                except Exception as e:
                    logging.error(f"Error eliminando log {log_file}: {e}")


# Instancia global
job_logger = JobLogger()
