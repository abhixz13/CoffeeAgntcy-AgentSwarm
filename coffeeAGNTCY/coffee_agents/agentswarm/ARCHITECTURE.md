# AgentSwarm Architecture Documentation

## Project Overview

**AgentSwarm** is a multi-agent AI system for Webex Contact Center, built on Cisco's AGNTCY framework and extending CoffeeAgentcy patterns.

**Purpose:** Demonstrate how multiple specialized AI agents can collaborate to handle customer support queries more effectively than a single agent.

**Hackathon:** Webex Playtime FY26

---

## System Architecture

### High-Level View

```
                              CUSTOMER
                                 |
                    +------------+------------+
                    |                         |
                    v                         v
              [Webex Chat]              [Direct API]
                    |                         |
                    v                         v
            +---------------+         +---------------+
            |  WEBEX BOT    |         |   curl/HTTP   |
            |  (port 5000)  |         |               |
            +-------+-------+         +-------+-------+
                    |                         |
                    +------------+------------+
                                 |
                                 v
                    +------------------------+
                    |     ORCHESTRATOR       |
                    |      (port 8000)       |
                    |                        |
                    |  - Intent Detection    |
                    |  - Agent Routing       |
                    |  - Response Aggregation|
                    +------------------------+
                      /     |      |      \
                     /      |      |       \
                    v       v      v        v
            +--------+ +--------+ +--------+ +----------+
            |KNOWLEDGE| |  CRM   | | TICKET | |ESCALATION|
            | :8001  | | :8002  | | :8003  | |  :8004   |
            +--------+ +--------+ +--------+ +----------+
            |        | |        | |        | |          |
            | FAQ    | |Customer| | Create | | Route to |
            | Answers| | Data   | | Track  | | Human    |
            +--------+ +--------+ +--------+ +----------+
```

### Component Details

#### 1. Orchestrator Agent (Supervisor)
- **Port:** 8000
- **Role:** Central coordinator that routes queries to appropriate specialists
- **Technology:** LangGraph StateGraph, FastAPI
- **Key Functions:**
  - Intent classification (faq, customer_lookup, ticket, escalation, general)
  - Parallel agent coordination
  - Response aggregation

#### 2. Knowledge Agent
- **Port:** 8001
- **Role:** Answers FAQs and provides troubleshooting steps
- **Data:** Simulated knowledge base (hardcoded for demo)
- **Skills:** `get_faq_answer`

#### 3. CRM Agent
- **Port:** 8002
- **Role:** Fetches customer information and history
- **Data:** Simulated customer database
- **Skills:** `get_customer_info`

#### 4. Ticket Agent
- **Port:** 8003
- **Role:** Creates and tracks support tickets
- **Data:** Simulated ticket system
- **Skills:** `create_support_ticket`

#### 5. Escalation Agent
- **Port:** 8004
- **Role:** Determines if human intervention is needed
- **Logic:** Keyword detection, sentiment analysis
- **Skills:** `escalate_to_human`

#### 6. Webex Bot
- **Port:** 5000
- **Role:** Interface between Webex and AgentSwarm
- **Technology:** FastAPI, Webex APIs
- **Webhook:** Receives messages, calls Orchestrator, sends responses

---

## Data Flow

### Request Flow
```
1. Customer sends message in Webex
2. Webex Cloud sends webhook to Bot (port 5000)
3. Bot extracts message text
4. Bot calls Orchestrator API (port 8000)
5. Orchestrator classifies intent
6. Orchestrator routes to appropriate agent(s)
7. Specialist agent(s) process and respond
8. Orchestrator aggregates responses
9. Bot sends formatted response to Webex
10. Customer sees response in chat
```

### Intent Classification
```
Query                              → Intent           → Agent(s)
─────────────────────────────────────────────────────────────────
"How do I reset my password?"      → faq              → Knowledge
"Check order #12345"               → customer_lookup  → CRM
"Create a ticket for network"      → ticket           → Ticket
"URGENT: System down!"             → escalation       → Escalation
"Hello!"                           → general          → (Direct response)
```

---

## Technology Stack

