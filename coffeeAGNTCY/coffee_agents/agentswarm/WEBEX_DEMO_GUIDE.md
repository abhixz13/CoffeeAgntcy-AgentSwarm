# AgentSwarm Webex Demo Guide

## Quick Setup (15 minutes total)

---

## Step 1: Create Webex Bot (5 min)

1. Go to: https://developer.webex.com/my-apps
2. Click **"Create a New App"** → **"Create a Bot"**
3. Fill in:
   - **Name:** `AgentSwarm Demo`
   - **Username:** `agentswarm-[yourname]` (must be unique)
   - **Description:** `Multi-Agent AI for Contact Center`
4. Click **Create**
5. **COPY THE BOT ACCESS TOKEN** (you can only see it once!)

---

## Step 2: Configure Environment (2 min)

Add your Webex token to `.env`:

```bash
cd coffeeAGNTCY/coffee_agents/agentswarm

# Edit .env file and add:
WEBEX_BOT_TOKEN=your_bot_token_here
```

---

## Step 3: Start All Agents (3 min)

Open 6 terminal windows:

```bash
# All terminals: First navigate to agentswarm folder
cd coffeeAGNTCY/coffee_agents/agentswarm

# Terminal 1: Knowledge Agent
python agents/knowledge/server.py

# Terminal 2: CRM Agent
python agents/crm/server.py

# Terminal 3: Ticket Agent
python agents/ticket/server.py

# Terminal 4: Escalation Agent
python agents/escalation/server.py

# Terminal 5: Orchestrator
python agents/orchestrator/main.py

# Terminal 6: Webex Bot
python webex/bot.py
```

You should see all agents starting on their ports (8000-8004, 5000).

---

## Step 4: Expose Bot to Internet (2 min)

Webex needs to reach your local bot. Use ngrok:

```bash
# Install ngrok if you don't have it
# https://ngrok.com/download

# Run ngrok
ngrok http 5000
```

Copy the HTTPS URL (e.g., `https://abc123.ngrok-free.app`)

---

## Step 5: Register Webhook (3 min)

1. Go to: https://developer.webex.com/my-apps
2. Click on your bot
3. Scroll to **Webhooks** section
4. Click **Add Webhook**
5. Fill in:
   - **Name:** `AgentSwarm Messages`
   - **Target URL:** `https://abc123.ngrok-free.app/webhook` (your ngrok URL)
   - **Resource:** `messages`
   - **Event:** `created`
6. Click **Save**

---

## Step 6: Test It!

1. Open Webex
2. Start a direct message with your bot (search for `agentswarm-[yourname]@webex.bot`)
3. Send a message: "How do I reset my password?"
4. Watch the magic happen!

---

## Demo Scenarios

### Scenario 1: Simple FAQ
```
You: How do I reset my password?
Bot: To reset your password, follow these steps:
     1. Go to Settings > Account > Reset Password
     2. Click "Forgot Password"
     3. Check your email for the reset link
     ...
```

### Scenario 2: Customer Lookup
```
You: My internet is slow, order #12345
Bot: I found your account (Order #12345). Based on your plan...
     Here are troubleshooting steps:
     1. Restart your router...
```

### Scenario 3: Urgent Escalation
```
You: URGENT: Complete system outage!
Bot: This has been flagged as CRITICAL.
     Ticket #URG-2024-001 created with P1 priority.
     A human agent will contact you within 5 minutes...
```

---

## Troubleshooting

### Bot doesn't respond?
- Check all 6 terminals are running
- Check ngrok is running and URL is correct
- Check webhook is registered correctly
- Look at terminal logs for errors

### Rate limit error?
- Your OpenAI API key has a rate limit
- Wait a few minutes or use GROQ instead

### Webhook not receiving?
- Make sure ngrok URL has `/webhook` at the end
- Check Webex webhook status shows "active"

---

## Architecture

```
Webex User
    |
    v
Webex Cloud --> Webhook --> Webex Bot (5000)
                               |
                               v
                          Orchestrator (8000)
                          /    |    \    \
                         v     v     v    v
                      8001   8002  8003  8004
                   Knowledge  CRM  Ticket Escalation
```

---

## Quick Commands Reference

```bash
# Health check all services
curl http://localhost:8000/health  # Orchestrator
curl http://localhost:8001/health  # Knowledge
curl http://localhost:8002/health  # CRM
curl http://localhost:8003/health  # Ticket
curl http://localhost:8004/health  # Escalation
curl http://localhost:5000/health  # Webex Bot

# Test orchestrator directly
curl -X POST http://localhost:8000/agent/prompt \
  -H "Content-Type: application/json" \
  -d '{"prompt": "How do I reset my password?"}'
```

---

## Need Help?

- Check terminal logs for errors
- Make sure .env has all required values
- Restart all agents if something seems stuck

