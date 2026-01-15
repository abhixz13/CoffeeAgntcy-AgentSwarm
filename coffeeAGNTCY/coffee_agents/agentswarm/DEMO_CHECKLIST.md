# AgentSwarm Demo - Quick Start Checklist

## 🚀 PRE-DEMO CHECKLIST

### ☐ Prerequisites (One-time setup)
- [ ] Docker Desktop installed
- [ ] Python 3.11+ installed
- [ ] `.env` file configured with CIRCUIT keys
- [ ] Webex Bot registered (BOT_QUEUE_NAME set)

---

## ⚡ QUICK START COMMANDS

### Step 1: Open PowerShell/Terminal
```powershell
cd C:\code\coffeeAgentify\coffeeAGNTCY\coffee_agents\agentswarm
```

### Step 2: Start Docker Desktop
- [ ] Open Docker Desktop from Start Menu
- [ ] Wait for whale icon to turn solid (30-60 sec)

### Step 3: Start Observability Stack
```powershell
docker-compose -f docker-compose.observability.yaml up -d
```

### Step 4: Verify Docker Containers
```powershell
docker ps --format "table {{.Names}}\t{{.Status}}"
```
**Expected:** 4 containers running (jaeger, grafana, prometheus, otel-collector)

### Step 5: Start All Agents (One Command)
```powershell
Start-Process cmd -ArgumentList '/k', 'python agents/knowledge/server.py'
Start-Process cmd -ArgumentList '/k', 'python agents/crm/server.py'
Start-Process cmd -ArgumentList '/k', 'python agents/ticket/server.py'
Start-Process cmd -ArgumentList '/k', 'python agents/escalation/server.py'
Start-Sleep -Seconds 3
Start-Process cmd -ArgumentList '/k', 'python agents/orchestrator/main.py'
Start-Sleep -Seconds 2
Start-Process cmd -ArgumentList '/k', 'python webex/bot_gateway.py'
```

### Step 6: Verify Agents Running
```powershell
netstat -ano | findstr "800"
```
**Expected:** Ports 8000, 8001, 8002, 8003, 8004 all LISTENING

### Step 7: Open Dashboards
```powershell
Start-Process "http://localhost:16686"   # Jaeger
Start-Process "http://localhost:3001"    # Grafana (admin/admin)
```

---

## ✅ DEMO READY CHECKLIST

| Component | Check | URL/Port |
|-----------|-------|----------|
| ☐ Docker running | `docker ps` shows 4 containers | - |
| ☐ Jaeger | Page loads | http://localhost:16686 |
| ☐ Grafana | Login works (admin/admin) | http://localhost:3001 |
| ☐ Knowledge Agent | Port 8001 listening | http://localhost:8001 |
| ☐ CRM Agent | Port 8002 listening | http://localhost:8002 |
| ☐ Ticket Agent | Port 8003 listening | http://localhost:8003 |
| ☐ Escalation Agent | Port 8004 listening | http://localhost:8004 |
| ☐ Orchestrator | Port 8000 listening | http://localhost:8000 |
| ☐ Webex Bot | Connected to RabbitMQ | Check terminal |

---

## 🎯 DEMO TEST QUERIES

### Test 1: Simple (2 agents)
```
Hi, I'm customer #67890 and I forgot my password
```

### Test 2: Medium (3 agents)
```
Customer #12345, internet slow for 3 days, please create ticket
```

### Test 3: Full Demo (ALL 4 agents)
```
URGENT: Enterprise customer #11111, network down, 50 employees affected!
```

---

## 🛑 STOP EVERYTHING

### Stop Agents
```powershell
Get-Process python | Stop-Process -Force
```

### Stop Docker
```powershell
docker-compose -f docker-compose.observability.yaml down
```

---

## 🔧 TROUBLESHOOTING

### Port already in use?
```powershell
netstat -ano | findstr "8000"
taskkill /PID <PID_NUMBER> /F
```

### Docker not connecting?
```powershell
docker info   # Should show Server Version
```
If error → Restart Docker Desktop

### No traces in Jaeger?
1. Send a test message to Webex bot
2. Wait 5 seconds
3. Refresh Jaeger, click "Find Traces"

---

## 📋 COPY-PASTE FULL STARTUP

```powershell
# FULL STARTUP SCRIPT - Copy and paste this entire block
cd C:\code\coffeeAgentify\coffeeAGNTCY\coffee_agents\agentswarm

# Start Docker stack
docker-compose -f docker-compose.observability.yaml up -d

# Wait for Docker
Start-Sleep -Seconds 5

# Start all agents
Start-Process cmd -ArgumentList '/k', 'python agents/knowledge/server.py'
Start-Process cmd -ArgumentList '/k', 'python agents/crm/server.py'
Start-Process cmd -ArgumentList '/k', 'python agents/ticket/server.py'
Start-Process cmd -ArgumentList '/k', 'python agents/escalation/server.py'
Start-Sleep -Seconds 4
Start-Process cmd -ArgumentList '/k', 'python agents/orchestrator/main.py'
Start-Sleep -Seconds 3
Start-Process cmd -ArgumentList '/k', 'python webex/bot_gateway.py'

# Open dashboards
Start-Sleep -Seconds 3
Start-Process "http://localhost:16686"
Start-Process "http://localhost:3001"

Write-Host "✅ Demo Ready! Send messages to your Webex bot."
```

---

**Good luck with your demo! 🚀**