### Core Framework
| Component | Version | Purpose |
|-----------|---------|---------|
| AGNTCY App SDK | 0.4.5 | Agent framework |
| LangGraph | >=0.4.1 | Workflow orchestration |
| LangChain | >=0.3.27 | LLM integration |
| FastAPI | >=0.115 | HTTP servers |
| LiteLLM | 1.75.3 | Unified LLM interface |

### LLM Provider
- **Primary:** OpenAI GPT-4o-mini
- **Alternative:** GROQ (free tier)
- **Interface:** LiteLLM for provider abstraction

### Communication
- **Mode:** HTTP (simplified for hackathon)
- **Alternative:** SLIM/A2A Protocol (production)

### Observability (Optional)
- OpenTelemetry for tracing
- Grafana for dashboards
- ClickHouse for storage

---

## File Structure

```
agentswarm/
├── agents/
│   ├── orchestrator/
│   │   ├── __init__.py
│   │   ├── main.py           # FastAPI server
│   │   ├── graph.py          # LangGraph workflow
│   │   ├── http_client.py    # HTTP client for agents
│   │   ├── models.py         # Pydantic models
│   │   └── tools.py          # A2A tools (not used in HTTP mode)
│   │
│   ├── knowledge/
│   │   ├── __init__.py
│   │   ├── agent.py          # Agent logic
│   │   ├── server.py         # HTTP server
│   │   ├── card.py           # Agent card
│   │   └── agent_executor.py # A2A executor (not used)
│   │
│   ├── crm/
│   │   └── (same structure)
│   │
│   ├── ticket/
│   │   └── (same structure)
│   │
│   └── escalation/
│       └── (same structure)
│
├── webex/
│   ├── __init__.py
│   └── bot.py                # Webex bot integration
│
├── config/
│   ├── __init__.py
│   ├── config.py             # Environment config
│   └── logging_config.py     # Logging setup
│
├── common/
│   ├── __init__.py
│   └── llm.py                # LLM utilities
│
├── .env                      # Environment variables (gitignored)
├── env.example               # Environment template
├── pyproject.toml            # Dependencies
├── ARCHITECTURE.md           # This file
├── DECISIONS.md              # Design decisions
├── WEBEX_DEMO_GUIDE.md       # Demo instructions
└── README.md                 # Project overview
```

---

## API Endpoints

### Orchestrator (8000)
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/agent/prompt` | Process customer query |
| GET | `/health` | Health check |
| GET | `/` | Service info |

### Specialist Agents (8001-8004)
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/process` | Process specific request |
| GET | `/health` | Health check |
| GET | `/` | Agent info |

### Webex Bot (5000)
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/webhook` | Webex webhook receiver |
| GET | `/health` | Health check |
| GET | `/` | Bot info |

---

## Configuration

### Environment Variables (.env)

```bash
# LLM Configuration
LLM_MODEL=openai/gpt-4o-mini
OPENAI_API_KEY=sk-...

# Agent Ports
ORCHESTRATOR_PORT=8000
KNOWLEDGE_AGENT_PORT=8001
CRM_AGENT_PORT=8002
TICKET_AGENT_PORT=8003
ESCALATION_AGENT_PORT=8004

# Webex Configuration
WEBEX_BOT_TOKEN=NDc4...

# Logging
LOGGING_LEVEL=INFO
```

---

## Deployment Options

### Option 1: Local Development (Current)
- All agents run locally as Python processes
- HTTP communication between agents
- Webex bot exposed via ngrok

### Option 2: Docker Compose
- All agents in containers
- SLIM message transport
- Full observability stack

### Option 3: Kubernetes
- Production deployment
- Helm charts available in CoffeeAgentcy
- Scalable architecture

---

## Security Considerations

### Current (Demo)
- No authentication between agents
- API keys in .env file
- Local network only

### Production Recommendations
- Enable AGNTCY Identity Service
- Use TBAC (Tool-Based Access Control)
- Encrypt inter-agent communication
- Rotate API keys regularly

---

## Related Documentation

- [CoffeeAgentcy](https://github.com/agntcy/coffeeAgntcy)
- [AGNTCY Framework](https://docs.agntcy.org/)
- [Webex APIs](https://developer.webex.com/)
- [LangGraph](https://langchain-ai.github.io/langgraph/)

