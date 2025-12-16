"""
Generador de IDs únicos para jobs
"""
import uuid
from datetime import datetime


def generate_job_id(prefix: str = "job") -> str:
    """
    Genera un ID único para un job
    
    Args:
        prefix: Prefijo para el ID (por defecto "job")
        
    Returns:
        ID único en formato: prefix_timestamp_uuid
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    unique_id = str(uuid.uuid4())[:8]
    return f"{prefix}_{timestamp}_{unique_id}"


def generate_short_id() -> str:
    """Genera un ID corto de 8 caracteres"""
    return str(uuid.uuid4())[:8]
