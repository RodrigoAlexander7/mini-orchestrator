"""
Mini Orchestrator - Sistema de gestión y monitoreo de procesos
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from config import settings
from core.process_manager import ProcessManager
from core.system_monitor import SystemMonitor
from core.job_monitor import JobMonitorManager

# Importar routers
from routers import jobs, metrics, logs


# Instancias globales
process_manager = ProcessManager()
system_monitor = SystemMonitor()
job_monitor = JobMonitorManager(
    process_manager=process_manager,
    interval=settings.monitor_interval
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Gestión del ciclo de vida de la aplicación
    - Startup: inicializar servicios
    - Shutdown: limpiar recursos
    """
    # Startup
    print("🚀 Iniciando Mini Orchestrator...")
    
    # Inicializar routers con dependencias
    jobs.init_router(process_manager, job_monitor)
    metrics.init_router(system_monitor)
    
    print("✅ Routers inicializados")
    print(f"📊 Intervalo de monitoreo: {settings.monitor_interval}s")
    print(f"📁 Directorio de logs: {settings.log_dir}")
    
    yield
    
    # Shutdown
    print("🛑 Cerrando Mini Orchestrator...")
    job_monitor.shutdown()
    print("✅ Recursos liberados")


# Crear aplicación FastAPI
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Sistema de orquestación y monitoreo de procesos con FastAPI",
    lifespan=lifespan
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registrar routers
app.include_router(jobs.router)
app.include_router(metrics.router)
app.include_router(logs.router)


@app.get("/")
def root():
    """Endpoint raíz - health check"""
    return {
        "status": "ok",
        "app": settings.app_name,
        "version": settings.app_version,
        "endpoints": {
            "jobs": "/jobs",
            "metrics": "/metrics",
            "logs": "/logs",
            "docs": "/docs"
        }
    }


@app.get("/health")
def health_check():
    """Health check detallado"""
    system_stats = system_monitor.get_system_stats()
    
    return {
        "status": "healthy",
        "system": system_stats,
        "active_jobs": len(jobs.jobs_db),
        "monitored_processes": len(job_monitor.monitors)
    }


if __name__ == "__main__":
    import uvicorn
    
    print(f"🌐 Iniciando servidor en http://{settings.host}:{settings.port}")
    
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug
    )
