# AgentSwarm Demo Prompts - Multi-Agent Scenarios

## Overview

These 4 carefully crafted prompts demonstrate the full power of multi-agent collaboration in AgentSwarm. Each scenario shows different agent combinations working together to resolve customer issues - most WITHOUT human intervention.

---

## 🎯 Prompt 1: Self-Service Resolution (2 Agents)
**Scenario:** Customer needs help but issue is resolved entirely by AI agents

### The Prompt:
```
Hi, I'm customer #67890 and I forgot my password. I've tried the reset link but it's not working. Can you help me get back into my account?
```

### Expected Agent Flow:
```
[SUPERVISOR] → Analyzes: Password issue + Customer ID
     │
     ├─→ [CRM Agent] 
     │      └─→ Looks up customer #67890 (Jane Smith, Standard tier)
     │      └─→ Finds: 1 recent issue (password reset)
     │      └─→ Notes: Account since 2023
     │
     └─→ [KNOWLEDGE Agent]
            └─→ Retrieves password reset troubleshooting
            └─→ Provides step-by-step: Settings > Account > Reset
            └─→ Checks spam folder tip
            └─→ Alternative: Contact support if link expired
     │
     ▼
[AGGREGATOR] → Combines CRM context + Knowledge steps
     │
     ▼
✅ RESOLVED WITHOUT HUMAN - Personalized instructions sent
```

### Why This Works:
- **CRM** identifies the customer and sees they had a recent password issue
- **KNOWLEDGE** provides the exact troubleshooting steps
- **No Ticket needed** - common issue with known solution
- **No Escalation needed** - not urgent, standard tier customer

### Expected Output Highlights:
- "Hello Jane Smith, I see you're having trouble with password reset..."
- Step-by-step instructions personalized to their account
- Tips about checking spam folder
- Alternative contact method if needed

---

## 🎯 Prompt 2: Issue Tracking & Resolution (3 Agents)
**Scenario:** Customer reports a problem that needs documentation but can still be resolved

### The Prompt:
```
I'm customer #12345 and my internet has been slow for the past 3 days. I've already restarted my router twice. Can you create a ticket and help me fix this?
```

### Expected Agent Flow:
```
[SUPERVISOR] → Analyzes: Slow internet + Customer ID + Ticket request
     │
     ├─→ [CRM Agent]
     │      └─→ Looks up customer #12345 (John Doe, Premium tier)
     │      └─→ Finds: 3 recent issues including "slow internet"
     │      └─→ Notes: Premium customer since 2020
     │      └─→ Flags: Recurring issue pattern!
     │
     ├─→ [KNOWLEDGE Agent]
     │      └─→ Retrieves slow internet troubleshooting
     │      └─→ Advanced steps beyond router restart
     │      └─→ Bandwidth check, speed test instructions
     │      └─→ ISP contact recommendation
     │
     └─→ [TICKET Agent]
            └─→ Creates ticket: TKT-XXXXX
            └─→ Priority: HIGH (Premium customer + recurring issue)
            └─→ Category: Network
            └─→ Assigned: Network Support Team
            └─→ ETA: Within 4 hours
     │
     ▼
[AGGREGATOR] → Combines all three agent responses
     │
     ▼
✅ RESOLVED BY AI - Ticket created + troubleshooting provided
```

### Why This Works:
- **CRM** reveals this is a Premium customer with recurring issues
- **KNOWLEDGE** provides advanced troubleshooting beyond what they tried
- **TICKET** documents the issue with appropriate priority
- **No Escalation needed** - not critical, has workaround

### Expected Output Highlights:
- "Hello John Doe, Premium customer since 2020..."
- "I see this is your 3rd internet issue - let's get this resolved"
- Advanced troubleshooting steps
- Ticket TKT-XXXXX created with HIGH priority
- Network team will follow up within 4 hours

---

## 🎯 Prompt 3: VIP Full Collaboration (ALL 4 Agents)
**Scenario:** Critical issue requiring all agents to work together

