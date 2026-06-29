# AgentSwarm Presentation Slides
## Multi-Agent AI System for Webex Contact Center

---

# SLIDE 1: Title

```
┌─────────────────────────────────────────────────────────────┐
│                                                              │
│                      AGENTSWARM                              │
│                                                              │
│         Multi-Agent AI for Enterprise Support                │
│                                                              │
│    ┌─────┐  ┌─────┐  ┌─────┐  ┌─────┐                      │
│    │ 🧠  │  │ 👤  │  │ 🎫  │  │ 🚨  │                      │
│    │Know │  │ CRM │  │Tick │  │Escal│                      │
│    └─────┘  └─────┘  └─────┘  └─────┘                      │
│                                                              │
│         Powered by AGNTCY + Cisco CIRCUIT                   │
│                                                              │
│                     [Your Name]                              │
│                    January 2026                              │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

**Speaker Notes:**
- Introduce yourself
- "Today I'll show you AgentSwarm - a multi-agent AI system I built for Webex Contact Center"

---

# SLIDE 2: The Problem

```
┌─────────────────────────────────────────────────────────────┐
│                                                              │
│              THE PROBLEM WITH SINGLE-LLM SUPPORT             │
│                                                              │
│    ┌─────────────────────────────────────────────────┐      │
│    │                                                  │      │
│    │   Customer: "My network is down, I'm a VIP      │      │
│    │              customer, create urgent ticket!"    │      │
│    │                                                  │      │
│    │   Single LLM: "I'm sorry to hear that.          │      │
│    │               Have you tried restarting?"       │      │
│    │                                                  │      │
│    └─────────────────────────────────────────────────┘      │
│                                                              │
│    ❌ No customer context                                    │
│    ❌ No ticket creation                                     │
│    ❌ No escalation                                          │
│    ❌ No specialized knowledge                               │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

**Speaker Notes:**
- "A single LLM can only give generic responses"
- "It can't access customer data, create tickets, or escalate"

---

# SLIDE 3: The Solution

```
┌─────────────────────────────────────────────────────────────┐
│                                                              │
│              THE SOLUTION: MULTI-AGENT COLLABORATION         │
│                                                              │
│                      ┌───────────┐                          │
│                      │ Customer  │                          │
│                      │  Query    │                          │
│                      └─────┬─────┘                          │
│                            │                                 │
│                            ▼                                 │
│                    ┌───────────────┐                        │
│                    │  Orchestrator │                        │
│                    │  (Supervisor) │                        │
│                    └───────┬───────┘                        │
│                            │                                 │
│         ┌──────────┬───────┼───────┬──────────┐            │
│         ▼          ▼       ▼       ▼          ▼            │
│    ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐            │
│    │  CRM   │ │Knowledge│ │ Ticket │ │Escalate│            │
│    │ Agent  │ │ Agent   │ │ Agent  │ │ Agent  │            │
│    └────────┘ └────────┘ └────────┘ └────────┘            │
│                            │                                 │
│                            ▼                                 │
│                    ┌───────────────┐                        │
│                    │   Unified     │                        │
│                    │   Response    │                        │
│                    └───────────────┘                        │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

**Speaker Notes:**
- "AgentSwarm uses 4 specialist agents that collaborate"
- "Each agent has specific expertise and capabilities"

---

# SLIDE 4: The Four Agents

```
┌─────────────────────────────────────────────────────────────┐
│                                                              │
│                    SPECIALIST AGENTS                         │
│                                                              │
│  ┌─────────────────────────┐  ┌─────────────────────────┐  │
│  │      🧠 KNOWLEDGE        │  │        👤 CRM           │  │
│  │                          │  │                          │  │
│  │  • Technical docs        │  │  • Customer lookup       │  │
│  │  • FAQs                  │  │  • Account history       │  │
│  │  • Troubleshooting       │  │  • Subscription tier     │  │
│  │  • How-to guides         │  │  • Priority level        │  │
│  └─────────────────────────┘  └─────────────────────────┘  │
│                                                              │
│  ┌─────────────────────────┐  ┌─────────────────────────┐  │
│  │       🎫 TICKET          │  │      🚨 ESCALATION      │  │
│  │                          │  │                          │  │
│  │  • Create tickets        │  │  • Urgency assessment    │  │
│  │  • Assign priority       │  │  • Team routing          │  │
│  │  • Track status          │  │  • Human handoff         │  │
│  │  • Set categories        │  │  • VIP handling          │  │
│  └─────────────────────────┘  └─────────────────────────┘  │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

