# Mini Orchestrator - Backend

Sistema de orquestación y monitoreo de procesos construido con FastAPI.

## 🚀 Características

- **Gestión de Procesos**: Lanzar, detener y monitorear procesos del sistema
- **Monitoreo en Tiempo Real**: Métricas de CPU, RAM, Disco y Red
- **Sistema de Logs**: Logs individuales por proceso/job
- **API RESTful**: Endpoints documentados con OpenAPI/Swagger
- **Validación de Comandos**: Seguridad en la ejecución de comandos
- **Historial de Métricas**: Tracking temporal de recursos

## 📁 Estructura del Proyecto

```
backend/
│
├── main.py                 → Aplicación FastAPI principal
├── config.py               → Configuración global (pydantic-settings)
│
├── core/
│   ├── process_manager.py  → Gestión de procesos (subprocess)
│   ├── system_monitor.py   → Monitoreo de sistema (psutil)
│   ├── job_monitor.py      → Monitoreo por job (threads + psutil)
│
├── models/
│   └── job_model.py        → Modelo de datos Job (Pydantic)
│
├── routers/
│   ├── jobs.py             → Endpoints: crear, listar, detener jobs
│   ├── metrics.py          → Endpoints: métricas sistema y procesos
│   └── logs.py             → Endpoints: ver logs de jobs
│
├── services/
│   ├── logger.py           → Sistema de logging por job
│   └── metrics_collector.py→ Recolector de métricas históricas
│
└── utils/
    ├── id_generator.py     → Generador de IDs únicos
    └── validators.py       → Validadores de entrada
```

## 🛠️ Instalación

### 1. Crear entorno virtual

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# o
.venv\Scripts\activate  # Windows
```

### 2. Instalar dependencias

```bash
pip install -r requirements.txt

# Opcional: dependencias de desarrollo
pip install -r dev-requirements.txt
```

### 3. Configurar variables de entorno

```bash
cp .env.example .env
# Editar .env según necesidades
```

### 4. Ejecutar servidor

```bash
# Modo desarrollo (con hot-reload)
python main.py

# O con uvicorn directamente
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## 📚 Documentación API

Una vez iniciado el servidor, accede a:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## 🔌 Endpoints Principales

### Jobs (Procesos)

- `POST /jobs/` - Crear nuevo job
- `GET /jobs/` - Listar todos los jobs
- `GET /jobs/{job_id}` - Obtener info de un job
- `DELETE /jobs/{job_id}` - Detener job
- `POST /jobs/{job_id}/restart` - Reiniciar job

### Métricas

- `GET /metrics/system` - Métricas básicas del sistema
- `GET /metrics/system/detailed` - Métricas detalladas
- `GET /metrics/system/history` - Historial de métricas
- `GET /metrics/process/{pid}` - Métricas de un proceso
- `GET /metrics/process/{pid}/history` - Historial de proceso

### Logs

- `GET /logs/{job_id}` - Obtener logs de un job
- `DELETE /logs/{job_id}` - Eliminar logs de un job
- `POST /logs/cleanup` - Limpiar logs antiguos

## 📝 Ejemplos de Uso

### Crear un job

```bash
curl -X POST "http://localhost:8000/jobs/" \
  -H "Content-Type: application/json" \
  -d '{
    "command": ["python", "-c", "import time; time.sleep(30)"]
  }'
```

### Listar jobs

```bash
curl "http://localhost:8000/jobs/"
```

### Obtener métricas del sistema

```bash
curl "http://localhost:8000/metrics/system"
```

### Ver logs de un job

```bash
curl "http://localhost:8000/logs/job_20241211_123456_abc123"
```

## ⚙️ Configuración

Edita el archivo `.env` para personalizar:

- Puerto del servidor
- Intervalo de monitoreo
- Directorio de logs
- Límites de procesos concurrentes
- Orígenes CORS permitidos

## 🔒 Seguridad

- Validación de comandos antes de ejecución
- Lista negra de comandos peligrosos
- Verificación de existencia de ejecutables
- Límite de procesos concurrentes

## 🧪 Testing (Opcional)

```bash
# Ejecutar tests
pytest

# Con coverage
pytest --cov=. --cov-report=html
```

## 📦 Dependencias Principales

- **FastAPI** - Framework web moderno y rápido
- **Uvicorn** - Servidor ASGI de alto rendimiento
- **Pydantic** - Validación de datos
- **psutil** - Monitoreo de sistema y procesos
- **python-dotenv** - Gestión de variables de entorno

## 🤝 Contribución

1. Fork el proyecto
2. Crea una rama (`git checkout -b feature/nueva-funcionalidad`)
3. Commit cambios (`git commit -m 'Añadir funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto es de código abierto.

## 🐛 Problemas Conocidos

- El monitoreo por threads puede ser intensivo en sistemas con muchos procesos
- Algunos comandos requieren permisos especiales
- En Windows, algunos comandos pueden comportarse diferente

## 🔮 Roadmap

- [ ] Autoscaling automático basado en métricas
- [ ] Integración con IA para predicción de recursos
- [ ] Scheduler de tareas programadas
- [ ] Persistencia de jobs en base de datos
- [ ] WebSocket para métricas en tiempo real
- [ ] Dashboard web integrado
