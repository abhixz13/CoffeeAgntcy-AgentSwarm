@echo off
REM AgentSwarm - Demo Log Viewer
REM Shows real-time agent activity

echo ============================================================
echo  AgentSwarm - Live Demo Log Viewer
echo ============================================================
echo.
echo Watching debug logs in real-time...
echo Press Ctrl+C to stop
echo.
echo ============================================================
echo.

REM Watch debug log and show key events
powershell -Command "Get-Content C:\code\coffeeAgentify\.cursor\debug.log -Wait | ForEach-Object { if ($_ -match 'location|intent|agent') { Write-Host $_ -ForegroundColor Green } }"
