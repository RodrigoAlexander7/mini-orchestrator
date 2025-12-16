"""
Router para logs de jobs
"""
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import List

from services.logger import job_logger


router = APIRouter(prefix="/logs", tags=["logs"])


class LogResponse(BaseModel):
    """Response con logs de un job"""
    job_id: str
    total_lines: int
    lines: List[str]


@router.get("/{job_id}", response_model=LogResponse)
async def get_job_logs(
    job_id: str,
    lines: int = Query(default=100, ge=1, le=10000, description="Número de líneas a obtener")
):
    """
    Obtiene los logs de un job específico
    
    - **job_id**: ID del job
    - **lines**: Número de últimas líneas a retornar (1-10000)
    """
    try:
        log_lines = job_logger.get_job_logs(job_id, lines=lines)
        
        if not log_lines:
            raise HTTPException(
                status_code=404,
                detail=f"No se encontraron logs para el job {job_id}"
            )
        
        # Limpiar saltos de línea
        cleaned_lines = [line.rstrip('\n') for line in log_lines]
        
        return LogResponse(
            job_id=job_id,
            total_lines=len(cleaned_lines),
            lines=cleaned_lines
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al obtener logs: {str(e)}"
        )


@router.delete("/{job_id}")
async def delete_job_logs(job_id: str):
    """
    Elimina los logs de un job específico
    
    - **job_id**: ID del job
    """
    from pathlib import Path
    from config import settings
    
    log_file = Path(settings.log_dir) / f"{job_id}.log"
    
    if not log_file.exists():
        raise HTTPException(
            status_code=404,
            detail=f"No se encontraron logs para el job {job_id}"
        )
    
    try:
        log_file.unlink()
        return {
            "message": f"Logs del job {job_id} eliminados exitosamente",
            "job_id": job_id
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al eliminar logs: {str(e)}"
        )


@router.post("/cleanup")
async def cleanup_old_logs(
    days: int = Query(default=7, ge=1, le=365, description="Días de retención")
):
    """
    Elimina logs más antiguos que X días
    
    - **days**: Días de retención (1-365)
    """
    try:
        job_logger.cleanup_old_logs(days=days)
        return {
            "message": f"Logs antiguos (>{days} días) eliminados exitosamente"
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al limpiar logs: {str(e)}"
        )
