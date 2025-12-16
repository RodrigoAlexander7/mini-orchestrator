"""
Configuración global de la aplicación
"""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Configuraciones del servidor de orquestación"""
    
    # API Settings
    app_name: str = "Mini Orchestrator"
    app_version: str = "1.0.0"
    debug: bool = False
    
    # Server
    host: str = "0.0.0.0"
    port: int = 8000
    
    # Monitoring
    monitor_interval: float = 1.0  # segundos entre lecturas
    log_retention_days: int = 7
    
    # Process limits
    max_concurrent_jobs: int = 50
    job_timeout: int = 3600  # segundos
    
    # Paths
    log_dir: str = "./logs"
    
    # CORS
    cors_origins: list = ["http://localhost:3000", "http://localhost:3001"]
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# Instancia global
settings = Settings()
