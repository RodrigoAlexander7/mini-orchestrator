"""
Router para métricas del sistema
"""
from fastapi import APIRouter, Query
from pydantic import BaseModel
from typing import List, Dict, Optional

from services.metrics_collector import metrics_collector
from core.system_monitor import SystemMonitor


router = APIRouter(prefix="/metrics", tags=["metrics"])

# Se inyectará desde main.py
system_monitor: Optional[SystemMonitor] = None


class SystemMetrics(BaseModel):
    """Métricas actuales del sistema"""
    cpu_percent: float
    ram_total_mb: float
    ram_used_mb: float
    ram_percent: float
    timestamp: float


class DetailedSystemMetrics(BaseModel):
    """Métricas detalladas del sistema"""
    timestamp: float
    datetime: str
    cpu: Dict
    memory: Dict
    disk: Dict
    network: Dict


class ProcessMetrics(BaseModel):
    """Métricas de un proceso"""
    timestamp: float
    datetime: str
    pid: int
    name: str
    status: str
    cpu_percent: float
    memory: Dict
    num_threads: int
    create_time: float
    io: Optional[Dict] = None


def init_router(sm: SystemMonitor):
    """Inicializa el router con las dependencias necesarias"""
    global system_monitor
    system_monitor = sm


@router.get("/system", response_model=SystemMetrics)
async def get_system_metrics():
    """
    Obtiene métricas básicas del sistema (CPU, RAM)
    """
    stats = system_monitor.get_system_stats()
    return SystemMetrics(**stats)


@router.get("/system/detailed", response_model=DetailedSystemMetrics)
async def get_detailed_system_metrics():
    """
    Obtiene métricas detalladas del sistema incluyendo:
    - CPU (total y por core)
    - Memoria (total, usada, disponible)
    - Disco (total, usado, libre)
    - Red (bytes enviados/recibidos)
    """
    metrics = metrics_collector.collect_system_metrics()
    return DetailedSystemMetrics(**metrics)


@router.get("/system/history", response_model=List[DetailedSystemMetrics])
async def get_system_history(
    minutes: int = Query(default=5, ge=1, le=60, description="Minutos de historial")
):
    """
    Obtiene historial de métricas del sistema
    
    - **minutes**: Cantidad de minutos de historial (1-60)
    """
    history = metrics_collector.get_system_history(minutes=minutes)
    return [DetailedSystemMetrics(**m) for m in history]


@router.get("/process/{pid}", response_model=ProcessMetrics)
async def get_process_metrics(pid: int):
    """
    Obtiene métricas de un proceso específico
    
    - **pid**: Process ID del proceso
    """
    metrics = metrics_collector.collect_process_metrics(pid)
    
    if metrics is None:
        return {"error": f"Proceso {pid} no encontrado"}
    
    if "error" in metrics:
        return metrics
    
    return ProcessMetrics(**metrics)


@router.get("/process/{pid}/history", response_model=List[ProcessMetrics])
async def get_process_history(
    pid: int,
    minutes: int = Query(default=5, ge=1, le=60, description="Minutos de historial")
):
    """
    Obtiene historial de métricas de un proceso
    
    - **pid**: Process ID del proceso
    - **minutes**: Cantidad de minutos de historial (1-60)
    """
    history = metrics_collector.get_process_history(pid, minutes=minutes)
    return [ProcessMetrics(**m) for m in history]


@router.get("/summary")
async def get_metrics_summary():
    """
    Obtiene un resumen general de métricas del sistema y procesos monitoreados
    """
    system_stats = system_monitor.get_system_stats()
    all_process_stats = metrics_collector.process_history
    
    return {
        "system": system_stats,
        "monitored_processes": len(all_process_stats),
        "process_pids": list(all_process_stats.keys())
    }
