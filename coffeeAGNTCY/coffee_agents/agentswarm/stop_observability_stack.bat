@echo off
REM AgentSwarm - Stop Docker Observability Stack

echo.
echo ================================================================
echo  Stopping Observability Stack...
echo ================================================================
echo.

cd /d "%~dp0"

docker-compose -f docker-compose.observability.yaml down

echo.
echo ================================================================
echo  Observability stack stopped.
echo ================================================================
echo.
pause