### The Prompt:
```
URGENT: I'm enterprise customer #11111, our entire office network is down affecting 50+ employees. We have a critical client presentation in 2 hours. This is a business emergency!
```

### Expected Agent Flow:
```
[SUPERVISOR] → Analyzes: URGENT + Enterprise + Network down + Time-critical
     │
     ├─→ [CRM Agent]
     │      └─→ Looks up customer #11111 (Bob Johnson)
     │      └─→ Finds: Enterprise tier, VIP support
     │      └─→ Account since 2019, excellent history
     │      └─→ Flags: VIP CUSTOMER - PRIORITY HANDLING
     │
     ├─→ [KNOWLEDGE Agent]
     │      └─→ Retrieves emergency network troubleshooting
     │      └─→ Immediate steps: Check main router, ISP status
     │      └─→ Backup options: Mobile hotspot, alternative site
     │      └─→ Escalation path documentation
     │
     ├─→ [TICKET Agent]
     │      └─→ Creates ticket: TKT-XXXXX
     │      └─→ Priority: CRITICAL
     │      └─→ Category: Network Emergency
     │      └─→ Assigned: Senior Network Engineer (immediate)
     │      └─→ ETA: 15 minutes response
     │      └─→ SLA: Enterprise 99.99% uptime commitment
     │
     └─→ [ESCALATION Agent]
            └─→ Level: CRITICAL
            └─→ Requires Human: YES
            └─→ Team: Network Engineering (On-Call)
            └─→ Priority: IMMEDIATE
            └─→ Reason: 50+ employees affected, business critical
            └─→ Action: Page on-call engineer NOW
            └─→ Backup: Prepare failover options
     │
     ▼
[AGGREGATOR] → Synthesizes comprehensive emergency response
     │
     ▼
⚠️ ESCALATED TO HUMAN - But with full context prepared
```

### Why This Works:
- **CRM** confirms VIP Enterprise status - triggers priority handling
- **KNOWLEDGE** provides immediate troubleshooting + backup options
- **TICKET** creates CRITICAL ticket with 15-min response SLA
- **ESCALATION** pages on-call engineer with full context
- **Human gets involved** but with ALL information ready

### Expected Output Highlights:
- "🚨 CRITICAL ALERT: Enterprise customer emergency detected"
- VIP status confirmed, priority handling activated
- Immediate troubleshooting steps while engineer is paged
- Ticket TKT-XXXXX created - CRITICAL priority
- On-call Network Engineer being contacted NOW
- Backup options provided (mobile hotspot for presentation)
- 15-minute response commitment

---

## 🎯 Prompt 4: Complex Multi-Issue Resolution (3-4 Agents)
**Scenario:** Customer has multiple issues that need coordinated resolution

### The Prompt:
```
Hi, I'm customer #12345. I have several problems: 1) My bill seems wrong - charged twice this month, 2) My router keeps disconnecting, and 3) I want to upgrade to Premium tier. Can you help with all of this?
```

### Expected Agent Flow:
```
[SUPERVISOR] → Analyzes: Multiple issues (Billing + Technical + Account change)
     │
     ├─→ [CRM Agent]
     │      └─→ Looks up customer #12345 (John Doe)
     │      └─→ Current tier: Premium (already premium!)
     │      └─→ Billing history: Identifies double charge
     │      └─→ Account notes: Recent router issues
     │      └─→ Recommendation: Billing adjustment needed
     │
     ├─→ [KNOWLEDGE Agent]
     │      └─→ Router disconnection troubleshooting
     │      └─→ Steps: Firmware update, channel change, placement
     │      └─→ Billing FAQ: Refund process explained
     │      └─→ Upgrade info: Already Premium - maybe Enterprise?
     │
     ├─→ [TICKET Agent]
     │      └─→ Creates ticket: TKT-XXXXX
     │      └─→ Priority: MEDIUM (billing issue + technical)
     │      └─→ Category: Multiple (Billing + Network)
     │      └─→ Sub-tickets created for each issue
     │      └─→ Assigned: Billing Team + Network Support
     │
     └─→ [ESCALATION Agent]
            └─→ Level: MEDIUM
            └─→ Requires Human: YES (for billing refund approval)
            └─→ Team: Billing Department
            └─→ Reason: Refund requires human authorization
            └─→ Technical issue: Can be handled by AI
     │
     ▼
[AGGREGATOR] → Coordinates multi-issue response
     │
     ▼
⚡ PARTIAL AI RESOLUTION + BILLING ESCALATED
```

