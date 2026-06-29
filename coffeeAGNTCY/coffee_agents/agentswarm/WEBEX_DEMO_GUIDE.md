# AgentSwarm Webex Demo Guide

## Two Options for Webex Integration

### Option A: Cisco Bot Gateway (RECOMMENDED for Cisco Network)
- No ngrok needed!
- Works on Cisco VPN
- Uses RabbitMQ for message delivery

### Option B: Webhook with ngrok (External Networks)
- Requires ngrok
- Works anywhere with internet

---

# Option A: Cisco Bot Gateway Setup (10 minutes)

## Step 1: Create Webex Bot (if not done)

1. Go to: https://developer.webex.com/my-apps
2. Click "Create a New App" → "Create a Bot"
3. Fill in details, click "Create"
4. **COPY THE BOT ACCESS TOKEN** (only shown once!)

## Step 2: Register Bot on Quicker Bots

**IMPORTANT:** This step creates the RabbitMQ queue for your bot.

1. Go to: https://scripts.cisco.com/app/quicker_bots/
2. Click "Add Bot"
3. Paste your Bot Token
4. Click "Add"
5. Note the queue URL (you'll see something like: `.../queues/Webex-Teams-Bot-Gateway/your-bot-name`)

## Step 3: Install pika (RabbitMQ client)

```bash
pip install pika
```

## Step 4: Configure .env

Make sure your `.env` has:
```bash
WEBEX_BOT_TOKEN="your_bot_token_here"
```

## Step 5: Start Agents + Bot Gateway

```bash
cd coffeeAGNTCY/coffee_agents/agentswarm

# Terminal 1-5: Start all agents (same as before)
python agents/knowledge/server.py
python agents/crm/server.py
python agents/ticket/server.py
python agents/escalation/server.py
python agents/orchestrator/main.py

# Terminal 6: Start Bot Gateway (instead of webhook bot)
python webex/bot_gateway.py
```

## Step 6: Test It!

1. Open Webex
2. Search for your bot name
3. Send a message: "How do I reset my password?"
4. Watch the magic happen!

---

# Option B: Webhook with ngrok Setup (15 minutes)

Use this if you're NOT on Cisco network or Bot Gateway doesn't work.

## Step 1: Create Webex Bot (same as above)

## Step 2: Install ngrok

Download from: https://ngrok.com/download

## Step 3: Start Agents + Webhook Bot

```bash
cd coffeeAGNTCY/coffee_agents/agentswarm

# Terminal 1-5: Start all agents
python agents/knowledge/server.py
python agents/crm/server.py
python agents/ticket/server.py
python agents/escalation/server.py
python agents/orchestrator/main.py

# Terminal 6: Start Webhook Bot
python webex/bot.py
```

## Step 4: Expose with ngrok

```bash
ngrok http 5000
```

Copy the HTTPS URL (e.g., `https://abc123.ngrok-free.app`)

## Step 5: Register Webhook

1. Go to: https://developer.webex.com/my-apps
2. Click on your bot
3. Scroll to "Webhooks" → "Add Webhook"
4. Fill in:
   - Name: `AgentSwarm Messages`
   - Target URL: `https://abc123.ngrok-free.app/webhook`
   - Resource: `messages`
   - Event: `created`
5. Click "Save"

## Step 6: Test It!

Same as Option A - message your bot in Webex!

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
     Ticket #URG-2026-001 created with P1 priority.
     A human agent will contact you within 5 minutes...
```

---

## Troubleshooting

### Bot Gateway Issues

**Authentication Error:**
```
[ERROR] Authentication failed!
```
→ Make sure you registered bot at https://scripts.cisco.com/app/quicker_bots/

**Connection Error:**
```
[ERROR] Could not connect to RabbitMQ
```
→ Make sure you're on Cisco VPN

**Queue Not Found:**
→ Queue name = bot's display name (lowercase, spaces → hyphens)
→ Check the queue name at quicker_bots portal

### Webhook Issues

**Bot doesn't respond:**
- Check ngrok is running
- Check webhook URL has `/webhook` at end
- Check webhook is "active" in developer portal

### Rate Limit Error
```
Rate limit reached for gpt-4o-mini
```
→ Wait a few minutes or switch to GROQ

---

## Architecture

### Option A: Bot Gateway
```
Webex Cloud
    |
    v (WebSocket)
Bot Listener (K8s)
    |
    v (AMQP)
RabbitMQ Queue
    |
    v (pika)
bot_gateway.py (5000)
    |
    v (HTTP)
Orchestrator (8000)
    |
    v
Specialist Agents (8001-8004)
```

### Option B: Webhook
```
Webex Cloud
    |
    v (HTTPS webhook)
ngrok tunnel
    |
    v
bot.py (5000)
    |
    v (HTTP)
Orchestrator (8000)
    |
    v
Specialist Agents (8001-8004)
```

---

## Quick Reference

```bash
# Health checks
curl http://localhost:8000/health  # Orchestrator
curl http://localhost:8001/health  # Knowledge
curl http://localhost:8002/health  # CRM
curl http://localhost:8003/health  # Ticket
curl http://localhost:8004/health  # Escalation

# Test orchestrator directly
curl -X POST http://localhost:8000/agent/prompt \
  -H "Content-Type: application/json" \
  -d '{"prompt": "How do I reset my password?"}'
```
