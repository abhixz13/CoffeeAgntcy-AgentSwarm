# AgentSwarm for Contact Center - Setup Guide
## Webex Playtime FY26 Hackathon Project

---

## 📋 Pre-Hackathon Setup (Do This NOW)

### 1. Clone CoffeeAgntcy Repository
```bash
cd c:\code\coffeeAgentify
# Already done! ✓
```

### 2. Install Prerequisites

**Python & Package Manager:**
```bash
# Install uv (Python package manager)
# Windows (PowerShell):
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# Or use pip:
pip install uv

# Verify installation
uv --version
```

**Docker Desktop:**
- Download: https://www.docker.com/products/docker-desktop/
- Required for: SLIM messaging, observability stack
- Alternative: Use NATS directly (simpler but less features)

### 3. Get Webex Credentials

**A. Create Webex Bot (5 minutes)**
1. Go to: https://developer.webex.com/my-apps/new/bot
2. Fill in details:
   - Bot Name: `AgentSwarm Bot`
   - Bot Username: `agentswarm` (or your choice)
   - Icon: Upload any image
3. **SAVE YOUR BOT TOKEN** - you'll need it!

**B. Create Webex Space for Testing**
1. Open Webex app
2. Create new space: "AgentSwarm Demo"
3. Add your bot to the space
4. Get Room ID:
   ```bash
   # Use Webex API to list rooms
   curl -X GET https://webexapis.com/v1/rooms \
     -H "Authorization: Bearer YOUR_BOT_TOKEN"
   ```

### 4. Get LLM API Key

**Recommended: GROQ (Free & Fast)**
1. Sign up: https://console.groq.com/
2. Create API key: https://console.groq.com/keys
3. Free tier: 14,400 requests/day
4. Models: llama-3.3-70b-versatile (best for agents)

**Alternative: OpenAI**
1. Sign up: https://platform.openai.com/
2. Add $5-10 credits
3. Create API key
4. Model: gpt-4o-mini (cheaper) or gpt-4o

### 5. Configure Environment

**Create `.env` file in `coffeeAGNTCY/coffee_agents/`:**
```env
# LLM Configuration (GROQ - Free)
LLM_MODEL="groq/llama-3.3-70b-versatile"
GROQ_API_KEY="your_groq_api_key_here"

# Alternative: OpenAI
# LLM_MODEL="openai/gpt-4o-mini"
# OPENAI_API_KEY="your_openai_key_here"

# Webex Configuration
WEBEX_BOT_TOKEN="your_webex_bot_token_here"
WEBEX_ROOM_ID="your_room_id_here"

# Transport Configuration
DEFAULT_MESSAGE_TRANSPORT="slim"
TRANSPORT_SERVER_ENDPOINT="http://localhost:46357"

# Observability
OTLP_HTTP_ENDPOINT="http://localhost:4318"
LOGGING_LEVEL="DEBUG"

# Identity (Optional for hackathon)
IDENTITY_AUTH_ENABLED="false"
```

### 6. Test CoffeeAgntcy Setup

**Install dependencies:**
```bash
cd coffeeAGNTCY/coffee_agents/lungo
uv sync
```

**Start infrastructure:**
```bash
# In one terminal
docker compose up slim clickhouse-server otel-collector grafana
```

**Test basic agent (in another terminal):**
```bash
cd coffeeAGNTCY/coffee_agents/corto
uv run python farm/farm_server.py
```

If you see: `"INFO:     Application startup complete."` - You're ready! ✓

---

## 🚀 What You'll Build (4-Day Breakdown)

### Day 1 (Jan 23): Core Agent Framework
**Goal:** Get 1 agent talking to Webex
- [ ] Create `webex_orchestrator` agent (copy from Lungo supervisor)
- [ ] Create `knowledge_base_agent` (simple FAQ responses)
- [ ] Connect to Webex using webhooks
- [ ] Test end-to-end: Webex → Orchestrator → Knowledge Agent → Webex

**Output:** Working bot that answers simple questions

---

### Day 2 (Jan 26): Multi-Agent Coordination
**Goal:** Add agent-to-agent communication
- [ ] Create `crm_agent` (simulated customer data)
- [ ] Create `ticket_agent` (simulated ticket creation)
- [ ] Implement A2A messaging between agents (using SLIM from CoffeeAgntcy)
- [ ] Add streaming responses

**Output:** Multiple agents collaborating to answer complex queries

---

### Day 3 (Jan 27): Polish & Demo Prep
**Goal:** Make it look amazing
- [ ] Add observability dashboard (reuse Grafana from CoffeeAgntcy)
- [ ] Create Adaptive Cards for rich Webex messages
- [ ] Add demo scenarios (3-4 customer queries)
- [ ] Test everything end-to-end
- [ ] Record backup demo video

**Output:** Polished demo with visual dashboard

---

### Day 4 (Jan 28): Demo Day!
**Goal:** Show off your work
- [ ] Live demo with real Webex interactions
- [ ] Show agent collaboration in dashboard
- [ ] Explain the architecture
- [ ] Submit to Playtime

---

## 🎯 Minimum Viable Demo (MVP)

