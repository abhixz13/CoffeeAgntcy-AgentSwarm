# AgentSwarm Quick Reference Card
## One-Page Cheat Sheet

---

## 🚀 START DEMO
```powershell
cd C:\code\coffeeAgentify\coffeeAGNTCY\coffee_agents\agentswarm
.\demo_start.ps1
```

## 🛑 STOP DEMO
```powershell
.\demo_stop.ps1
```

## 📊 CHECK STATUS
```powershell
.\demo_status.ps1
```

---

## 🔗 URLS

| Service | URL | Login |
|---------|-----|-------|
| Jaeger | http://localhost:16686 | - |
| Grafana | http://localhost:3001 | admin/admin |
| Orchestrator | http://localhost:8000 | - |

---

## 🎯 DEMO PROMPTS

**Simple (2 agents):**
```
Hi, I'm customer #67890 and I forgot my password
```

**Medium (3 agents):**
```
Customer #12345, internet slow for 3 days, create ticket please
```

**Full Demo (4 agents):**
```
URGENT: Enterprise customer #11111, network down, 50 employees affected!
```

---

## 🤖 AGENTS

| Agent | Port | Does |
|-------|------|------|
| Knowledge | 8001 | FAQs, troubleshooting |
| CRM | 8002 | Customer lookup |
| Ticket | 8003 | Create tickets |
| Escalation | 8004 | Route urgent issues |
| Orchestrator | 8000 | Coordinates all |

---

## 🔧 TROUBLESHOOTING

**Port in use:**
```powershell
netstat -ano | findstr "8001"
taskkill /PID <number> /F
```

**No traces in Jaeger:**
1. Send message to bot
2. Wait 5 seconds
3. Click "Find Traces"

**Restart everything:**
```powershell
.\demo_stop.ps1
.\demo_start.ps1
```

---

## 💬 KEY TALKING POINTS

- "4 specialist AI agents collaborate"
- "Full distributed tracing with OpenTelemetry"
- "Built on AGNTCY framework from Cisco Outshift"
- "Real Webex integration, not just CLI"
- "Production-ready observability"

---

## 📁 KEY FILES

```
agentswarm/
├── demo_start.ps1          # Start everything
├── demo_stop.ps1           # Stop everything
├── DEMO_KIT.md             # Full demo script
├── agents/
│   ├── orchestrator/
│   │   └── graph.py        # LangGraph workflow
│   ├── knowledge/
│   ├── crm/
│   ├── ticket/
│   └── escalation/
├── common/
│   ├── llm.py              # LLM factory
│   ├── circuit_llm.py      # CIRCUIT wrapper
│   └── observability.py    # Tracing
└── docs/                   # All documentation
```

---

## 🏆 SUCCESS METRICS

| Metric | Target |
|--------|--------|
| Response time | < 10 seconds |
| Agents collaborating | Up to 4 |
| Traces visible | 100% |
| Human intervention | Minimal |

---

*Print this page for quick reference during demo!*
