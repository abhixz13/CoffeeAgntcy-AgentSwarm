# AgentSwarm Architecture Deep Dive
## Technical Documentation for Multi-Agent AI System

---

## 1. System Overview

### 1.1 What is AgentSwarm?

AgentSwarm is an enterprise-grade **Multi-Agent AI System** designed for Webex Contact Center. It demonstrates how multiple specialized AI agents can collaborate to handle complex customer support scenarios.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         AGENTSWARM ARCHITECTURE                          │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│    ┌──────────────┐                                                     │
│    │   Customer   │                                                     │
│    │   (Webex)    │                                                     │
│    └──────┬───────┘                                                     │
│           │                                                              │
│           ▼                                                              │
│    ┌──────────────┐         ┌─────────────────────────────────────┐    │
│    │  Webex Bot   │         │         OBSERVABILITY LAYER          │    │
│    │   Gateway    │         │  ┌─────────┐ ┌────────┐ ┌─────────┐ │    │
│    └──────┬───────┘         │  │ Jaeger  │ │Grafana │ │Promethe.│ │    │
│           │                  │  │ Traces  │ │Metrics │ │  Store  │ │    │
│           ▼                  │  └─────────┘ └────────┘ └─────────┘ │    │
│    ┌──────────────┐         └─────────────────────────────────────┘    │
│    │ ORCHESTRATOR │◄──────────────── OpenTelemetry ────────────────    │
│    │  (LangGraph) │                                                     │
│    └──────┬───────┘                                                     │
│           │                                                              │
│    ┌──────┴──────────────────────────────────────┐                     │
│    │              SUPERVISOR NODE                 │                     │
│    │         (Intent Classification)              │                     │
│    └──────┬──────────────────────────────────────┘                     │
│           │                                                              │
│    ┌──────┼──────────────────────────────────────┐                     │
│    │      │     SPECIALIST AGENTS                 │                     │
│    │      │                                       │                     │
│    │  ┌───▼───┐ ┌───────┐ ┌───────┐ ┌─────────┐ │                     │
│    │  │  CRM  │ │KNOWL- │ │TICKET │ │ESCALAT- │ │                     │
│    │  │ Agent │ │EDGE   │ │ Agent │ │  ION    │ │                     │
│    │  │:8002  │ │:8001  │ │:8003  │ │ :8004   │ │                     │
│    │  └───┬───┘ └───┬───┘ └───┬───┘ └────┬────┘ │                     │
│    │      │         │         │          │       │                     │
│    └──────┼─────────┼─────────┼──────────┼───────┘                     │
│           │         │         │          │                              │
│    ┌──────┴─────────┴─────────┴──────────┴───────┐                     │
│    │              AGGREGATOR NODE                 │                     │
│    │        (Response Synthesis)                  │                     │
│    └──────────────────┬──────────────────────────┘                     │
│                       │                                                  │
│                       ▼                                                  │
│              ┌─────────────────┐                                        │
│              │ Unified Response │                                        │
│              │   to Customer    │                                        │
│              └─────────────────┘                                        │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

### 1.2 Key Components

| Component | Technology | Purpose |
|-----------|------------|---------|
| **Orchestrator** | LangGraph | Coordinates agent collaboration |
| **Supervisor** | LLM (CIRCUIT) | Classifies intent, selects agents |
| **Specialist Agents** | FastAPI + LLM | Domain-specific processing |
| **Aggregator** | LLM (CIRCUIT) | Synthesizes unified response |
| **Observability** | OpenTelemetry | Distributed tracing & metrics |
| **Interface** | Webex Bot | Enterprise communication |

---

## 2. Agent Specifications

### 2.1 Knowledge Agent (Port 8001)

**Purpose:** Technical documentation, FAQs, troubleshooting guides

**Capabilities:**
- Password reset procedures
- Network troubleshooting steps
- Router configuration guides
- VPN setup instructions
- Email configuration help

**Prompt Template:**
```
You are a knowledgeable technical support agent with access 
to a comprehensive knowledge base.

Customer Question: {user_message}

Provide a helpful, accurate answer including:
1. Direct solution or answer
2. Step-by-step troubleshooting if applicable
3. Any relevant tips or warnings
```

### 2.2 CRM Agent (Port 8002)

**Purpose:** Customer information, account history, subscription tiers

**Capabilities:**
- Customer lookup by ID/order number
- Subscription tier identification
- Recent issue history
- Priority level assessment
- Account age and status

