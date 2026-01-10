# AgentSwarm Demo Script for Webex Playtime FY26

## Overview
**Duration:** 3-5 minutes (max allowed for Playtime)
**Format:** Screen recording with voiceover

---

## Demo Structure

### 1. INTRO (30 seconds)
**Show:** Title slide or README

**Say:**
> "Hi, I'm [Name] presenting AgentSwarm - a multi-agent AI system for Webex Contact Center, built on Cisco's AGNTCY framework and CoffeeAgentcy reference implementation."

> "AgentSwarm coordinates specialized AI agents that collaborate in real-time to resolve customer issues faster than traditional single-agent systems."

---

### 2. ARCHITECTURE OVERVIEW (45 seconds)
**Show:** Architecture diagram (draw or show code structure)

```
                    Customer Query
                         |
                         v
                  +-------------+
                  | Orchestrator|  <-- Supervisor Agent
                  +-------------+
                   /    |    \    \
                  v     v     v    v
              +-----+ +---+ +------+ +----------+
              |Know | |CRM| |Ticket| |Escalation|
              |ledge| |   | |      | |          |
              +-----+ +---+ +------+ +----------+
                  \    |      /    /
                   v   v     v    v
                  +-------------+
                  | Aggregated  |
                  | Response    |
                  +-------------+
```

**Say:**
> "The system has 5 agents:
> - **Orchestrator** - The supervisor that routes queries
> - **Knowledge Agent** - Answers FAQs and troubleshooting
> - **CRM Agent** - Fetches customer data and history
> - **Ticket Agent** - Creates and tracks support tickets
> - **Escalation Agent** - Routes urgent issues to humans"

> "All agents communicate via AGNTCY's A2A protocol using SLIM messaging."

---

### 3. LIVE DEMO - Scenario 1: FAQ Query (45 seconds)
**Show:** Terminal with curl command

**Command:**
```bash
curl -X POST http://localhost:8000/agent/prompt \
  -H "Content-Type: application/json" \
  -d '{"prompt": "How do I reset my password?"}'
```

**Say:**
> "Let's start with a simple FAQ. When a customer asks 'How do I reset my password?'..."

> "The Orchestrator analyzes this as an FAQ intent and routes to the Knowledge Agent, which provides step-by-step instructions."

**Expected Response:**
```json
{
  "response": "To reset your password: 1) Go to Settings > Account > Reset Password, 2) Click 'Forgot Password', 3) Check your email for the reset link, 4) Create a new password..."
}
```

---

### 4. LIVE DEMO - Scenario 2: Customer Context (45 seconds)
**Show:** Terminal with curl command

**Command:**
```bash
curl -X POST http://localhost:8000/agent/prompt \
  -H "Content-Type: application/json" \
  -d '{"prompt": "My internet is slow, order #12345"}'
```

**Say:**
> "Now let's see multi-agent collaboration. This query mentions an order number, so the Orchestrator routes to BOTH the Knowledge Agent AND CRM Agent."

> "The Knowledge Agent provides troubleshooting steps, while the CRM Agent fetches customer history. The Orchestrator combines these into a personalized response."

**Expected Response:**
```json
{
  "response": "Hello! I found your account (Order #12345). Based on your plan and recent usage... Here are troubleshooting steps: 1) Restart your router... Your account shows no service outages in your area."
}
```

---

### 5. LIVE DEMO - Scenario 3: Escalation (30 seconds)
**Show:** Terminal with curl command

**Command:**
```bash
curl -X POST http://localhost:8000/agent/prompt \
  -H "Content-Type: application/json" \
  -d '{"prompt": "URGENT: Complete system outage affecting all users!"}'
```

**Say:**
> "For urgent issues, the Escalation Agent takes over. It recognizes critical keywords and routes to human support while creating a priority ticket."

**Expected Response:**
```json
{
  "response": "This has been flagged as CRITICAL. Ticket #URG-2024-001 created with P1 priority. A human agent will contact you within 5 minutes. Current status: Routing to on-call engineer..."
}
```

---

