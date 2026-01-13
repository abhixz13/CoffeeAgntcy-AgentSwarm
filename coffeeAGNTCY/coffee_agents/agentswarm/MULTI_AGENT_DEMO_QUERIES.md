# Multi-Agent Demo Queries

## 🎯 Showcase Different Agent Combinations

### Single Agent Demos (Current)

#### 1. **FAQ Only** → Knowledge Agent
```
Query: "How do I reset my password?"
Agents: Knowledge
Flow: FAQ classification → Knowledge Base lookup
```

#### 2. **Customer Lookup** → CRM Agent
```
Query: "What is the status of my account #12345?"
Agents: CRM
Flow: Customer lookup → Account info retrieval
```

#### 3. **Ticket Creation** → Ticket Agent
```
Query: "I need to create a support ticket for a login issue"
Agents: Ticket
Flow: Ticket creation → Assign priority
```

#### 4. **Escalation** → Escalation Agent
```
Query: "URGENT: Critical system outage affecting production!"
Agents: Escalation
Flow: Urgency assessment → Routing decision
```

---

## 🚀 Multi-Agent Demos (Future Enhancement)

To demonstrate TRUE multi-agent collaboration, you would need queries that require **multiple specialists working together**:

### Architecture Change Needed

Current: **1 intent → 1 agent**
```
FAQ intent → Knowledge Agent only
```

Enhanced: **1 intent → Multiple agents in parallel**
```
Customer-specific FAQ → CRM + Knowledge + Ticket (if needed)
```

### Example Enhanced Flows

#### Scenario 1: Customer-Specific Troubleshooting
```
Query: "I'm premium customer #12345 and my WiFi keeps disconnecting"

Flow:
1. Supervisor classifies as "customer_lookup + faq"
2. **Parallel Calls:**
   - CRM Agent: "Customer #12345, Premium tier, 3 previous tickets"
   - Knowledge Agent: "WiFi troubleshooting steps: restart router, check firmware..."
3. Aggregator: Combines customer context + technical solution
4. Response: "Hi John (Premium Customer), I see you've had similar issues before. 
   Let me help you with priority support..."
```

#### Scenario 2: Issue with Ticket Creation
```
Query: "Customer #67890 order delayed, need to escalate"

Flow:
1. Supervisor classifies as "customer_lookup + ticket + escalation"
2. **Parallel Calls:**
   - CRM Agent: "Order #67890, placed 10 days ago, customer tier: Standard"
   - Ticket Agent: "Created ticket #TKT-12345, Priority: High"
   - Escalation Agent: "Routing to logistics team, SLA: 24 hours"
3. Aggregator: "Created ticket #TKT-12345 for your order delay. 
   Escalated to logistics team - you'll hear back within 24 hours."
```

---

## 🎬 Demo Script (Current Architecture)

### Demo Flow 1: Knowledge Agent
**Say:** "Let's start with a simple FAQ question"
**Query:** `"How do I reset my password?"`
**Show:** Knowledge Agent window processing the query
**Result:** Step-by-step password reset instructions

### Demo Flow 2: CRM Agent
**Say:** "Now let's look up a customer account"
**Query:** `"Show me details for customer account #12345"`
**Show:** CRM Agent window retrieving customer data
**Result:** Customer tier, order history, past interactions

### Demo Flow 3: Ticket Agent
**Say:** "Let's create a support ticket"
**Query:** `"Create a ticket for internet connectivity issue"`
**Show:** Ticket Agent window creating ticket
**Result:** Ticket number, priority assignment, estimated response time

### Demo Flow 4: Escalation Agent
**Say:** "Now a critical issue requiring immediate escalation"
**Query:** `"CRITICAL: Production server down for 2 hours!"`
**Show:** Escalation Agent window assessing urgency
**Result:** Escalation path, team routing, SLA commitment

---

## 💡 Key Demo Talking Points

1. **Specialization**: Each agent is an expert in its domain
2. **Orchestration**: Supervisor intelligently routes queries
3. **Observability**: All interactions logged and traceable
4. **Scalability**: Easy to add new specialist agents
5. **Flexibility**: Agents can be called individually or in combination

---

## 🔧 To Enable True Multi-Agent Collaboration

**Option 1: Modify Supervisor to call multiple agents**
- Change intent classification to support multiple intents
- Example: `["customer_lookup", "faq"]` → Call both CRM + Knowledge

**Option 2: Add composite intents**
- `customer_faq`: Automatically calls CRM + Knowledge
- `customer_ticket`: Automatically calls CRM + Ticket + Escalation

**Option 3: Tool-based approach** (Most flexible)
- Supervisor has access to all agents as "tools"
- LLM decides which agents to call based on query
- Agents can chain together dynamically

---

## 📊 Current Demo Value

**Even with single-agent routing**, the demo showcases:
- ✅ Intent classification (LLM-powered)
- ✅ Agent specialization (domain experts)
- ✅ HTTP-based communication (no Docker needed)
- ✅ Webex integration (real-time chat)
- ✅ CIRCUIT API (Cisco internal LLM)
- ✅ Observability (debug logs for every step)

**The architecture is already multi-agent** - it just routes intelligently to avoid unnecessary calls!
