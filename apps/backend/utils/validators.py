"""
Validadores de entrada para comandos y parámetros
"""
import shutil
from typing import List, Tuple
import os


class ValidationError(Exception):
    """Custom exception for validation errors"""
    pass


def validate_command(command: List[str]) -> Tuple[bool, str]:
    """
    Args:
        command: List with command and args
    Returns:
        (is valid: bool, mesage: str)
    """
    if not command or len(command) == 0:
        return False, "The command is empty"
    
    if not isinstance(command, list):
        return False, "Command must be a list"
    
    # Check if the command exist
    executable = command[0]
    
    # if is an absolute route check if exist
    if os.path.isabs(executable):
        if not os.path.exists(executable):
            return False, f"El ejecutable '{executable}' no existe"
    else:
        # search on PATH
        if not shutil.which(executable):
            return False, f"the command '{executable}' is not in path"
    
    # Black list 
    dangerous_commands = ["rm", "mkfs", "dd", "format", ">", ">>"]
    if any(cmd in command for cmd in dangerous_commands):
        return False, "Potential danger command detected"
    
    return True, "Valid command"


def validate_pid(pid: int) -> Tuple[bool, str]:
    """
    Args:
        pid: Process ID
        
    Returns:
        (is_valid, mesage)
    """
    if not isinstance(pid, int):
        return False, "El PID must to be a integer"
    
    if pid <= 0:
        return False, "PID must be gratter than 0"
    
    return True, "valid PID "


def validate_job_id(job_id: str) -> Tuple[bool, str]:
    """
    Valid format of job_id
    
    Args:
        job_id
    Returns:
        (is)valid, mesage)
    """
    if not job_id or not isinstance(job_id, str):
        return False, "job_id must be a non empty sting"
    
    if len(job_id) < 3:
        return False, "El job_id is so short-must be 3<len"
    
    return True, "Valid Job ID "
