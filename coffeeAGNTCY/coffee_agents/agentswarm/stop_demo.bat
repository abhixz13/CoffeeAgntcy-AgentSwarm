@echo off
REM AgentSwarm Demo - Stop All Services
REM Windows Batch Script

echo ============================================================
echo  AgentSwarm - Stopping All Services
echo ============================================================
echo.

echo Stopping all Python processes (agents and services)...
echo.

REM Kill all Python processes running the agents
taskkill /F /FI "WindowTitle eq Knowledge Agent*" 2>nul
taskkill /F /FI "WindowTitle eq Orchestrator*" 2>nul
taskkill /F /FI "WindowTitle eq CRM Agent*" 2>nul
taskkill /F /FI "WindowTitle eq Ticket Agent*" 2>nul
taskkill /F /FI "WindowTitle eq Escalation Agent*" 2>nul
taskkill /F /FI "WindowTitle eq Webex Bot Gateway*" 2>nul

echo.
echo ============================================================
echo  All services stopped!
echo ============================================================
echo.
echo Press any key to close...
pause >nul
