# Mini Orchestrator 🚀

Sistema de orquestación y monitoreo de procesos en tiempo real con FastAPI y Next.js.

## 📋 Características

### Backend (FastAPI)
- ✅ **Gestión de procesos**: Lanzar, detener y monitorear procesos del sistema
- ✅ **Métricas en tiempo real**: CPU, RAM del sistema y por proceso
- ✅ **Sistema de logs**: Logs individuales por job con rotación
- ✅ **API RESTful**: Endpoints documentados con Swagger/OpenAPI
- ✅ **Validación de comandos**: Sistema de seguridad para comandos peligrosos
- ✅ **Monitoreo continuo**: Thread dedicado para recolectar métricas

### Frontend (Next.js 16)
- ✅ **Dashboard en tiempo real**: Actualización automática cada 2 segundos
- ✅ **Visualización de métricas**: Gráficos de CPU y RAM con indicadores de estado
- ✅ **Gestión de jobs**: Crear, listar, detener procesos desde la UI
- ✅ **Logs interactivos**: Ver logs de cualquier job con un click
- ✅ **Diseño responsive**: Funciona en desktop y móvil
- ✅ **Dark mode**: Soporte para tema oscuro

## 🚀 Inicio Rápido

### Backend
\`\`\`bash
cd apps/backend
pip install -r requirements.txt
uvicorn main:app --reload
# → http://localhost:8000
\`\`\`

### Frontend
\`\`\`bash
cd apps/frontend
pnpm install
pnpm dev
# → http://localhost:3000
\`\`\`

## 📡 API Principal

- \`POST /jobs/\` - Crear job
- \`GET /jobs/\` - Listar jobs
- \`POST /jobs/{id}/kill\` - Detener job
- \`GET /metrics/system\` - Métricas del sistema
- \`GET /logs/{id}\` - Ver logs

**Documentación completa**: http://localhost:8000/docs

## 🎯 Uso

1. Abre http://localhost:3000
2. Click en "+ New Job"
3. Escribe un comando (ej: `sleep 30`)
4. Monitorea CPU/RAM en tiempo real
5. Ve logs con el botón "Logs"
6. Detén con "Kill"

## 🛠️ Stack Tecnológico

**Backend**: FastAPI + Uvicorn + psutil + Pydantic  
**Frontend**: Next.js 16 + React 19 + TypeScript + Tailwind CSS

## 📝 Licencia

MIT License - Código abierto
