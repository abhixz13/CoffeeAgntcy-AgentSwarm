@echo off
REM AgentSwarm Demo - Start All Services
REM Windows Batch Script

echo ============================================================
echo  AgentSwarm - Starting Demo Services
echo ============================================================
echo.

REM Change to agentswarm directory
cd /d "%~dp0"

echo [1/4] Starting Knowledge Agent (Port 8001)...
start "Knowledge Agent" cmd /k "python agents/knowledge/server.py"
timeout /t 3 /nobreak >nul

echo [2/4] Starting Orchestrator (Port 8000)...
start "Orchestrator" cmd /k "python agents/orchestrator/main.py"
timeout /t 3 /nobreak >nul

echo [3/4] Starting CRM Agent (Port 8002)...
start "CRM Agent" cmd /k "python agents/crm/server.py"
timeout /t 2 /nobreak >nul

echo [4/4] Starting Webex Bot Gateway...
start "Webex Bot Gateway" cmd /k "python webex/bot_gateway.py"
timeout /t 2 /nobreak >nul

echo.
echo ============================================================
echo  All services started!
echo ============================================================
echo.
echo Services running:
echo   - Knowledge Agent:  http://localhost:8001
echo   - Orchestrator:     http://localhost:8000
echo   - CRM Agent:        http://localhost:8002
echo   - Webex Bot:        Connected to RabbitMQ
echo.
echo Send a message to your Webex bot to test!
echo Press any key to open shutdown script...
pause >nul
start stop_demo.bat
