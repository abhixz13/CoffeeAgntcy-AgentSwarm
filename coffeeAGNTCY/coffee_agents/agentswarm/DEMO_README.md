# AgentSwarm Demo - Quick Start Guide

## Windows Demo Scripts

### Start Demo
Double-click `start_demo.bat` to launch all services:
- Opens 4 separate console windows (one per service)
- Waits 3 seconds between starts to avoid conflicts
- Shows status messages

**Services Started:**
1. Knowledge Agent (Port 8001)
2. Orchestrator (Port 8000)
3. CRM Agent (Port 8002)
4. Webex Bot Gateway (RabbitMQ)

### Stop Demo
Double-click `stop_demo.bat` to shutdown all services:
- Cleanly terminates all agent processes
- Closes all console windows

## Manual Start (Alternative)

### Option 1: Individual Terminals
```powershell
# Terminal 1 - Knowledge Agent
cd C:\code\coffeeAgentify\coffeeAGNTCY\coffee_agents\agentswarm
python agents/knowledge/server.py

# Terminal 2 - Orchestrator
cd C:\code\coffeeAgentify\coffeeAGNTCY\coffee_agents\agentswarm
python agents/orchestrator/main.py

# Terminal 3 - Webex Bot
cd C:\code\coffeeAgentify\coffeeAGNTCY\coffee_agents\agentswarm
python webex/bot_gateway.py
```

### Option 2: Python Script
```powershell
cd C:\code\coffeeAgentify\coffeeAGNTCY\coffee_agents\agentswarm
python start_demo.py
```

## Testing

1. **Start services** using `start_demo.bat`
2. **Wait 10 seconds** for all services to initialize
3. **Send a message** to your Webex bot:
   - "How do I reset my password?"
   - "Look up customer order #12345"
   - "Create a support ticket"
4. **Observe the flow** in console windows:
   - Bot Gateway receives message
   - Orchestrator classifies intent
   - Specialist agent processes query
   - Response returns to Webex

## Troubleshooting

**Services won't start:**
- Check if ports 8000, 8001, 8002 are already in use
- Run `stop_demo.bat` to clear any stuck processes

**Bot not responding:**
- Verify `WEBEX_BOT_TOKEN` in `.env`
- Check Bot Gateway console for RabbitMQ connection
- Ensure registered at https://scripts.cisco.com/app/quicker_bots/

**CIRCUIT API errors:**
- Verify VPN connection
- Check CIRCUIT credentials in `.env`
- Test with `python test_circuit.py`

## Demo Flow

```
User Message (Webex)
    ↓
Bot Gateway (RabbitMQ) → logs to debug.log
    ↓
Orchestrator (Intent Classification)
    ↓
Specialist Agent (Knowledge/CRM/Ticket/Escalation)
    ↓
Aggregator (Combines responses)
    ↓
Bot Gateway → Webex Response
```

## Debug Logs

All interactions are logged to: `C:\code\coffeeAgentify\.cursor\debug.log`

View logs in real-time:
```powershell
Get-Content C:\code\coffeeAgentify\.cursor\debug.log -Wait
```
