# AgentSwarm Glossary
## Terms and Definitions

---

## A

### A2A (Agent-to-Agent) Protocol
An open standard developed by AGNTCY for enabling interoperability between AI agents from different vendors and frameworks. Key components include:
- **Agent Card**: JSON manifest describing an agent's capabilities, skills, and endpoints
- **Message Format**: Standardized structure with `messageId`, `role`, and `parts` for agent communication
- **Task Protocol**: For longer-running operations with status tracking

The protocol enables agents built with different frameworks (LangChain, CrewAI, AutoGen) to discover and communicate with each other without custom integration code. In AgentSwarm, each agent defines an `AgentCard` in `card.py` using the `a2a-sdk` package.

### Aggregator
The final node in the LangGraph workflow that combines responses from all specialist agents into a unified response.

### Agent
An autonomous AI component with specific capabilities. In AgentSwarm, there are 4 specialist agents plus an orchestrator.

### AGNTCY
Cisco Outshift's multi-agent framework. Provides infrastructure for building and deploying multi-agent AI systems.

---

## C

### CIRCUIT API
Cisco's internal LLM API service. Provides access to models like GPT-4o-mini for Cisco employees.

### Context Passing
The practice of sharing information from one agent's response with subsequent agents to improve their responses.

### CRM Agent
Specialist agent responsible for customer relationship management - looking up customer data, subscription tiers, and history.

---

## D

### Distributed Tracing
Technique for tracking requests as they flow through multiple services. Each service adds a "span" to the trace.

### Docker
Container platform used to run the observability stack (Jaeger, Grafana, Prometheus).

---

## E

### Escalation Agent
Specialist agent responsible for assessing urgency and routing critical issues to human specialists.

### Execution Trace
Record of which agents were called, in what order, and how long each took.

---

## G

### Grafana
Open-source visualization platform for metrics and traces. Used for dashboards.

### Graph (LangGraph)
State machine that defines the flow of execution through different nodes (agents).

---

## H

### HTTP Client
Component that makes HTTP requests from the Orchestrator to specialist agents.

---

## I

### Intent Classification
Process of analyzing a user's query to determine their goal/intent. Performed by the Supervisor node.

### IOA Observe SDK
AGNTCY's observability SDK. Provides decorators for tracing agents and tools.

---

## J

### Jaeger
Open-source distributed tracing system. Visualizes traces as waterfall diagrams.

---

## K

### Knowledge Agent
Specialist agent responsible for technical documentation, FAQs, and troubleshooting guides.

---

## L

### LangGraph
Library for building stateful, multi-actor applications with LLMs. Used for orchestration.

### LangChain
Framework for building LLM applications. AgentSwarm uses LangChain for LLM interactions.

### LiteLLM
Unified interface for multiple LLM providers (OpenAI, Azure, GROQ, etc.).

### LLM (Large Language Model)
AI model trained on text data that can generate human-like responses. The "brain" of each agent.

---

## M

### Metrics
Quantitative measurements of system performance (request count, latency, errors).

### Multi-Agent System (MAS)
System where multiple AI agents collaborate to solve problems.

---

## N

### Node
A step in the LangGraph workflow. Examples: Supervisor, Aggregator, General.

---

## O

### Observability
Ability to understand a system's internal state by examining its outputs (logs, metrics, traces).

### OpenTelemetry (OTEL)
Vendor-neutral standard for collecting telemetry data (traces, metrics, logs).

### Orchestrator
Central component that coordinates the flow of requests through specialist agents.

### OTLP
OpenTelemetry Protocol. Standard format for transmitting telemetry data.

---

## P

### Prometheus
Open-source metrics storage and querying system.

### Prompt Template
Predefined text structure that guides an LLM's response. Each agent has its own template.

---

## R

### RabbitMQ
Message broker used by Cisco Bot Gateway for Webex message delivery.

---

## S

### Span
A single operation within a distributed trace. Has start time, duration, and attributes.

### Specialist Agent
An agent with domain-specific expertise (Knowledge, CRM, Ticket, Escalation).

### State
The current data being passed through the LangGraph workflow. Includes messages, responses, and metadata.

### Supervisor
The node that analyzes user queries and decides which agents to involve.

---

## T

### Ticket Agent
Specialist agent responsible for creating and managing support tickets.

### Trace
Complete record of a request's journey through the system, composed of multiple spans.

### Trace ID
Unique identifier that links all spans belonging to the same request.

---

## U

### Unified Response
The final response sent to the user, synthesized from all agent contributions.

---

## W

### Waterfall View
Visualization of a trace showing spans as horizontal bars on a timeline.

### Webex
Cisco's collaboration platform. AgentSwarm integrates via Webex Bot.

### Workflow
The defined sequence of steps (nodes) in a LangGraph application.

---

## Acronyms Quick Reference

| Acronym | Full Form |
|---------|-----------|
| A2A | Agent-to-Agent |
| API | Application Programming Interface |
| CRM | Customer Relationship Management |
| FAQ | Frequently Asked Questions |
| HTTP | Hypertext Transfer Protocol |
| LLM | Large Language Model |
| MAS | Multi-Agent System |
| OTEL | OpenTelemetry |
| OTLP | OpenTelemetry Protocol |
| REST | Representational State Transfer |
| SDK | Software Development Kit |
| SLA | Service Level Agreement |
| VIP | Very Important Person |

---

*Glossary Version 1.0*
