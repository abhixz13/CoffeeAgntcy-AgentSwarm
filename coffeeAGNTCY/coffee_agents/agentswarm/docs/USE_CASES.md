# AgentSwarm Use Cases
## Real-World Scenarios and Examples

---

## Overview

This document provides detailed use cases showing how AgentSwarm handles various customer support scenarios. Each use case shows the query, which agents are involved, and the expected response.

---

## Use Case 1: Password Reset (Simple)

### Scenario
A customer forgot their password and needs help resetting it.

### Customer Query
```
Hi, I'm customer #67890 and I forgot my password. Can you help me reset it?
```

### Agents Involved
| Agent | Role |
|-------|------|
| CRM | Look up customer #67890 |
| Knowledge | Retrieve password reset steps |

### Agent Flow
```
[Customer] → [Supervisor] → [CRM Agent] → [Knowledge Agent] → [Aggregator] → [Response]
```

### Expected Response
```
Hello Jane Smith (Customer #67890),

I can help you reset your password. Based on your account, here are the steps:

1. Go to Settings > Account > Reset Password
2. Click "Forgot Password"
3. Check your email (j.smith@email.com) for the reset link
4. The link expires in 24 hours

Tips:
- Check your spam folder if you don't see the email
- Make sure to use a strong password (8+ characters, mix of letters/numbers)

If you continue to have issues, please let me know and I can escalate to our technical team.
```

### Why This Works
- CRM Agent identifies the customer and their email
- Knowledge Agent provides the exact reset steps
- Response is personalized with customer name

---

## Use Case 2: Technical Issue with Ticket (Medium)

### Scenario
A customer has an ongoing technical issue and wants to create a support ticket.

### Customer Query
```
I'm customer #12345 and my internet has been slow for the past 3 days. 
I've already restarted my router twice. Can you create a ticket and help me fix this?
```

### Agents Involved
| Agent | Role |
|-------|------|
| CRM | Look up customer, check history |
| Knowledge | Provide advanced troubleshooting |
| Ticket | Create support ticket |

### Agent Flow
```
[Customer] → [Supervisor] → [CRM] → [Knowledge] → [Ticket] → [Aggregator] → [Response]
```

### CRM Agent Findings
```
Customer: John Doe (#12345)
Tier: Premium
Account Since: 2020
Recent Issues: 3 (including previous slow internet complaints)
Priority: HIGH (Premium + recurring issue)
```

### Knowledge Agent Response
```
Advanced Troubleshooting Steps:
1. Check for bandwidth-heavy applications
2. Run speed test (speedtest.net)
3. Try changing WiFi channel (router settings)
4. Check for firmware updates
5. Consider router placement (away from walls/interference)
```

### Ticket Agent Action
```
✅ Ticket Created: TKT-54321
Priority: HIGH
Category: Network - Slow Internet
Assigned: Network Support Team
ETA: 4 hours
```

### Expected Response
```
Hello John Doe (Premium Customer since 2020),

I see this is your 3rd internet issue - let's get this resolved for good.

TICKET CREATED:
- Ticket ID: TKT-54321
- Priority: HIGH (Premium customer + recurring issue)
- Team: Network Support
- Expected Response: Within 4 hours

While you wait, try these advanced steps:
1. Run a speed test at speedtest.net and note the results
2. Check if specific devices are slower than others
3. Try connecting directly via ethernet cable
4. Check your router's admin page (192.168.1.1) for firmware updates

Our Network Support team will contact you within 4 hours. Given your Premium status 
and recurring issues, I've flagged this for priority handling.
```

---

## Use Case 3: Critical Emergency (Full Escalation)

### Scenario
An enterprise customer has a complete network outage affecting their business.

### Customer Query
```
URGENT: I'm enterprise customer #11111, our entire office network is down 
affecting 50+ employees. We have a critical client presentation in 2 hours. 
This is a business emergency!
```

### Agents Involved
| Agent | Role |
|-------|------|
| CRM | Identify VIP enterprise customer |
| Knowledge | Emergency troubleshooting |
| Ticket | Create CRITICAL ticket |
| Escalation | Route to Network Engineering |

### Agent Flow
```
[Customer] → [Supervisor] → [CRM] → [Knowledge] → [Ticket] → [Escalation] → [Aggregator]
```

### CRM Agent Findings
```
🚨 VIP CUSTOMER ALERT
Customer: Bob Johnson (#11111)
Tier: ENTERPRISE
Account Since: 2019
Status: VIP Support Enabled
SLA: 99.99% uptime guarantee
Recent Issues: 5 interactions, all resolved
```

### Escalation Agent Assessment
```
🚨 ESCALATION ASSESSMENT

Level: CRITICAL
Requires Human: YES

Routing Decision:
- Team: Network Engineering (On-Call)
- Specialist: Senior Network Engineer
- Priority: IMMEDIATE
- Reason: 50+ employees affected, business critical, VIP customer

Recommended Actions:
1. Page on-call Network Engineer NOW
2. Prepare failover options
3. 15-minute status updates to customer
4. Executive notification if not resolved in 30 min
```

