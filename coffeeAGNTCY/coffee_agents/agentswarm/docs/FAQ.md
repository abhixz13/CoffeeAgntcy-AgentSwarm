# AgentSwarm FAQ
## Frequently Asked Questions

---

## General Questions

### Q: What is AgentSwarm?
**A:** AgentSwarm is a multi-agent AI system designed for Webex Contact Center. It uses 4 specialist AI agents (Knowledge, CRM, Ticket, Escalation) that collaborate to handle customer support requests. Unlike a single LLM chatbot, AgentSwarm can access customer data, create tickets, and make escalation decisions.

### Q: Why use multiple agents instead of one LLM?
**A:** A single LLM can only provide generic responses. Multiple specialist agents can:
- Access different data sources (CRM, knowledge base)
- Perform actions (create tickets, escalate)
- Apply domain-specific logic
- Be updated independently
- Scale horizontally

### Q: What makes this different from ChatGPT?
**A:** ChatGPT is a single model that generates text. AgentSwarm is a **system** that:
- Coordinates multiple AI agents
- Integrates with enterprise systems (Webex, CRM)
- Has full observability (you can trace every request)
- Makes decisions about which agents to involve
- Synthesizes responses from multiple sources

---

## Technical Questions

### Q: What framework does AgentSwarm use?
**A:** AgentSwarm is built on:
- **AGNTCY Framework** (Cisco Outshift) - Multi-agent infrastructure
- **LangGraph** - State machine for agent orchestration
- **OpenTelemetry** - Distributed tracing
- **FastAPI** - HTTP APIs for each agent
- **Cisco CIRCUIT** - LLM backend

### Q: How does the Orchestrator decide which agents to call?
**A:** The Supervisor node uses an LLM to classify the user's intent and select appropriate agents based on rules:
- Customer ID mentioned → CRM Agent
- Troubleshooting needed → Knowledge Agent
- Ticket request → Ticket Agent
- Urgent/Critical → Escalation Agent

### Q: How do agents communicate?
**A:** Agents communicate via HTTP REST APIs. Each agent runs as an independent FastAPI server on its own port:
- Knowledge: 8001
- CRM: 8002
- Ticket: 8003
- Escalation: 8004
- Orchestrator: 8000

### Q: Is this stateless or stateful?
**A:** Currently stateless - each request is independent. Future versions could add:
- Conversation memory
- Session persistence
- User context caching

### Q: How is context shared between agents?
**A:** The Orchestrator passes relevant context from earlier agents to later ones. For example:
- CRM response is passed to Ticket Agent (for priority)
- Ticket info is passed to Escalation Agent (for routing)

---

## Observability Questions

### Q: What is distributed tracing?
**A:** Distributed tracing tracks a request as it flows through multiple services. Each operation creates a "span" with timing information. All spans share a "trace ID" so you can see the complete request flow.

### Q: Why use Jaeger?
**A:** Jaeger is an open-source distributed tracing system that:
- Visualizes traces as waterfall diagrams
- Shows timing for each operation
- Helps identify bottlenecks
- Is the industry standard (CNCF project)

### Q: What metrics are collected?
**A:** AgentSwarm collects:
- Request count
- Agent call duration (histogram)
- LLM token usage
- Error counts per agent

### Q: Can I use Datadog/New Relic instead?
**A:** Yes! AgentSwarm uses OpenTelemetry, which is vendor-neutral. You can export traces and metrics to any OTLP-compatible backend including Datadog, New Relic, Splunk, etc.

---

## Integration Questions

### Q: How does Webex integration work?
**A:** AgentSwarm uses Cisco's Bot Gateway:
1. User sends message in Webex
2. Message queued in RabbitMQ
3. Bot Gateway consumes message
4. Forwards to Orchestrator via HTTP
5. Response sent back to Webex

### Q: Can I use a different chat interface?
**A:** Yes! The Orchestrator exposes a REST API (`POST /agent/prompt`). You can integrate with:
- Slack
- Microsoft Teams
- Custom web chat
- Mobile apps

