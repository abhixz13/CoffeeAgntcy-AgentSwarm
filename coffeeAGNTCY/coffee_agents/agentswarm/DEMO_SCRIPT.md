# AgentSwarm - Demo Guide

## 🎬 Demo Setup (5 minutes before demo)

### Step 1: Start All Services
```cmd
cd C:\code\coffeeAgentify\coffeeAGNTCY\coffee_agents\agentswarm
start_demo.bat
```
**Wait 10 seconds** for all services to initialize.

### Step 2: Setup Your Screen

#### Option A: Clean Demo (Recommended for Executives)
- **Minimize all terminal windows**
- **Open Webex** (full screen or large window)
- **That's it!** Let the magic happen invisibly

#### Option B: Technical Demo (Recommended for Developers/Hackathons)
- **Left side**: Webex window (50% screen)
- **Right side**: Run `watch_demo.bat` (50% screen)
  - Shows real-time logs of agent activity
  - Green highlighting for key events

#### Option C: Full Transparency (Advanced)
- **Keep 2-3 terminal windows visible:**
  - Orchestrator (Port 8000)
  - Bot Gateway (Webex connection)
  - One specialist agent (your choice)

---

## 🎯 Demo Script

### Introduction (30 seconds)
**Say:** "I built AgentSwarm - a multi-agent AI orchestration system for Webex Contact Center. Instead of one AI handling everything, I have **4 specialized agents** that collaborate to solve customer issues."

**Show:** Webex interface

---

### Demo 1: Simple FAQ (Knowledge Agent)
**Say:** "First, a simple question..."

**Type in Webex:**
```
How do I reset my password?
```

**Expected:** Knowledge Agent responds with troubleshooting steps

**Highlight:** "Notice the structured response with step-by-step instructions"

---

### Demo 2: Customer Lookup (CRM Agent)
**Say:** "Now let's look up a customer account..."

**Type in Webex:**
```
What is the status of customer account #12345?
```

**Expected:** CRM Agent returns customer tier, history

**Highlight:** "The system recognized this needs customer data and routed to the CRM specialist"

---

### Demo 3: Support Ticket (Ticket Agent)
**Say:** "Let's create a support ticket..."

**Type in Webex:**
```
Create a support ticket for login issues with account #67890
```

**Expected:** Ticket Agent creates ticket, assigns priority

**Highlight:** "Ticket number assigned, priority set automatically"

---

### Demo 4: Critical Escalation (Escalation Agent)
**Say:** "Finally, a critical issue requiring immediate escalation..."

**Type in Webex:**
```
URGENT: Premium customer #12345 system down for 2 hours!
```

**Expected:** Escalation Agent routes to Network Engineering team

**Highlight:** "The system detected urgency, customer tier, and automatically escalated to the right team with CRITICAL priority"

---

### Closing (30 seconds)
**Say:** "This demonstrates intelligent orchestration - the **Supervisor Agent** analyzes each query and routes to the right specialist. No manual routing, no delays. Just intelligent, automated customer support."

**Key Points:**
- ✅ 4 specialized agents working together
- ✅ AI-powered intent classification
- ✅ Webex integration (no external tools needed)
- ✅ Cisco CIRCUIT API (internal LLM, free for hackathons)
- ✅ Full observability and logging

---

## 🔧 Troubleshooting During Demo

### If a query doesn't work:
**Say:** "Let me try another query type..." (switch to a different agent)

### If response is slow:
**Say:** "The agents are consulting our internal LLM... notice the thoughtful, context-aware response"

### If terminal shows an error:
**Ignore it** - switch focus to Webex only

---

## 📊 Architecture Talking Points

**If asked "How does it work?":**

1. **Webex Integration** - Cisco Bot Gateway (RabbitMQ)
2. **Supervisor Agent** - Classifies intent using LLM
3. **Specialist Agents** - Knowledge, CRM, Ticket, Escalation
4. **HTTP Communication** - No Docker/containers needed
5. **Aggregator** - Synthesizes responses into coherent answers
6. **Observability** - Every interaction logged for debugging

**If asked "Why multi-agent?":**

- **Specialization**: Each agent is an expert in its domain
- **Scalability**: Add new agents without modifying existing ones
- **Maintainability**: Update one agent without breaking others
- **Performance**: Agents can eventually run in parallel

**If asked "What's the tech stack?":**

- **LangChain + LangGraph**: Agent orchestration framework
- **Cisco CIRCUIT API**: Internal LLM (GPT-4o-mini)
- **FastAPI**: Agent HTTP servers
- **Webex SDK**: Bot integration
- **Cisco Bot Gateway**: RabbitMQ messaging

---

## ✅ Demo Checklist

**5 minutes before:**
- [ ] Run `start_demo.bat`
- [ ] Check all 4 agents are running (look for "Uvicorn running" messages)
- [ ] Test one query in Webex to verify connectivity
- [ ] Arrange screen layout (Webex + optional logs)

**During demo:**
- [ ] Start with simple query (Knowledge Agent)
- [ ] Progress to more complex (Escalation Agent)
- [ ] Keep queries visible on screen
- [ ] Let responses complete before next query

**After demo:**
- [ ] Run `stop_demo.bat` to clean up
- [ ] Save any interesting logs for follow-up questions

---

## 🎥 Recording Tips

If recording a demo video:

1. **Use screen recording** (OBS, PowerPoint Recording, etc.)
2. **Enable microphone** for narration
3. **1920x1080 resolution** minimum
4. **Show Webex + logs side-by-side**
5. **Keep recording under 5 minutes**

**Script:** Follow the 4-query demo flow above
