# AgentSwarm Design Decisions

## Document Purpose
This document captures all key architectural and implementation decisions made during the AgentSwarm project development. Reference this when resuming work or onboarding new contributors.

---

## Decision Log

### Decision 1: Project Foundation
**Date:** Day 1  
**Context:** Needed to build a multi-agent system for Webex Playtime FY26 hackathon  
**Decision:** Build on top of Cisco's AGNTCY framework and CoffeeAgentcy reference implementation  
**Rationale:**
- Aligns with Cisco's strategic direction
- Leverages proven patterns from CoffeeAgentcy
- Demonstrates internal adoption of Cisco technology
- Strong hackathon pitch: "Using Cisco's own tech for Cisco's products"

**Alternatives Considered:**
- Build from scratch (too time-consuming)
- Use AutoGen (not Cisco technology)
- Use CrewAI (not aligned with AGNTCY)

---

### Decision 2: Agent Architecture
**Date:** Day 1  
**Context:** How to structure the multi-agent system  
**Decision:** Supervisor pattern with 5 specialized agents
```
Orchestrator (Supervisor)
├── Knowledge Agent (FAQ)
├── CRM Agent (Customer data)
├── Ticket Agent (Support tickets)
└── Escalation Agent (Urgent routing)
```
**Rationale:**
- Clear separation of concerns
- Each agent has single responsibility
- Orchestrator handles routing logic
- Scalable - can add more agents later

**Alternatives Considered:**
- Peer-to-peer agents (harder to coordinate)
- Single monolithic agent (no collaboration demo)
- Hierarchical agents (too complex for demo)

---

### Decision 3: HTTP vs SLIM Transport
**Date:** Day 2  
**Context:** CoffeeAgentcy uses SLIM (requires Docker), but Docker setup adds complexity  
**Decision:** Use HTTP for inter-agent communication (simplified mode)  
**Rationale:**
- No Docker dependency
- Faster setup and testing
- Easier debugging
- Good enough for demo purposes
- Can upgrade to SLIM later if needed

**Alternatives Considered:**
- Full SLIM setup (requires Docker, more complex)
- NATS transport (still needs Docker)
- gRPC (overkill for demo)

**Trade-offs:**
- Lost: A2A protocol compliance, message persistence
- Gained: Simplicity, faster development, easier demo

---

### Decision 4: LLM Provider
**Date:** Day 2  
**Context:** Need LLM for agent intelligence  
**Decision:** Support multiple providers via LiteLLM, defaulting to OpenAI  
**Rationale:**
- User already had OpenAI API key
- LiteLLM provides unified interface
- Easy to switch providers if needed
- GROQ available as free backup

**Configuration:**
```
LLM_MODEL=openai/gpt-4o-mini  # Current
LLM_MODEL=groq/llama-3.3-70b-versatile  # Alternative
```

**Rate Limit Issue:** User hit OpenAI rate limit (100k TPM) during testing. Solution: wait or switch to GROQ.

---

### Decision 5: Webex Integration Approach
**Date:** Day 2  
**Context:** Demo needs to impress non-technical audience  
**Decision:** Build Webex bot for chat-based demo instead of curl commands  
**Rationale:**
- Visual, interactive demo
- Non-technical audience can understand
- Shows real-world use case
- More impressive than terminal output

**Implementation:**
- FastAPI webhook receiver
- Webex Bot SDK for messaging
- ngrok for local development exposure

---

### Decision 6: Skip Observability for Demo
**Date:** Day 2  
**Context:** Full observability requires Docker (ClickHouse, Grafana, OTel)  
**Decision:** Defer observability setup, focus on core functionality  
**Rationale:**
- Time constraint
- Core demo doesn't need dashboards
- Can mention observability as a feature without showing
- Docker complexity not worth it for hackathon

**Future Enhancement:** Add Docker Compose with observability stack for production demo.

---

### Decision 7: Simulated Data
**Date:** Day 1  
**Context:** Agents need data sources (KB, CRM, Tickets)  
**Decision:** Use simulated/hardcoded data in agent prompts  
**Rationale:**
- No external dependencies
- Consistent demo behavior
- Fast implementation
- Can replace with real APIs later

