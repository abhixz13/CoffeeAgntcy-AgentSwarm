# AgentSwarm Observability Demo
## Enterprise-Grade Multi-Agent System Monitoring

> **"If you can't observe it, you can't improve it."**
> 
> This demo showcases how to build **production-ready observability** for AI multi-agent systems using OpenTelemetry, distributed tracing, and real-time metrics.

---

## 🎯 Why This Matters (For Your Next Job Interview)

When building AI systems in production, observability is **not optional**. Here's what enterprises need:

| Challenge | Our Solution |
|-----------|--------------|
| "Which agent is slow?" | Per-agent latency metrics & histograms |
| "Why did this request fail?" | Distributed tracing with span context |
| "How much is AI costing us?" | LLM token tracking & cost attribution |
| "Is the system healthy?" | Real-time health dashboards |
| "What happened at 3am?" | Trace correlation & event logging |

---

## 🏗️ Architecture: Observability Stack

```
┌─────────────────────────────────────────────────────────────────┐
│                    AGENTSWARM OBSERVABILITY                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   ┌──────────────┐     ┌──────────────┐     ┌──────────────┐   │
│   │   Webex Bot  │────▶│ Orchestrator │────▶│  Specialist  │   │
│   │   Gateway    │     │   (Tracer)   │     │    Agents    │   │
│   └──────────────┘     └──────────────┘     └──────────────┘   │
│          │                    │                    │            │
│          ▼                    ▼                    ▼            │
│   ┌─────────────────────────────────────────────────────────┐  │
│   │              OBSERVABILITY LAYER                         │  │
│   │  ┌─────────────┐  ┌─────────────┐  ┌─────────────────┐  │  │
│   │  │ OpenTelemetry│  │   Metrics   │  │  Trace Store   │  │  │
│   │  │   Tracing   │  │  Collector  │  │  (In-Memory)   │  │  │
│   │  └─────────────┘  └─────────────┘  └─────────────────┘  │  │
│   └─────────────────────────────────────────────────────────┘  │
│                              │                                  │
│                              ▼                                  │
│   ┌─────────────────────────────────────────────────────────┐  │
│   │              VISUALIZATION LAYER                         │  │
│   │  ┌─────────────┐  ┌─────────────┐  ┌─────────────────┐  │  │
│   │  │  Dashboard  │  │  Waterfall  │  │  Agent Health   │  │  │
│   │  │   (Live)    │  │    View     │  │    Monitor      │  │  │
│   │  └─────────────┘  └─────────────┘  └─────────────────┘  │  │
│   └─────────────────────────────────────────────────────────┘  │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🔧 Key Observability Components

### 1. Distributed Tracing (OpenTelemetry)

Every request gets a **trace_id** that follows it through all agents:

```python
# From common/observability.py
@dataclass
class TraceContext:
    trace_id: str           # Unique identifier for this request
    session_id: str         # Session for grouping related requests
    user_query: str         # Original user input
    start_time: float       # Request start timestamp
    spans: List[SpanData]   # Individual operation spans
    agent_calls: List[Dict] # Inter-agent communication records
    llm_calls: List[Dict]   # LLM invocation tracking
```

**Why it matters:** When a customer reports "my request was slow", you can trace exactly which agent took how long.

### 2. Span Context Propagation

Context flows through the entire agent graph:

```
[User Request] 
    │
    ▼ trace_id=abc123
[Supervisor] ─── span: supervisor.analyze (150ms)
    │
    ├──▶ [CRM Agent] ─── span: crm.lookup (320ms)
    │         │
    │         └── span: llm.invoke (280ms)
    │
    ├──▶ [Knowledge Agent] ─── span: knowledge.search (180ms)
    │
    └──▶ [Ticket Agent] ─── span: ticket.create (250ms)
    │
    ▼
[Aggregator] ─── span: aggregator.synthesize (200ms)
    │
    ▼
[Response] ─── Total: 1100ms, 4 agents, 3 LLM calls
```

### 3. Metrics Collection

Real-time metrics for every component:

```python
# Automatically collected metrics:
- agentswarm.requests          # Total request count
- agentswarm.agent.duration    # Per-agent latency histogram
- agentswarm.llm.tokens        # Token usage (input/output)
- agentswarm.agent.errors      # Error rate per agent
```

### 4. Real-Time Dashboard

Live visualization at `http://localhost:8080`:

- **Request throughput** - How many queries/minute
- **Agent health** - Which agents are responding, which are slow
- **Latency waterfall** - Visual breakdown of each request
- **Token consumption** - LLM cost tracking

---

## 🚀 Running the Observability Demo

### Option A: Full Docker Stack (Recommended for Demo)

This gives you **Jaeger + Grafana + Prometheus** - enterprise-grade observability!

```bash
# Step 1: Start Docker observability stack
cd coffeeAGNTCY/coffee_agents/agentswarm
start_observability_stack.bat

# Step 2: Add to your .env file
OTLP_HTTP_ENDPOINT=http://localhost:4318

# Step 3: Start all agents
start_demo.bat
```

**Dashboards:**
| Service | URL | Credentials |
|---------|-----|-------------|
| **Jaeger** (Traces) | http://localhost:16686 | None |
| **Grafana** (Metrics) | http://localhost:3001 | admin/admin |
| **Prometheus** | http://localhost:9090 | None |

### Option B: Lightweight (No Docker)

Uses the built-in Python dashboard:

```bash
# Terminal 1: Start all agents
cd coffeeAGNTCY/coffee_agents/agentswarm
start_demo.bat

# Say "Y" when asked to start dashboard
```