**Speaker Notes:**
- Walk through each agent's capabilities
- "Together they handle any customer scenario"

---

# SLIDE 5: How It Works

```
┌─────────────────────────────────────────────────────────────┐
│                                                              │
│                    HOW AGENTSWARM WORKS                      │
│                                                              │
│   1️⃣ RECEIVE                                                 │
│      Customer sends message via Webex                        │
│                                                              │
│   2️⃣ ANALYZE                                                 │
│      Supervisor classifies intent                            │
│      Determines which agents to involve                      │
│                                                              │
│   3️⃣ COLLABORATE                                             │
│      Selected agents process in parallel                     │
│      Share context with each other                           │
│                                                              │
│   4️⃣ SYNTHESIZE                                              │
│      Aggregator combines all responses                       │
│      Creates unified, coherent answer                        │
│                                                              │
│   5️⃣ RESPOND                                                 │
│      Customer receives comprehensive response                │
│      All in under 10 seconds!                                │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

**Speaker Notes:**
- "The whole process takes under 10 seconds"
- "Customer gets a comprehensive response from all relevant agents"

---

# SLIDE 6: Live Demo

```
┌─────────────────────────────────────────────────────────────┐
│                                                              │
│                      🎬 LIVE DEMO                            │
│                                                              │
│                                                              │
│         "URGENT: I'm enterprise customer #11111,            │
│          our network is down affecting 50 employees.        │
│          Critical presentation in 2 hours!"                 │
│                                                              │
│                                                              │
│                         ┌─────────┐                         │
│                         │  DEMO   │                         │
│                         │  TIME   │                         │
│                         └─────────┘                         │
│                                                              │
│                                                              │
│         Watch all 4 agents collaborate in real-time         │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

**Speaker Notes:**
- Switch to Webex, send the message
- Show the response
- Switch to Jaeger to show the trace

---

# SLIDE 7: Observability

```
┌─────────────────────────────────────────────────────────────┐
│                                                              │
│              ENTERPRISE-GRADE OBSERVABILITY                  │
│                                                              │
│    ┌─────────────────────────────────────────────────┐      │
│    │                                                  │      │
│    │  DISTRIBUTED TRACE (Jaeger)                     │      │
│    │                                                  │      │
│    │  orchestrator.run     ████████████████  1.2s   │      │
│    │    ├─ supervisor      ████              150ms  │      │
│    │    ├─ crm.process     ██████            320ms  │      │
│    │    ├─ knowledge       ████              180ms  │      │
│    │    ├─ ticket          █████             250ms  │      │
│    │    ├─ escalation      ████              200ms  │      │
│    │    └─ aggregator      ████              200ms  │      │
│    │                                                  │      │
│    └─────────────────────────────────────────────────┘      │
│                                                              │
│    ✅ OpenTelemetry standard                                 │
│    ✅ Every request traced                                   │
│    ✅ Debug any issue instantly                              │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

**Speaker Notes:**
- "Every request has a trace ID"
- "I can see exactly which agent took how long"
- "This is critical for production debugging"

---

# SLIDE 8: Technology Stack

```
┌─────────────────────────────────────────────────────────────┐
│                                                              │
│                    TECHNOLOGY STACK                          │
│                                                              │
│    ┌──────────────────┬──────────────────────────────┐      │
│    │    Component     │        Technology            │      │
│    ├──────────────────┼──────────────────────────────┤      │
│    │ Orchestration    │ LangGraph                    │      │
│    │ LLM              │ Cisco CIRCUIT API            │      │
│    │ Framework        │ AGNTCY (Cisco Outshift)      │      │
│    │ Tracing          │ OpenTelemetry + Jaeger       │      │
│    │ Metrics          │ Prometheus + Grafana         │      │
│    │ Interface        │ Webex Bot                    │      │
│    │ API              │ FastAPI                      │      │
│    │ Infrastructure   │ Docker                       │      │
│    └──────────────────┴──────────────────────────────┘      │
│                                                              │
│    All open standards • Production ready • Scalable         │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

**Speaker Notes:**
- "Built on industry standards"
- "AGNTCY is Cisco Outshift's multi-agent framework"
- "Everything is containerized and scalable"

---

# SLIDE 9: Key Differentiators