**Data Model:**
```python
Customer:
  - customer_id: str
  - name: str
  - subscription_tier: Standard | Premium | Enterprise
  - account_since: date
  - recent_issues: List[Issue]
  - priority_level: Standard | Priority | VIP
```

### 2.3 Ticket Agent (Port 8003)

**Purpose:** Support ticket creation and management

**Capabilities:**
- Create new tickets
- Assign priority levels
- Categorize issues
- Estimate resolution time
- Track ticket status

**Priority Matrix:**
| Priority | Criteria | Resolution Time |
|----------|----------|-----------------|
| Critical | System down, security breach, VIP major | 15 minutes |
| High | Service degraded, premium customer | 4 hours |
| Medium | Single user, workaround available | 24 hours |
| Low | Enhancement, general inquiry | 72 hours |

### 2.4 Escalation Agent (Port 8004)

**Purpose:** Urgent issue routing and human handoff

**Capabilities:**
- Escalation level assessment
- Team routing decisions
- Human intervention triggers
- SLA enforcement
- VIP handling

**Routing Teams:**
| Team | Handles |
|------|---------|
| Network Engineering | Connectivity, infrastructure, outages |
| Security Team | Security incidents, breaches |
| Senior Support | Complex technical, VIP customers |
| Billing Department | Payment issues, refunds |
| Product Team | Feature requests, bugs |

---

## 3. LangGraph Workflow

### 3.1 State Machine

```python
class OrchestratorState(TypedDict):
    messages: List[BaseMessage]
    intent: str
    agents_to_call: List[str]
    agents_called: List[str]
    execution_trace: List[Dict]
    agent_communications: List[str]
    total_time: float
    knowledge_response: str
    crm_response: str
    ticket_response: str
    escalation_response: str
    final_response: str
```

### 3.2 Graph Structure

```
                    ┌─────────────┐
                    │   START     │
                    └──────┬──────┘
                           │
                           ▼
                    ┌─────────────┐
                    │ SUPERVISOR  │
                    │   NODE      │
                    └──────┬──────┘
                           │
              ┌────────────┼────────────┐
              │            │            │
              ▼            ▼            ▼
        ┌─────────┐  ┌──────────┐  ┌─────────┐
        │ GENERAL │  │  MULTI   │  │  ERROR  │
        │  NODE   │  │  AGENT   │  │ HANDLER │
        └────┬────┘  │ EXECUTOR │  └────┬────┘
             │       └─────┬────┘       │
             │             │            │
             │             ▼            │
             │       ┌──────────┐       │
             │       │AGGREGATOR│       │
             │       │   NODE   │       │
             │       └─────┬────┘       │
             │             │            │
             └─────────────┼────────────┘
                           │
                           ▼
                    ┌─────────────┐
                    │    END      │
                    └─────────────┘
```

### 3.3 Conditional Routing

```python
def _route_based_on_intent(state: OrchestratorState) -> str:
    """
    Routes based on supervisor's intent classification:
    - "general" → General greeting response
    - "multi_agent" → Execute multiple specialist agents
    """
    intent = state.get("intent", "general")
    return intent
```

---

## 4. Communication Patterns

### 4.1 HTTP-Based Agent Communication

```
┌────────────┐     HTTP POST      ┌────────────┐
│Orchestrator│ ─────────────────► │  Agent     │
│            │  /process          │  Server    │
│            │  {"prompt": "..."}│            │
│            │ ◄───────────────── │            │
│            │  {"response":"..."}│            │
└────────────┘                    └────────────┘
```

### 4.2 Request/Response Format

**Request:**
```json
{
  "prompt": "Customer query with context..."
}
```

**Response:**
```json
{
  "response": "Agent's processed response..."
}
```

### 4.3 Context Passing Between Agents

```python
# CRM response informs Ticket priority
if responses.get("crm_response"):
    context += f"\nCustomer Context: {responses['crm_response'][:300]}"

# Ticket info informs Escalation
if responses.get("ticket_response"):
    context += f"\nTicket Info: {responses['ticket_response'][:300]}"
```

---

## 5. Observability Architecture

### 5.1 Tracing Flow