### Q: What LLM does it use?
**A:** AgentSwarm supports:
- **Cisco CIRCUIT API** (default) - Free for Cisco employees
- **OpenAI** via LiteLLM
- **GROQ** via LiteLLM
- Any LiteLLM-supported provider

---

## Performance Questions

### Q: How fast is it?
**A:** Typical response times:
- Simple query (2 agents): 3-5 seconds
- Complex query (4 agents): 8-12 seconds
- Most time is spent in LLM calls

### Q: What are the bottlenecks?
**A:** Primary bottlenecks:
1. LLM inference time (~2-4s per call)
2. Sequential agent calls (could be parallelized)
3. Network latency between services

### Q: How can it be optimized?
**A:** Optimization strategies:
- Parallel agent calls where possible
- LLM response caching
- Streaming responses
- Smaller/faster models for simple tasks

### Q: Can it scale?
**A:** Yes! Each agent is:
- Stateless
- Independently deployable
- Horizontally scalable
- Container-ready (Docker/Kubernetes)

---

## Development Questions

### Q: How do I add a new agent?
**A:** To add a new agent:
1. Create agent folder in `agents/`
2. Implement `agent.py` with process logic
3. Create `server.py` with FastAPI endpoint
4. Add port to `config.py`
5. Update Orchestrator to call new agent

### Q: How do I modify agent behavior?
**A:** Each agent has a prompt template in `agent.py`. Modify the template to change behavior. No code changes needed for prompt adjustments.

### Q: How do I test locally?
**A:** 
```powershell
# Start all services
.\demo_start.ps1

# Send test request
Invoke-RestMethod -Uri "http://localhost:8000/agent/prompt" `
  -Method POST -ContentType "application/json" `
  -Body '{"prompt": "Test query"}'
```

### Q: How do I debug issues?
**A:** 
1. Check agent terminal windows for errors
2. View traces in Jaeger (http://localhost:16686)
3. Check debug log: `.cursor/debug.log`
4. Run `.\demo_status.ps1` to check services

---

## Deployment Questions

### Q: What are the system requirements?
**A:** 
- Python 3.11+
- Docker Desktop
- 8GB RAM minimum
- VPN (for CIRCUIT API)

### Q: Can it run in production?
**A:** The current version is demo-ready. For production:
- Add authentication between services
- Implement rate limiting
- Add input validation
- Set up proper logging
- Configure alerting
- Use Kubernetes for orchestration

### Q: How do I deploy to Kubernetes?
**A:** Each agent can be deployed as a separate Kubernetes Deployment with a Service. Use the existing Docker setup as a starting point.

---

## Troubleshooting

### Q: Agents won't start - port in use
**A:** 
```powershell
# Find process using port
netstat -ano | findstr "8001"

# Kill process
taskkill /PID <PID> /F
```

### Q: No traces in Jaeger
**A:**
1. Ensure Docker containers are running: `docker ps`
2. Send a test request
3. Wait 5 seconds
4. Click "Find Traces" in Jaeger

### Q: Bot not responding in Webex
**A:**
1. Check bot gateway terminal for errors
2. Verify BOT_QUEUE_NAME in .env
3. Ensure VPN is connected
4. Restart bot gateway

### Q: LLM errors / rate limits
**A:**
- CIRCUIT: Check VPN connection, verify API keys
- OpenAI: Check API key, billing status
- GROQ: Check API key, rate limits

---

## Business Questions

### Q: What's the ROI of multi-agent AI?
**A:** Benefits include:
- Faster resolution times
- 24/7 availability
- Consistent responses
- Reduced human workload
- Full audit trail (observability)

### Q: How does it compare to traditional chatbots?
**A:** Traditional chatbots:
- Rule-based or single LLM
- Limited capabilities
- No system integration
- Black box (no observability)

AgentSwarm:
- Multiple specialist agents
- Full system integration
- Enterprise observability
- Extensible architecture

### Q: What's the cost?
**A:** 
- CIRCUIT API: Free for Cisco employees
- Infrastructure: Docker on any machine
- No per-seat licensing
- Open source components

---

*FAQ Version 1.0 - January 2026*