```
┌─────────────────────────────────────────────────────────────┐
│                                                              │
│                  WHY AGENTSWARM IS DIFFERENT                 │
│                                                              │
│                                                              │
│    🔹 TRUE MULTI-AGENT                                       │
│       Not just one LLM - 4 specialists collaborating        │
│                                                              │
│    🔹 CONTEXT SHARING                                        │
│       Agents share information intelligently                 │
│                                                              │
│    🔹 ENTERPRISE OBSERVABILITY                               │
│       Full distributed tracing, not black box               │
│                                                              │
│    🔹 REAL INTEGRATION                                       │
│       Webex, not just CLI demo                              │
│                                                              │
│    🔹 PRODUCTION PATTERNS                                    │
│       Error handling, timeouts, health checks               │
│                                                              │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

**Speaker Notes:**
- "This isn't a toy demo"
- "It's built with production patterns from day one"

---

# SLIDE 10: Results

```
┌─────────────────────────────────────────────────────────────┐
│                                                              │
│                        RESULTS                               │
│                                                              │
│                                                              │
│         ┌─────────────────────────────────────┐             │
│         │                                      │             │
│         │    < 10 sec    Response time        │             │
│         │                                      │             │
│         │    4 agents    Collaborating        │             │
│         │                                      │             │
│         │    100%        Requests traced      │             │
│         │                                      │             │
│         │    0           Human intervention   │             │
│         │                (for routine queries)│             │
│         │                                      │             │
│         └─────────────────────────────────────┘             │
│                                                              │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

**Speaker Notes:**
- "Most queries resolved without human intervention"
- "Full observability for debugging"

---

# SLIDE 11: Future Vision

```
┌─────────────────────────────────────────────────────────────┐
│                                                              │
│                      FUTURE ROADMAP                          │
│                                                              │
│                                                              │
│    NOW ────────────────────────────────────────► FUTURE     │
│                                                              │
│    ✅ 4 Agents          │  📋 Agent Memory                  │
│    ✅ Webex Bot         │  📋 Streaming Responses           │
│    ✅ Observability     │  📋 Multi-turn Conversations      │
│    ✅ Docker Stack      │  📋 Dynamic Agent Discovery       │
│                         │  📋 Kubernetes Deployment         │
│                         │  📋 A/B Testing Agents            │
│                                                              │
│                                                              │
│         "The foundation is solid - ready to scale"          │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

**Speaker Notes:**
- "The architecture supports future enhancements"
- "Each agent can be improved independently"

---

# SLIDE 12: Thank You

```
┌─────────────────────────────────────────────────────────────┐
│                                                              │
│                      THANK YOU                               │
│                                                              │
│                                                              │
│                     AGENTSWARM                               │
│          Multi-Agent AI for Enterprise Support               │
│                                                              │
│                                                              │
│                    ┌─────────────┐                          │
│                    │  QUESTIONS? │                          │
│                    └─────────────┘                          │
│                                                              │
│                                                              │
│              [Your Name] • [Your Email]                      │
│                                                              │
│                                                              │
│    GitHub: github4-chn.cisco.com/rguvvala/coffeeAgentify    │
│                                                              │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

**Speaker Notes:**
- "Happy to answer questions"
- "Code is available if you want to explore"

---

# BACKUP SLIDES

## Backup: Agent Selection Logic

```
┌─────────────────────────────────────────────────────────────┐
│                                                              │
│              SUPERVISOR AGENT SELECTION RULES                │
│                                                              │
│    IF query mentions:              THEN include:            │
│    ─────────────────────────────────────────────            │
│    customer ID, order number   →   CRM Agent                │
│    troubleshooting, how-to     →   Knowledge Agent          │
│    create ticket, track issue  →   Ticket Agent             │
│    urgent, critical, VIP       →   Escalation Agent         │
│    complex scenario            →   All 4 Agents             │
│    simple greeting             →   General Response         │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## Backup: Error Handling

```
┌─────────────────────────────────────────────────────────────┐
│                                                              │
│                    ERROR HANDLING                            │
│                                                              │
│    Agent Offline    →   Graceful degradation                │
│    Agent Timeout    →   30 second limit, retry once         │
│    LLM Error        →   Fallback response                   │
│    All Agents Down  →   "Please try again" message          │
│                                                              │
│    Every error is:                                          │
│    • Logged with full context                               │
│    • Traced in Jaeger                                       │
│    • Counted in metrics                                     │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

*Presentation Template v1.0*