**Example (Knowledge Agent):**
```python
# Simulated knowledge base in prompt
Knowledge Base Context:
- Password Reset: Go to Settings > Account...
- Slow Internet: 1) Restart router...
```

---

### Decision 8: Intent Classification
**Date:** Day 1  
**Context:** Orchestrator needs to route queries to correct agents  
**Decision:** LLM-based intent classification with 5 categories  
**Rationale:**
- Flexible, handles natural language
- No need for ML training
- Easy to add new intents
- Proven pattern from CoffeeAgentcy

**Intent Categories:**
| Intent | Description | Target Agent |
|--------|-------------|--------------|
| faq | General questions | Knowledge |
| customer_lookup | Order/account queries | CRM |
| ticket | Ticket creation | Ticket |
| escalation | Urgent issues | Escalation |
| general | Greetings, unclear | Direct response |

---

### Decision 9: Single Agent Routing
**Date:** Day 2  
**Context:** Should Orchestrator call multiple agents in parallel?  
**Decision:** Route to single primary agent based on intent  
**Rationale:**
- Simpler implementation
- Clearer demo flow
- Avoids rate limit issues
- Can enhance later for multi-agent calls

**Future Enhancement:** Add parallel agent calls for complex queries.

---

### Decision 10: Port Assignment
**Date:** Day 1  
**Context:** Need consistent ports for all services  
**Decision:** Sequential ports starting from 8000  
```
8000 - Orchestrator
8001 - Knowledge Agent
8002 - CRM Agent
8003 - Ticket Agent
8004 - Escalation Agent
5000 - Webex Bot
```
**Rationale:**
- Easy to remember
- No conflicts with common services
- Matches typical development patterns

---

## Technical Constraints

### Rate Limits
- **OpenAI:** 100k TPM on user's plan
- **Mitigation:** Use GROQ for unlimited testing

### Windows Development
- PowerShell syntax differs from bash
- Unicode/emoji encoding issues in terminal
- Used `[OK]` instead of `✓` for compatibility

### Network
- Local development requires ngrok for Webex webhooks
- VPN may affect Cisco internal services

---

## Future Enhancements (Not Implemented)

### Phase 2 Enhancements
1. **Parallel Agent Calls:** Query multiple agents simultaneously
2. **Streaming Responses:** Real-time response display
3. **Conversation Memory:** Multi-turn conversations
4. **Real Data Sources:** Connect to actual CRM, KB systems

### Phase 3 Enhancements
1. **Docker Deployment:** Full observability stack
2. **SLIM Transport:** A2A protocol compliance
3. **Identity Service:** Agent authentication
4. **Webex Contact Center API:** Real integration

---

## Lessons Learned

### What Worked Well
1. Adapting CoffeeAgentcy patterns saved significant time
2. HTTP mode simplified development and testing
3. LiteLLM abstraction made provider switching easy
4. Webex bot created impressive demo

### What Could Be Improved
1. Rate limit awareness earlier
2. Test with GROQ from start (free, no limits)
3. Create startup script for all agents
4. Better error handling in production

---

## References

### CoffeeAgentcy Patterns Used
- `lungo/agents/farms/` → Specialist agent structure
- `lungo/agents/supervisors/auction/` → Orchestrator pattern
- `lungo/config/` → Configuration management
- `lungo/common/llm.py` → LLM utilities

### Key Files Adapted
| Original | AgentSwarm | Purpose |
|----------|------------|---------|
| farm_server.py | server.py | Agent HTTP server |
| graph.py | graph.py | LangGraph workflow |
| card.py | card.py | Agent capabilities |
| config.py | config.py | Environment config |

---

## Changelog

| Date | Change | Author |
|------|--------|--------|
| Day 1 | Initial architecture, 5 agents built | AI + User |
| Day 2 | HTTP mode, Webex bot, demo prep | AI + User |

---

## Contact

For questions about these decisions, refer to:
- This document
- ARCHITECTURE.md
- Original CoffeeAgentcy documentation

