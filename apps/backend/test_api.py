#!/usr/bin/env python3
"""
Script de prueba rápida del sistema
"""
import requests
import time
import json


BASE_URL = "http://localhost:8000"


def test_health():
    """Test health check"""
    print("🔍 Testing health check...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"✅ Status: {response.status_code}")
    print(json.dumps(response.json(), indent=2))
    print()


def test_system_metrics():
    """Test métricas del sistema"""
    print("📊 Testing system metrics...")
    response = requests.get(f"{BASE_URL}/metrics/system")
    print(f"✅ Status: {response.status_code}")
    print(json.dumps(response.json(), indent=2))
    print()


def test_create_job():
    """Test crear job"""
    print("🚀 Testing create job...")
    
    payload = {
        "command": ["sleep", "10"]
    }
    
    response = requests.post(f"{BASE_URL}/jobs/", json=payload)
    print(f"✅ Status: {response.status_code}")
    data = response.json()
    print(json.dumps(data, indent=2))
    print()
    
    return data.get("job_id")


def test_list_jobs():
    """Test listar jobs"""
    print("📋 Testing list jobs...")
    response = requests.get(f"{BASE_URL}/jobs/")
    print(f"✅ Status: {response.status_code}")
    print(json.dumps(response.json(), indent=2))
    print()


def test_get_job_logs(job_id):
    """Test obtener logs"""
    print(f"📝 Testing get logs for job {job_id}...")
    response = requests.get(f"{BASE_URL}/logs/{job_id}")
    
    if response.status_code == 200:
        print(f"✅ Status: {response.status_code}")
        data = response.json()
        print(f"Total lines: {data['total_lines']}")
        for line in data['lines'][:5]:  # Mostrar primeras 5 líneas
            print(f"  {line}")
    else:
        print(f"⚠️  Status: {response.status_code} - {response.json()}")
    print()


def test_stop_job(job_id):
    """Test detener job"""
    print(f"🛑 Testing stop job {job_id}...")
    response = requests.delete(f"{BASE_URL}/jobs/{job_id}")
    print(f"✅ Status: {response.status_code}")
    print(json.dumps(response.json(), indent=2))
    print()


def main():
    """Ejecutar todos los tests"""
    print("=" * 60)
    print("🧪 MINI ORCHESTRATOR - TEST SUITE")
    print("=" * 60)
    print()
    
    try:
        # 1. Health check
        test_health()
        
        # 2. System metrics
        test_system_metrics()
        
        # 3. Create job
        job_id = test_create_job()
        
        if job_id:
            # 4. List jobs
            time.sleep(1)
            test_list_jobs()
            
            # 5. Get logs
            time.sleep(1)
            test_get_job_logs(job_id)
            
            # 6. Stop job
            test_stop_job(job_id)
        
        print("=" * 60)
        print("✅ All tests completed!")
        print("=" * 60)
        
    except requests.exceptions.ConnectionError:
        print("❌ Error: No se pudo conectar al servidor")
        print("   Asegúrate de que el servidor esté corriendo en http://localhost:8000")
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()