If time is tight, focus on this:

### Core Features (MUST HAVE):
1. ✅ Webex bot receives messages
2. ✅ Orchestrator routes to 2-3 specialized agents
3. ✅ Agents communicate via A2A (visible in logs)
4. ✅ Response sent back to Webex with agent collaboration summary

### Nice-to-Have (if time permits):
- Real-time dashboard showing agent interactions
- Adaptive Cards for rich responses
- Identity/TBAC for secure access
- Streaming responses

### Demo Flow:
```
User in Webex: "My internet is slow, order #12345"
                      ↓
         Orchestrator receives query
                      ↓
    ┌─────────────────┴─────────────────┐
    ↓                                   ↓
Knowledge Agent:              CRM Agent:
"Check router settings"       "Premium customer, 3 issues"
                      ↓
         Orchestrator combines responses
                      ↓
Webex: "I found troubleshooting steps. I see you're 
a premium customer with recent issues. I'm creating 
a priority ticket and escalating to senior support."
```

---

## 📦 What You Get From CoffeeAgntcy

### Reusable Components:
```
coffeeAGNTCY/coffee_agents/lungo/
├─ agents/supervisors/auction/graph/graph.py
│  └─ ExchangeGraph class (supervisor pattern)
│
├─ agents/supervisors/auction/graph/tools.py
│  ├─ A2A client creation
│  ├─ Agent communication patterns
│  └─ Identity verification (optional)
│
├─ agents/farms/colombia/agent.py
│  └─ Worker agent pattern
│
├─ config/config.py
│  └─ Configuration management
│
└─ docker-compose.yaml
   └─ Infrastructure setup (SLIM, Grafana, etc.)
```

### What to Copy:
1. **Supervisor Pattern** → Your Orchestrator
2. **Worker Pattern** → Your specialized agents
3. **A2A Communication** → Agent-to-agent messaging
4. **Observability Setup** → Dashboard for demo

---

## 🤔 Common Questions

### Q: Do I need Webex Contact Center access?
**A:** No! Start with Webex Messaging Bot. You can simulate contact center scenarios. If you have Contact Center access, even better, but it's not required.

### Q: Do I need to understand all of CoffeeAgntcy?
**A:** No! You'll extract:
- Supervisor pattern (1 file)
- Worker pattern (1 file)
- A2A communication (code snippets)
- Config setup (docker-compose)

Total reuse: ~500 lines of code

### Q: What if I don't have AGNTCY Identity credentials?
**A:** Skip it for the hackathon! Set `IDENTITY_AUTH_ENABLED="false"`. Identity is nice-to-have but not required for the demo.

### Q: Can I use a different language (Node.js, Java)?
**A:** Possible but harder. CoffeeAgntcy is Python-based. If you want to use Node.js, you'll need to rebuild the patterns yourself (loses the advantage of the reference implementation).

### Q: What if Docker doesn't work on my machine?
**A:** You can run without Docker:
- Use NATS directly (install NATS server)
- Skip observability stack (just show logs)
- Focus on core agent coordination

---

## 🎥 Demo Video Tips (Due Jan 27)

### What to Show (3-5 minutes):
1. **Problem Statement** (30 sec): Why single AI agents aren't enough
2. **Architecture** (45 sec): Show your multi-agent diagram
3. **Live Demo** (2 min): Customer query → agent collaboration → response
4. **Dashboard** (30 sec): Show agents communicating in real-time
5. **Impact** (30 sec): Benefits for Contact Center

### Recording Tools:
- Loom (free)
- OBS Studio (free)
- Zoom recording
- Windows Game Bar (Win+G)

---

## 📞 Need Help?

### Resources:
- **CoffeeAgntcy Docs**: https://docs.agntcy.org/
- **Webex Developer Docs**: https://developer.webex.com/docs/api/getting-started
- **LangGraph Docs**: https://langchain-ai.github.io/langgraph/

### During Hackathon:
- Check CoffeeAgntcy GitHub issues
- Webex Developer Support forums
- Your team and site coordinators

---

## ✅ Pre-Hackathon Checklist

**Complete before Jan 23:**
- [ ] CoffeeAgntcy repo cloned ✓
- [ ] Python & uv installed
- [ ] Docker Desktop installed (or NATS alternative)
- [ ] Webex bot created + token saved
- [ ] LLM API key obtained (GROQ or OpenAI)
- [ ] `.env` file configured
- [ ] Tested CoffeeAgntcy locally (run Corto demo)
- [ ] Read ExchangeGraph code (understand supervisor pattern)
- [ ] Webex space created for testing

**You're ready when:**
- Corto or Lungo demo runs successfully
- You can send/receive Webex messages with your bot
- You understand the supervisor-worker pattern

---

## 🎉 Let's Win This!

**Timeline:**
- **NOW - Jan 23**: Setup & preparation
- **Jan 23-27**: Build (3 coding days)
- **Jan 28**: Demo day
- **Feb 3**: Results!

**Next Steps:**
1. Complete setup checklist above
2. Test CoffeeAgntcy locally
3. Create Webex bot and test basic messaging
4. We'll build the agents together starting Jan 23!

Good luck! 🚀


