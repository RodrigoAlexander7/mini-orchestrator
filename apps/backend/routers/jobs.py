"""
Router para gestión de jobs (procesos)
"""
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from typing import List, Optional, Dict
from datetime import datetime

from core.process_manager import ProcessManager
from core.job_monitor import JobMonitorManager
from models.job_model import Job
from utils.id_generator import generate_job_id
from utils.validators import validate_command, validate_job_id
from services.logger import job_logger


router = APIRouter(prefix="/jobs", tags=["jobs"])

# Estos se inyectarán desde main.py
process_manager: Optional[ProcessManager] = None
job_monitor: Optional[JobMonitorManager] = None

# Almacenamiento en memoria de jobs (job_id -> Job)
jobs_db: Dict[str, Job] = {}


class CreateJobRequest(BaseModel):
    """Request para crear un nuevo job"""
    command: List[str]
    job_id: Optional[str] = None


class CreateJobResponse(BaseModel):
    """Response al crear un job"""
    job_id: str
    pid: int
    command: List[str]
    status: str
    message: str


class JobStatus(BaseModel):
    """Estado detallado de un job"""
    job_id: str
    pid: int
    command: List[str]
    status: str
    created_at: str
    metrics: Optional[Dict] = None


class JobListResponse(BaseModel):
    """Lista de jobs"""
    total: int
    jobs: List[JobStatus]


def init_router(pm: ProcessManager, jm: JobMonitorManager):
    """Inicializa el router con las dependencias necesarias"""
    global process_manager, job_monitor
    process_manager = pm
    job_monitor = jm


@router.post("/", response_model=CreateJobResponse, status_code=status.HTTP_201_CREATED)
async def create_job(request: CreateJobRequest):
    """
    Lanza un nuevo proceso/job
    
    - **command**: Lista con el comando y sus argumentos
    - **job_id**: ID opcional (se genera automáticamente si no se provee)
    """
    # Validar comando
    is_valid, msg = validate_command(request.command)
    if not is_valid:
        raise HTTPException(status_code=400, detail=msg)
    
    # Generar job_id si no se provee
    job_id = request.job_id or generate_job_id()
    
    # Validar job_id
    is_valid, msg = validate_job_id(job_id)
    if not is_valid:
        raise HTTPException(status_code=400, detail=msg)
    
    # Verificar que no exista
    if job_id in jobs_db:
        raise HTTPException(status_code=400, detail=f"Job {job_id} ya existe")
    
    try:
        # Lanzar proceso
        pid = process_manager.start_job(request.command)
        
        # Crear registro del job
        job = Job(
            job_id=job_id,
            pid=pid,
            command=request.command,
            status="running"
        )
        jobs_db[job_id] = job
        
        # Iniciar monitoreo
        job_monitor.start_monitoring(pid)
        
        # Log del inicio
        job_logger.log_job_start(job_id, request.command, pid)
        
        return CreateJobResponse(
            job_id=job_id,
            pid=pid,
            command=request.command,
            status="running",
            message=f"Job {job_id} iniciado exitosamente"
        )
        
    except Exception as e:
        job_logger.log_job_error(job_id, str(e))
        raise HTTPException(status_code=500, detail=f"Error al iniciar job: {str(e)}")


@router.get("/", response_model=JobListResponse)
async def list_jobs():
    """
    Lista todos los jobs activos
    """
    jobs_list = []
    
    for job_id, job in jobs_db.items():
        # Obtener métricas actuales
        metrics = job_monitor.get_stats(job.pid)
        
        jobs_list.append(JobStatus(
            job_id=job_id,
            pid=job.pid,
            command=job.command,
            status=job.status,
            created_at=datetime.now().isoformat(),  # TODO: guardar timestamp real
            metrics=metrics
        ))
    
    return JobListResponse(
        total=len(jobs_list),
        jobs=jobs_list
    )


@router.get("/{job_id}", response_model=JobStatus)
async def get_job(job_id: str):
    """
    Obtiene información detallada de un job específico
    """
    if job_id not in jobs_db:
        raise HTTPException(status_code=404, detail=f"Job {job_id} no encontrado")
    
    job = jobs_db[job_id]
    metrics = job_monitor.get_stats(job.pid)
    
    return JobStatus(
        job_id=job_id,
        pid=job.pid,
        command=job.command,
        status=job.status,
        created_at=datetime.now().isoformat(),
        metrics=metrics
    )


@router.delete("/{job_id}")
async def stop_job(job_id: str):
    """
    Detiene y elimina un job
    """
    if job_id not in jobs_db:
        raise HTTPException(status_code=404, detail=f"Job {job_id} no encontrado")
    
    job = jobs_db[job_id]
    
    try:
        # Detener el proceso
        success = process_manager.stop_job(job.pid)
        
        if not success:
            raise HTTPException(status_code=500, detail="No se pudo detener el proceso")
        
        # Detener monitoreo
        job_monitor.stop_monitoring(job.pid)
        
        # Log del fin
        job_logger.log_job_end(job_id, job.pid)
        
        # Actualizar estado
        job.status = "stopped"
        
        # Eliminar del registro
        del jobs_db[job_id]
        
        return {
            "message": f"Job {job_id} detenido exitosamente",
            "job_id": job_id,
            "pid": job.pid
        }
        
    except Exception as e:
        job_logger.log_job_error(job_id, str(e))
        raise HTTPException(status_code=500, detail=f"Error al detener job: {str(e)}")


@router.post("/{job_id}/restart")
async def restart_job(job_id: str):
    """
    Reinicia un job (lo detiene y lo vuelve a lanzar)
    """
    if job_id not in jobs_db:
        raise HTTPException(status_code=404, detail=f"Job {job_id} no encontrado")
    
    job = jobs_db[job_id]
    command = job.command
    
    # Detener el job actual
    await stop_job(job_id)
    
    # Relanzar con el mismo comando
    request = CreateJobRequest(command=command, job_id=job_id)
    return await create_job(request)
