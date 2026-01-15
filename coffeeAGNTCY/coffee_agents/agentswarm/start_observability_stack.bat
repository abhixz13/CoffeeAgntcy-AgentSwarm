@echo off
REM AgentSwarm - Start Docker Observability Stack
REM Starts Jaeger, Grafana, Prometheus, OTEL Collector

echo.
echo ================================================================
echo       AGENTSWARM OBSERVABILITY STACK (Docker)
echo ================================================================
echo.

REM Change to agentswarm directory
cd /d "%~dp0"

REM Check if Docker is running
docker info >nul 2>&1
if errorlevel 1 (
    echo ERROR: Docker is not running!
    echo Please start Docker Desktop and try again.
    pause
    exit /b 1
)

echo [1/2] Starting observability containers...
docker-compose -f docker-compose.observability.yaml up -d

if errorlevel 1 (
    echo.
    echo ERROR: Failed to start containers.
    echo Check Docker logs for details.
    pause
    exit /b 1
)

echo.
echo [2/2] Waiting for services to be ready...
timeout /t 10 /nobreak >nul

echo.
echo ================================================================
echo  OBSERVABILITY STACK RUNNING!
echo ================================================================
echo.
echo  DASHBOARDS:
echo    - Jaeger (Traces):    http://localhost:16686
echo    - Grafana (Metrics):  http://localhost:3001  (admin/admin)
echo    - Prometheus:         http://localhost:9090
echo.
echo  TELEMETRY ENDPOINTS:
echo    - OTLP HTTP:          http://localhost:4318
echo    - OTLP gRPC:          localhost:4317
echo.
echo  Set this in your .env to enable trace export:
echo    OTLP_HTTP_ENDPOINT=http://localhost:4318
echo.
echo ================================================================
echo.

set /p OPEN="Open Jaeger UI in browser? (Y/N): "
if /i "%OPEN%"=="Y" (
    start http://localhost:16686
)

set /p OPEN2="Open Grafana in browser? (Y/N): "
if /i "%OPEN2%"=="Y" (
    start http://localhost:3001
)

echo.
echo To stop the stack, run: stop_observability_stack.bat
echo.
pause
