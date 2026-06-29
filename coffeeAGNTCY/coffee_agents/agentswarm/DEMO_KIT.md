# 🎬 AgentSwarm Demo Kit
## Everything You Need - No Panic Guide

---

## ⚡ ONE-CLICK START

```powershell
cd C:\code\coffeeAgentify\coffeeAGNTCY\coffee_agents\agentswarm
.\demo_start.ps1
```

**That's it.** Wait 30 seconds, dashboards open automatically.

---

## ✅ BEFORE DEMO (5 min before)

| # | Check | How |
|---|-------|-----|
| 1 | Docker Desktop running | Look for whale icon in system tray |
| 2 | VPN connected | For CIRCUIT API |
| 3 | Webex app open | To show bot responses |
| 4 | Run `.\demo_start.ps1` | Wait for "DEMO READY!" |

---

## 🎯 DEMO SCRIPT (Copy-Paste Ready)

### INTRO (30 seconds)
> "I built AgentSwarm - a multi-agent AI system for Webex Contact Center. 
> It has 4 specialist AI agents that collaborate to handle customer requests.
> Let me show you how it works with full observability."

---

### DEMO 1: Simple Query (2 agents)

**📱 Send to Webex Bot:**
```
Hi, I'm customer #67890 and I forgot my password. Can you help?
```

**🎤 Say while waiting:**
> "This query will trigger the CRM agent to look up the customer, 
> and the Knowledge agent to find password reset steps."

**📊 Show in Jaeger** (http://localhost:16686):
1. Select service: `agentswarm.knowledge`
2. Click "Find Traces"
3. Click newest trace → Show waterfall

**🎤 Say:**
> "Here's the distributed trace. You can see exactly which agents were called 
> and how long each took. This is OpenTelemetry tracing."

---

### DEMO 2: Complex Query (ALL 4 agents) ⭐

**📱 Send to Webex Bot:**
```
URGENT: I'm enterprise customer #11111, our entire office network is down affecting 50+ employees. We have a critical client presentation in 2 hours. Please help immediately!
```

**🎤 Say while waiting:**
> "This urgent query will trigger ALL 4 agents to collaborate - 
> CRM for customer lookup, Knowledge for troubleshooting, 
> Ticket to create a case, and Escalation to route to an engineer."

**📊 Show in Grafana** (http://localhost:3001):
1. Go to Explore
2. Select Jaeger datasource
3. Find the trace with longest duration
4. Click to show waterfall with all 4 agents

**🎤 Say:**
> "Look at this waterfall - all 4 agents worked together in under 10 seconds.
> The CRM agent identified them as an Enterprise VIP customer.
> The Escalation agent routed it to a Network Engineer immediately.
> In production, this observability helps us debug and optimize."

---

### DEMO 3: Show the Response

**📱 Show Webex response on screen:**

**🎤 Say:**
> "The response shows the orchestration flow, which agents were consulted,
> execution timeline, and a synthesized answer combining all agent insights.
> This is true multi-agent collaboration, not just one LLM call."

---

### WRAP UP (30 seconds)

**🎤 Say:**
> "To summarize: AgentSwarm uses LangGraph for orchestration, 
> OpenTelemetry for distributed tracing, Cisco CIRCUIT for the LLM,
> and integrates with Webex for the enterprise interface.
> 
> The key differentiator is observability - in production, 
> when something goes wrong, I can trace exactly what happened."

---

## 📋 COPY-PASTE PROMPTS

### Prompt 1: Simple (2 agents)
```
Hi, I'm customer #67890 and I forgot my password. Can you help?
```

### Prompt 2: Medium (3 agents)
```
I'm customer #12345 and my internet has been slow for 3 days. I've restarted my router twice. Can you create a ticket and help me fix this?
```

### Prompt 3: Full Demo - ALL 4 AGENTS ⭐
```
URGENT: I'm enterprise customer #11111, our entire office network is down affecting 50+ employees. We have a critical client presentation in 2 hours. Please help immediately!
```

### Prompt 4: Multi-Issue (Complex)
```
Hi, I'm customer #12345. I have several problems: 1) My bill seems wrong - charged twice this month, 2) My router keeps disconnecting, and 3) I want to upgrade to Premium tier. Can you help with all of this?
```

---

## 🔗 DASHBOARD URLS

| Dashboard | URL | Login |
|-----------|-----|-------|
| **Jaeger** | http://localhost:16686 | None |
| **Grafana** | http://localhost:3001 | admin / admin |
| **Prometheus** | http://localhost:9090 | None |

---

## 🚨 IF SOMETHING GOES WRONG

### Bot not responding?
```powershell
# Check bot gateway terminal for errors
# Restart just the bot:
python webex/bot_gateway.py
```

### No traces in Jaeger?
1. Send another message to bot
2. Wait 5 seconds
3. Click "Find Traces" again

### Agent error?
```powershell
# Check which port is down
.\demo_status.ps1

# Restart specific agent
python agents/knowledge/server.py
```

### Nuclear option - restart everything:
```powershell
.\demo_stop.ps1
.\demo_start.ps1
```

---

## 🎤 KEY TALKING POINTS

### For Technical Audience:
- "LangGraph for multi-agent orchestration"
- "OpenTelemetry distributed tracing"
- "Cisco CIRCUIT API for LLM"
- "Each agent is a microservice"

### For Business Audience:
- "4 specialist AI agents collaborate"
- "Handles customer requests in seconds"
- "Full visibility into what happened"
- "Enterprise-ready with Webex integration"

### For Observability Focus:
- "Every request has a trace ID"
- "Can debug slow requests instantly"
- "Production-ready monitoring"
- "Industry-standard OpenTelemetry"

---

## 💪 CONFIDENCE BOOSTERS

✅ **You built this** - You know it inside out

✅ **It's working** - You tested it already

✅ **Jaeger has traces** - Proof it works

✅ **4 agents collaborate** - That's impressive

✅ **Real Webex integration** - Not just CLI demo

✅ **Enterprise observability** - Production-ready

---

## 🏆 AFTER DEMO

**If they ask questions you can't answer:**
> "That's a great question. Let me look into that and follow up with you."

**If they want to see code:**
> "Sure, the orchestrator uses LangGraph. Here's the graph.py file..."

**If they ask about scaling:**
> "Each agent is a separate service. We can scale horizontally 
> and the OTEL Collector handles telemetry aggregation."

---

## 📱 QUICK REFERENCE CARD

```
┌─────────────────────────────────────────────────┐
│           AGENTSWARM DEMO QUICK REF             │
├─────────────────────────────────────────────────┤
│                                                 │
│  START:    .\demo_start.ps1                     │
│  STOP:     .\demo_stop.ps1                      │
│  STATUS:   .\demo_status.ps1                    │
│                                                 │
│  JAEGER:   http://localhost:16686               │
│  GRAFANA:  http://localhost:3001 (admin/admin)  │
│                                                 │
│  BEST PROMPT (all 4 agents):                    │
│  "URGENT: Enterprise customer #11111,           │
│   network down, 50 employees affected!"         │
│                                                 │
└─────────────────────────────────────────────────┘
```

---

**You've got this! 🚀**