**Dashboard:** http://localhost:8080

### Step 3: Send Test Queries

Send queries via Webex bot and watch the dashboards update in real-time!

**Demo Query 1 (2 agents):**
```
I'm customer #67890 and forgot my password
```

**Demo Query 2 (3 agents):**
```
Customer #12345 - internet slow for 3 days, please create ticket
```

**Demo Query 3 (ALL 4 agents):**
```
URGENT: Enterprise customer #11111, network down, 50 employees affected!
```

---

## 📊 What to Show in Demo

### 1. Distributed Trace View

Point out:
- **Trace ID** - Unique identifier linking all operations
- **Span hierarchy** - Parent-child relationships
- **Timing breakdown** - Where time was spent

### 2. Waterfall Visualization

Show:
- Sequential vs parallel execution
- Which agent is the bottleneck
- Total request latency

### 3. Agent Metrics

Highlight:
- Call counts per agent
- Average/P95 latencies
- Error rates

### 4. LLM Token Tracking

Demonstrate:
- Input vs output tokens
- Cost attribution per agent
- Token efficiency

---

## 💡 Key Talking Points for Interviews

### "How do you debug a slow AI agent?"

> "We use distributed tracing with OpenTelemetry. Every request gets a trace_id that follows it through all agents. I can see exactly which agent took how long, and drill down into individual LLM calls. The waterfall view shows bottlenecks instantly."

### "How do you monitor AI costs in production?"

> "We track LLM token usage at the agent level. Each agent's input/output tokens are recorded, so we can attribute costs accurately. The metrics collector aggregates this for dashboards and alerts."

### "How do you ensure reliability of multi-agent systems?"

> "We have health checks for each agent, error rate tracking, and latency histograms. If an agent's P95 latency spikes or error rate increases, we get alerted. The trace store keeps recent requests for debugging."

### "What observability standards do you follow?"

> "We use OpenTelemetry, which is the industry standard. Our traces and metrics are compatible with Jaeger, Grafana, Datadog, and any OTLP-compatible backend. We also integrate with AGNTCY's IOA Observe SDK for agent-specific insights."

---

## 🐳 Docker Observability Stack

### What's Included

```
┌─────────────────────────────────────────────────────────────┐
│                 DOCKER OBSERVABILITY STACK                   │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌─────────────────┐         ┌─────────────────┐           │
│  │  AgentSwarm     │  OTLP   │  OTEL Collector │           │
│  │  (Your Agents)  │────────▶│  :4317/:4318    │           │
│  └─────────────────┘         └────────┬────────┘           │
│                                       │                     │
│                    ┌──────────────────┼──────────────────┐ │
│                    │                  │                  │ │
│                    ▼                  ▼                  ▼ │
│           ┌────────────┐      ┌────────────┐     ┌──────┐ │
│           │   Jaeger   │      │ Prometheus │     │Grafana│ │
│           │   :16686   │      │   :9090    │     │ :3001 │ │
│           └────────────┘      └────────────┘     └──────┘ │
│                                                            │
└─────────────────────────────────────────────────────────────┘
```

### Quick Start

```bash
# Start the stack
start_observability_stack.bat

# Stop the stack
stop_observability_stack.bat
```

### Jaeger Features (Trace Visualization)

- **Service Map** - See how agents connect
- **Trace Timeline** - Waterfall view of each request
- **Span Details** - Drill into individual operations
- **Compare Traces** - Side-by-side comparison

### Grafana Features (Metrics Dashboard)

Pre-configured dashboard includes:
- Total requests counter
- Agent call counts
- Latency by agent type
- LLM token consumption
- Error rates

## 🔌 Integration with Production Systems

### Export to Jaeger/Grafana (Docker)

```bash
# Set OTLP endpoint in .env
OTLP_HTTP_ENDPOINT=http://localhost:4318
```

### Export to Datadog

```python
# In observability.py, add Datadog exporter
from opentelemetry.exporter.datadog import DatadogSpanExporter
```

### Export to ClickHouse (AGNTCY default)

```yaml
# otel-collector-config.yaml
exporters:
  clickhouse:
    endpoint: "tcp://clickhouse:9000"
```

---

## 📁 Files Reference

| File | Purpose |
|------|---------|
| `common/observability.py` | Core observability module |
| `observability_dashboard.py` | Real-time web dashboard |
| `agents/orchestrator/graph.py` | Trace context integration |
| `agents/orchestrator/http_client.py` | Agent call metrics |

---

## 🎓 What This Demonstrates

1. **OpenTelemetry Integration** - Industry-standard distributed tracing
2. **Metrics Collection** - Real-time performance monitoring
3. **Span Context Propagation** - Tracing across service boundaries
4. **Live Dashboards** - WebSocket-powered real-time updates
5. **Production Patterns** - Error handling, timeouts, health checks
6. **Cost Attribution** - LLM token tracking per agent

---

## 🏆 Why This Gets You Hired

> "I built an observability layer for a multi-agent AI system using OpenTelemetry. I can show you distributed traces across 4 specialist agents, real-time latency dashboards, and LLM token tracking for cost management. The system handles errors gracefully and provides debugging capabilities for production issues."

This demonstrates:
- **Systems thinking** - End-to-end observability design
- **Production readiness** - Real-world monitoring patterns
- **Industry standards** - OpenTelemetry, OTLP, metrics
- **AI/ML ops** - LLM-specific observability needs
- **Full-stack skills** - Backend tracing + frontend dashboard

---

*Built with AGNTCY Framework + Cisco CIRCUIT AI + OpenTelemetry*
