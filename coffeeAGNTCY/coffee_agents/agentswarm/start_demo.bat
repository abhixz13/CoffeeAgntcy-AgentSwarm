@echo off
REM AgentSwarm Demo - Start All Services with Observability
REM Windows Batch Script

echo.
echo ================================================================
echo       AGENTSWARM MULTI-AGENT DEMO WITH OBSERVABILITY
echo            Powered by AGNTCY + Cisco CIRCUIT AI
echo ================================================================
echo.

REM Change to agentswarm directory
cd /d "%~dp0"

echo [1/6] Starting Knowledge Agent (Port 8001)...
start "Knowledge Agent" cmd /k "python agents/knowledge/server.py"
timeout /t 3 /nobreak >nul

echo [2/6] Starting CRM Agent (Port 8002)...
start "CRM Agent" cmd /k "python agents/crm/server.py"
timeout /t 2 /nobreak >nul

echo [3/6] Starting Ticket Agent (Port 8003)...
start "Ticket Agent" cmd /k "python agents/ticket/server.py"
timeout /t 2 /nobreak >nul

echo [4/6] Starting Escalation Agent (Port 8004)...
start "Escalation Agent" cmd /k "python agents/escalation/server.py"
timeout /t 2 /nobreak >nul

echo [5/6] Starting Orchestrator (Port 8000)...
start "Orchestrator" cmd /k "python agents/orchestrator/main.py"
timeout /t 3 /nobreak >nul

echo [6/6] Starting Webex Bot Gateway...
start "Webex Bot Gateway" cmd /k "python webex/bot_gateway.py"
timeout /t 2 /nobreak >nul

echo.
echo ================================================================
echo  All Agent Services Started!
echo ================================================================
echo.
echo  AGENT ENDPOINTS:
echo    - Knowledge Agent:    http://localhost:8001
echo    - CRM Agent:          http://localhost:8002
echo    - Ticket Agent:       http://localhost:8003
echo    - Escalation Agent:   http://localhost:8004
echo    - Orchestrator:       http://localhost:8000
echo    - Webex Bot:          Connected to RabbitMQ
echo.
echo ================================================================
echo.

set /p DASHBOARD="Start Observability Dashboard? (Y/N): "
if /i "%DASHBOARD%"=="Y" (
    echo.
    echo Starting Observability Dashboard (Port 8080)...
    start "Observability Dashboard" cmd /k "python observability_dashboard.py"
    timeout /t 3 /nobreak >nul
    echo.
    echo ================================================================
    echo  OBSERVABILITY DASHBOARD: http://localhost:8080
    echo ================================================================
    echo.
    echo  Open your browser to see:
    echo    - Real-time metrics
    echo    - Distributed traces
    echo    - Agent health monitoring
    echo    - Latency waterfall views
    echo.
    start http://localhost:8080
)

echo.
echo ================================================================
echo  DEMO READY! Send messages to your Webex bot.
echo ================================================================
echo.
echo  Try these demo queries:
echo.
echo  [2 Agents] "I'm customer #67890, forgot my password"
echo  [3 Agents] "Customer #12345, internet slow, create ticket"
echo  [4 Agents] "URGENT: Enterprise #11111, network down!"
echo.
echo ================================================================
echo.
echo Press any key to open shutdown script...
pause >nul
start stop_demo.bat