### Expected Response
```
🚨 CRITICAL ALERT - ENTERPRISE EMERGENCY

Mr. Johnson, I understand the severity of this situation. Here's what's happening:

IMMEDIATE ACTIONS TAKEN:
✅ CRITICAL Ticket Created: TKT-99999
✅ Network Engineering Team PAGED
✅ Senior Engineer assigned - contacting you within 15 MINUTES
✅ Your Enterprise SLA (99.99%) has been activated

WHILE YOU WAIT (next 15 minutes):
1. Check if the issue is isolated to your office or affects the building
2. Verify power to all network equipment
3. Note any error lights on routers/switches

BACKUP OPTIONS FOR YOUR PRESENTATION:
- Mobile hotspot can provide temporary connectivity
- Webex meetings work on cellular data
- Nearest backup location: [Company Branch Office]

ESCALATION PATH:
- 15 min: Engineer on-site/remote
- 30 min: If unresolved, escalate to VP of Operations
- 60 min: Executive notification

I will personally monitor this ticket. You will receive updates every 15 minutes 
until resolution.

Direct Line: [Support Hotline]
Ticket: TKT-99999
Priority: CRITICAL
```

---

## Use Case 4: Multiple Issues (Complex)

### Scenario
A customer has several unrelated issues they want to address in one interaction.

### Customer Query
```
Hi, I'm customer #12345. I have several problems:
1) My bill seems wrong - I was charged twice this month
2) My router keeps disconnecting every few hours
3) I want to upgrade to Premium tier
Can you help with all of this?
```

### Agents Involved
| Agent | Role |
|-------|------|
| CRM | Look up account, check billing, check current tier |
| Knowledge | Router troubleshooting |
| Ticket | Create ticket for billing issue |
| Escalation | Flag billing for human review (refund needed) |

### CRM Agent Findings
```
Customer: John Doe (#12345)
Current Tier: Premium (already Premium!)
Billing: ANOMALY DETECTED - Double charge on Jan 5
Router Issues: 2 previous disconnection reports
```

### Expected Response
```
Hello John,

I've reviewed all three of your concerns. Here's the status:

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1️⃣ BILLING ISSUE - Double Charge
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STATUS: Confirmed - You were charged $99.99 twice on Jan 5

ACTION TAKEN:
✅ Refund request submitted: $99.99
✅ Ticket created: TKT-88888
✅ Billing team notified (requires human approval)

TIMELINE: Refund will appear in 3-5 business days

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
2️⃣ ROUTER DISCONNECTIONS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
This is your 3rd report of disconnections. Try these steps:

1. Update router firmware (check 192.168.1.1)
2. Change WiFi channel to reduce interference
3. Check for overheating (ensure ventilation)
4. Consider router placement (central location)

If issues persist after trying these steps, reply and I'll schedule 
a technician visit.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
3️⃣ UPGRADE TO PREMIUM
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
GOOD NEWS: You're already on Premium tier! 🎉

Your Premium benefits include:
- Priority support (4-hour response)
- 99.9% uptime SLA
- Free router replacement
- Dedicated account manager

Did you mean to upgrade to ENTERPRISE tier? Let me know and I can 
provide details on that.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Is there anything else I can help with?
```

---

## Use Case 5: Simple Greeting (General)

### Scenario
Customer sends a simple greeting without a specific request.

### Customer Query
```
Hello!
```

### Agents Involved
None - handled by General node

### Expected Response
```
================================================
      AGENTSWARM MULTI-AGENT SYSTEM
      Webex Contact Center AI Demo
================================================

AVAILABLE SPECIALIST AGENTS:
-----------------------------------------------
[1] KNOWLEDGE  - Technical docs & FAQs
[2] CRM        - Customer data & history
[3] TICKET     - Support ticket management
[4] ESCALATION - Urgent issue routing
-----------------------------------------------

Hello! I'm AgentSwarm - a Multi-Agent AI System.

Try these demo queries to see agents collaborate:

>> 'I'm customer #12345 and can't reset my password'
   (Triggers: CRM + Knowledge agents)

>> 'Create a ticket for order #67890 - login issue'
   (Triggers: CRM + Ticket + Knowledge agents)

>> 'URGENT: Premium customer #12345, system down!'
   (Triggers: ALL 4 agents in collaboration)
```

---

## Use Case Summary Matrix

| Use Case | Agents | Complexity | Human Needed |
|----------|--------|------------|--------------|
| Password Reset | CRM, Knowledge | Simple | No |
| Tech Issue + Ticket | CRM, Knowledge, Ticket | Medium | No |
| Critical Emergency | All 4 | High | Yes (Engineer) |
| Multiple Issues | All 4 | High | Partial (Billing) |
| Simple Greeting | None | Minimal | No |

---

## Agent Selection Patterns

### Pattern: Customer ID Mentioned
```
Query contains: "customer #", "order #", "account"
→ Always include CRM Agent
```

### Pattern: Technical Problem
```
Query contains: "slow", "not working", "error", "how to"
→ Always include Knowledge Agent
```

### Pattern: Ticket Request
```
Query contains: "ticket", "track", "create", "status"
→ Always include Ticket Agent
```

### Pattern: Urgency Indicators
```
Query contains: "URGENT", "CRITICAL", "emergency", "down", "VIP"
→ Always include Escalation Agent
→ Consider all 4 agents
```

---

*Use Cases Document v1.0*
