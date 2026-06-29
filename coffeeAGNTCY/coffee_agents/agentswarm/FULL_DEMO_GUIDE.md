# AgentSwarm Full Demo Guide
## Enterprise Multi-Agent AI System with Observability

> **Demo Duration:** 15-20 minutes  
> **Audience:** Technical evaluators, hiring managers, AI/ML teams  
> **Key Focus:** Multi-Agent Orchestration + Production Observability

---

## 🎬 Demo Setup Checklist

### Prerequisites
- [ ] Docker Desktop running
- [ ] Python 3.11+ installed
- [ ] Webex Bot configured (BOT_QUEUE_NAME in .env)
- [ ] Cisco CIRCUIT API keys (or OpenAI/GROQ)

### Quick Setup Commands
```bash
cd coffeeAGNTCY/coffee_agents/agentswarm

# 1. Install dependencies (first time only)
pip install -e .

# 2. Start Docker observability stack
start_observability_stack.bat

# 3. Start all agents
start_demo.bat
```

---

## 📋 Demo Script (Step by Step)

### Part 1: Introduction (2 min)

**Say:**
> "I'm going to demonstrate AgentSwarm - a multi-agent AI system I built for Webex Contact Center. What makes this special is not just the AI agents, but the **enterprise-grade observability** that lets us monitor, debug, and optimize the system in production."

**Show:**
- Architecture diagram (from OBSERVABILITY_DEMO.md)
- List of 4 specialist agents

### Part 2: Start the System (2 min)

**Do:**
1. Run `start_observability_stack.bat`
2. Run `start_demo.bat` (say Y to dashboard)

**Show:**
- 6 terminal windows starting up
- Jaeger UI at http://localhost:16686
- Grafana at http://localhost:3001 (login: admin/admin)

**Say:**
> "I'm starting 4 specialist AI agents, an orchestrator, and a full observability stack with Jaeger for distributed tracing and Grafana for metrics."

### Part 3: Simple Query Demo (3 min)

**Send via Webex:**
```
Hi, I'm customer #67890 and I forgot my password
```

**Show in Jaeger:**
1. Go to http://localhost:16686
2. Select Service: `agentswarm`
3. Click "Find Traces"
4. Click on the trace to see waterfall

**Say:**
> "Watch how the request flows through the system. The Supervisor analyzes the intent, then calls the CRM Agent to look up customer info, and the Knowledge Agent to get password reset steps. Each operation is a 'span' in our distributed trace."

**Point out:**
- Trace ID (unique identifier)
- Span hierarchy (parent-child)
- Duration of each agent call
- Total request time

### Part 4: Complex Query Demo (4 min)

**Send via Webex:**
```
URGENT: I'm enterprise customer #11111, our entire office network is down affecting 50+ employees. We have a critical presentation in 2 hours!
```

**Show in Jaeger:**
1. Find the new trace
2. Show ALL 4 agents being called
3. Expand each span to show details

**Show in Grafana:**
1. Open AgentSwarm Overview dashboard
2. Point out metrics updating in real-time
3. Show agent call counts increasing
4. Show latency graph

**Say:**
> "This urgent query triggered ALL 4 agents to collaborate. The CRM Agent identified them as an Enterprise VIP customer. The Knowledge Agent provided troubleshooting steps. The Ticket Agent created a CRITICAL priority ticket. And the Escalation Agent routed it to a Network Engineer immediately."

**Point out:**
- Multi-agent collaboration
- Context passing between agents
- Priority escalation logic
- Real-time metrics

### Part 5: Observability Deep Dive (4 min)

**Show Jaeger Features:**
1. **Compare Traces** - Compare two different requests
2. **Service Dependencies** - Show agent relationships
3. **Span Details** - Click on a span, show attributes

**Show Grafana Features:**
1. **Agent Latency Graph** - Which agent is slowest?
2. **Calls per Minute** - Traffic patterns
3. **Error Rates** - (hopefully zero!)

**Say:**
> "In production, this observability is critical. If a customer reports a slow response, I can find their exact trace, see which agent was slow, and drill down to the specific LLM call. I can also set up alerts if latency exceeds thresholds."

### Part 6: Architecture Walkthrough (3 min)

**Show code briefly:**
- `common/observability.py` - Tracing module
- `agents/orchestrator/graph.py` - LangGraph workflow
- `docker-compose.observability.yaml` - Infrastructure

**Say:**
> "The system uses OpenTelemetry, which is the industry standard for observability. Traces export to Jaeger, metrics go to Prometheus and Grafana. This same setup works with Datadog, New Relic, or any OTLP-compatible backend."

### Part 7: Q&A Prep

**Anticipated Questions:**

**Q: "How do you handle agent failures?"**
> "Each agent call has timeout handling and error recording. Failed calls are logged with full context in the trace. The orchestrator can continue with partial results or return a graceful error."

**Q: "How do you scale this?"**
> "Each agent is a separate microservice. We can scale horizontally by running multiple instances behind a load balancer. The OTEL Collector handles telemetry aggregation."

**Q: "What about LLM costs?"**
> "We track token usage per agent. The metrics show input/output tokens, so we can attribute costs accurately and identify expensive operations."

**Q: "How is this different from a single LLM call?"**
> "A single LLM can't access real-time customer data, create tickets, or make escalation decisions. Our agents have specialized prompts, tools, and integrations. The orchestrator coordinates them intelligently based on intent."

---

## 🎯 Key Demo Messages

### For Technical Audience
1. **Distributed Tracing** - "Every request has a trace_id that follows it through all services"
2. **OpenTelemetry** - "Industry-standard, works with any backend"
3. **Production Ready** - "Error handling, timeouts, health checks"

### For Business Audience
1. **Cost Visibility** - "We track exactly how much each query costs"
2. **Debugging** - "When something goes wrong, we can find exactly why"
3. **Optimization** - "Metrics help us identify and fix bottlenecks"

### For AI/ML Audience
1. **LangGraph** - "State machine for multi-agent orchestration"
2. **Context Passing** - "Agents share information intelligently"
3. **Intent Classification** - "Supervisor decides which agents to involve"

---

## 📊 Demo URLs Quick Reference

| Service | URL | Purpose |
|---------|-----|---------|
| Jaeger | http://localhost:16686 | Trace visualization |
| Grafana | http://localhost:3001 | Metrics dashboard |
| Prometheus | http://localhost:9090 | Metrics storage |
| Custom Dashboard | http://localhost:8080 | Live agent status |
| Orchestrator | http://localhost:8000 | API endpoint |

---

## 🔧 Troubleshooting

### No traces appearing in Jaeger?
```bash
# Check OTEL Collector is running
docker ps | findstr otel

# Check .env has correct endpoint
OTLP_HTTP_ENDPOINT=http://localhost:4318
```

### Agents not starting?
```bash
# Check ports are free
netstat -ano | findstr "800"

# Kill existing processes
stop_demo.bat
```

### Webex bot not responding?
```bash
# Check bot gateway logs
# Look for RabbitMQ connection errors
# Verify BOT_QUEUE_NAME in .env
```

---

## 🏆 Demo Success Criteria

After this demo, the audience should understand:

1. ✅ How multiple AI agents collaborate on a single request
2. ✅ How distributed tracing works across services
3. ✅ How to debug and optimize multi-agent systems
4. ✅ Why observability is critical for production AI
5. ✅ The technical depth of the implementation

---

*Good luck with your demo! 🚀*