```
┌─────────────────────────────────────────────────────────────┐
│                    DISTRIBUTED TRACE                         │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  trace_id: abc123                                           │
│  ├── span: orchestrator.run (parent)                        │
│  │   ├── span: supervisor.analyze                           │
│  │   ├── span: crm.process                                  │
│  │   │   └── span: llm.invoke                               │
│  │   ├── span: knowledge.process                            │
│  │   │   └── span: llm.invoke                               │
│  │   ├── span: ticket.process                               │
│  │   │   └── span: llm.invoke                               │
│  │   ├── span: escalation.process                           │
│  │   │   └── span: llm.invoke                               │
│  │   └── span: aggregator.synthesize                        │
│  │       └── span: llm.invoke                               │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### 5.2 Metrics Collected

| Metric | Type | Description |
|--------|------|-------------|
| `agentswarm.requests` | Counter | Total requests processed |
| `agentswarm.agent.duration` | Histogram | Agent call latency |
| `agentswarm.llm.tokens` | Counter | LLM token usage |
| `agentswarm.agent.errors` | Counter | Error count per agent |

### 5.3 Observability Stack

```yaml
# docker-compose.observability.yaml
services:
  jaeger:        # Trace visualization
  otel-collector: # Telemetry pipeline
  prometheus:    # Metrics storage
  grafana:       # Dashboards
```

---

## 6. LLM Integration

### 6.1 Cisco CIRCUIT API

```python
class CircuitChatModel(BaseChatModel):
    """
    LangChain-compatible wrapper for Cisco CIRCUIT API.
    
    Features:
    - OAuth2 authentication
    - Token caching
    - Automatic refresh
    - Rate limit handling
    """
    
    def _generate(self, messages, stop, run_manager, **kwargs):
        # Convert to CIRCUIT format
        # Call API
        # Return LangChain response
```

### 6.2 Model Configuration

```python
# config.py
AI_BACKEND = "circuit"  # or "litellm"
CIRCUIT_MODEL = "gpt-4o-mini"  # Free tier
```

### 6.3 Fallback Strategy

```python
def get_llm():
    if AI_BACKEND == "circuit":
        if is_circuit_available():
            return CircuitChatModel()
    # Fallback to LiteLLM
    return ChatLiteLLM(model=LLM_MODEL)
```

---

## 7. Webex Integration

### 7.1 Bot Gateway Architecture

```
┌─────────────┐    RabbitMQ     ┌─────────────┐
│   Webex     │ ──────────────► │    Bot      │
│   Cloud     │   Bot Queue     │   Gateway   │
│             │ ◄────────────── │             │
└─────────────┘    Response     └──────┬──────┘
                                       │
                                       ▼ HTTP
                                ┌─────────────┐
                                │Orchestrator │
                                └─────────────┘
```

### 7.2 Message Flow

1. User sends message in Webex
2. Cisco Bot Gateway queues message (RabbitMQ)
3. Bot Gateway consumes message
4. Forwards to Orchestrator via HTTP
5. Orchestrator coordinates agents
6. Response sent back to Webex

---

## 8. Security Considerations

### 8.1 Authentication

- **CIRCUIT API:** OAuth2 with client credentials
- **Webex Bot:** Bot token authentication
- **Internal APIs:** No auth (demo mode)

### 8.2 Data Handling

- Customer IDs are simulated
- No real PII in demo
- Traces may contain query content

### 8.3 Production Recommendations

- Add API authentication between agents
- Encrypt sensitive data in traces
- Implement rate limiting
- Add input validation

---

## 9. Scalability Patterns

### 9.1 Horizontal Scaling

```
                    Load Balancer
                         │
         ┌───────────────┼───────────────┐
         │               │               │
         ▼               ▼               ▼
    ┌─────────┐    ┌─────────┐    ┌─────────┐
    │ Agent   │    │ Agent   │    │ Agent   │
    │Instance1│    │Instance2│    │Instance3│
    └─────────┘    └─────────┘    └─────────┘
```

### 9.2 Agent Independence

Each agent is:
- Stateless
- Independently deployable
- Horizontally scalable
- Self-contained

### 9.3 Bottleneck Mitigation

| Bottleneck | Solution |
|------------|----------|
| LLM latency | Caching, streaming |
| Agent startup | Connection pooling |
| Trace volume | Sampling |

---

## 10. Future Enhancements

### 10.1 Planned Features

- [ ] Agent memory/context persistence
- [ ] Streaming responses
- [ ] Multi-turn conversations
- [ ] Agent-to-agent direct communication
- [ ] Dynamic agent discovery

### 10.2 Production Readiness

- [ ] Kubernetes deployment
- [ ] CI/CD pipeline
- [ ] Load testing
- [ ] Chaos engineering
- [ ] SLA monitoring

---

*Document Version: 1.0*
*Last Updated: January 2026*