### Why This Works:
- **CRM** discovers they're already Premium (prevents unnecessary upgrade)
- **CRM** identifies the double billing issue
- **KNOWLEDGE** provides router troubleshooting
- **TICKET** creates organized sub-tickets for each issue
- **ESCALATION** flags billing for human approval (refunds need authorization)
- **Router issue resolved by AI**, billing needs human

### Expected Output Highlights:
- "Hello John, I see you have 3 concerns - let me address each:"
- "1) BILLING: I found the double charge. Refund request submitted (requires approval)"
- "2) ROUTER: Here are steps to fix disconnections..."
- "3) UPGRADE: Good news - you're already Premium! Did you mean Enterprise?"
- Ticket created with sub-items for tracking
- Billing team will contact within 24 hours for refund

---

## 📊 Summary: Agent Involvement by Scenario

| Prompt | CRM | KNOWLEDGE | TICKET | ESCALATION | Human Needed? |
|--------|-----|-----------|--------|------------|---------------|
| #1 Password Reset | ✅ | ✅ | ❌ | ❌ | **NO** - Fully automated |
| #2 Slow Internet | ✅ | ✅ | ✅ | ❌ | **NO** - Documented & resolved |
| #3 VIP Emergency | ✅ | ✅ | ✅ | ✅ | **YES** - Engineer paged |
| #4 Multi-Issue | ✅ | ✅ | ✅ | ✅ | **PARTIAL** - Billing only |

---

## 🎬 Demo Script

### Opening (say to audience):
> "Watch how AgentSwarm coordinates multiple AI agents to handle customer requests. Each agent specializes in a different area, and they work together like a team of human experts."

### For each prompt:
1. **Show the visual flow diagram** in the response
2. **Point out the execution timeline** with timestamps
3. **Highlight agent-to-agent communication** messages
4. **Explain why certain agents were/weren't involved**

### Key talking points:
- "Notice how CRM data influences other agents' decisions"
- "The ticket priority was set based on customer tier from CRM"
- "Escalation only happens when truly necessary"
- "Most issues resolved WITHOUT human intervention"

---

## 🚀 Quick Copy-Paste Prompts

```
Prompt 1 (2 agents, no human):
Hi, I'm customer #67890 and I forgot my password. I've tried the reset link but it's not working. Can you help me get back into my account?

Prompt 2 (3 agents, no human):
I'm customer #12345 and my internet has been slow for the past 3 days. I've already restarted my router twice. Can you create a ticket and help me fix this?

Prompt 3 (ALL 4 agents, human escalation):
URGENT: I'm enterprise customer #11111, our entire office network is down affecting 50+ employees. We have a critical client presentation in 2 hours. This is a business emergency!

Prompt 4 (3-4 agents, partial human):
Hi, I'm customer #12345. I have several problems: 1) My bill seems wrong - charged twice this month, 2) My router keeps disconnecting, and 3) I want to upgrade to Premium tier. Can you help with all of this?
```

---

## 💡 Tips for Best Demo Impact

1. **Start with Prompt 1** - Shows basic 2-agent collaboration
2. **Progress to Prompt 2** - Adds ticket creation
3. **Build to Prompt 3** - Full 4-agent emergency response
4. **End with Prompt 4** - Shows complex multi-issue handling

This progression tells a story of increasing complexity and demonstrates the full range of AgentSwarm's capabilities!