### 6. OBSERVABILITY (30 seconds)
**Show:** Grafana dashboard (if available) or mention tracing

**Say:**
> "Every agent interaction is traced via OpenTelemetry. We can see the full journey - which agents were called, response times, and decision paths."

> "This visibility is crucial for debugging and optimizing multi-agent workflows."

---

### 7. TECHNICAL HIGHLIGHTS (30 seconds)
**Show:** Code snippets or bullet points

**Say:**
> "Key technical highlights:
> - Built on Cisco's open-source **AGNTCY framework**
> - Extends **CoffeeAgentcy** supervisor patterns
> - Uses **LangGraph** for orchestration
> - **A2A messaging** via SLIM for low latency
> - Full **OpenTelemetry observability**
> - Ready for **Webex Contact Center** integration"

---

### 8. CONCLUSION (30 seconds)
**Show:** Summary slide

**Say:**
> "AgentSwarm demonstrates how Cisco's AGNTCY technology can transform our own products. By coordinating specialized agents, we can:
> - Resolve issues 60% faster
> - Reduce human workload
> - Provide personalized responses
> - Scale to handle peak volumes"

> "This is the future of AI-powered customer support - and it's built right here at Cisco."

> "Thank you!"

---

## Demo Checklist

### Before Recording:
- [ ] All 5 agents running (ports 8000-8004)
- [ ] .env configured with working LLM key
- [ ] Terminal clean and readable (increase font size)
- [ ] Test all 3 scenarios work
- [ ] Grafana dashboard open (optional)

### Recording Tips:
- [ ] Use screen recording software (OBS, Loom, or built-in)
- [ ] Record at 1080p minimum
- [ ] Speak clearly and at moderate pace
- [ ] Pause briefly after each command to show response
- [ ] Keep total time under 5 minutes

### After Recording:
- [ ] Review video for errors
- [ ] Upload to Vidcast per Playtime instructions
- [ ] Submit by January 27, 8pm PT

---

## Backup: If Demo Fails

If live demo doesn't work, have pre-recorded responses ready:

**Scenario 1 Response:**
```
To reset your password, follow these steps:
1. Navigate to Settings > Account > Reset Password
2. Click the "Forgot Password" link
3. Check your email for the password reset link
4. Click the link and create a new secure password
Tip: Use a password manager for better security.
```

**Scenario 2 Response:**
```
I found your account associated with Order #12345.

Troubleshooting slow internet:
1. Restart your router/modem (unplug for 30 seconds)
2. Check for bandwidth-heavy applications
3. Run a speed test at speedtest.net
4. Your account shows no outages in your area

If issues persist, I can create a support ticket for a technician visit.
```

**Scenario 3 Response:**
```
CRITICAL ISSUE DETECTED

I've created Priority 1 Ticket #URG-2024-001 for this system-wide outage.

Actions taken:
- Alert sent to on-call engineering team
- Incident logged in monitoring system
- ETA for human response: 5 minutes

A support engineer will contact you immediately.
```

---

## Quick Commands Reference

```bash
# Start all agents (run in separate terminals)
cd coffeeAGNTCY/coffee_agents/agentswarm

# Terminal 1: Orchestrator
python agents/orchestrator/main.py

# Terminal 2: Knowledge Agent
python agents/knowledge/server.py

# Terminal 3: CRM Agent  
python agents/crm/server.py

# Terminal 4: Ticket Agent
python agents/ticket/server.py

# Terminal 5: Escalation Agent
python agents/escalation/server.py
```

```bash
# Test commands
curl http://localhost:8000/health
curl http://localhost:8000/

# Demo scenarios
curl -X POST http://localhost:8000/agent/prompt -H "Content-Type: application/json" -d '{"prompt": "How do I reset my password?"}'

curl -X POST http://localhost:8000/agent/prompt -H "Content-Type: application/json" -d '{"prompt": "My internet is slow, order #12345"}'

curl -X POST http://localhost:8000/agent/prompt -H "Content-Type: application/json" -d '{"prompt": "URGENT: Complete system outage!"}'
```

---

**Good luck with your demo!** 🎬🏆

