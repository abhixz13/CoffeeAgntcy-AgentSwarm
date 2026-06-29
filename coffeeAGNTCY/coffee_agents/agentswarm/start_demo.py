# AgentSwarm - Demo Startup Script
# Starts all agents for the Webex demo

import subprocess
import sys
import time
import os

# Change to agentswarm directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

print("=" * 60)
print(" AgentSwarm - Starting Demo")
print("=" * 60)

# List of agents to start
agents = [
    ("Knowledge Agent", "python agents/knowledge/server.py", 8001),
    ("CRM Agent", "python agents/crm/server.py", 8002),
    ("Ticket Agent", "python agents/ticket/server.py", 8003),
    ("Escalation Agent", "python agents/escalation/server.py", 8004),
    ("Orchestrator", "python agents/orchestrator/main.py", 8000),
    ("Webex Bot", "python webex/bot.py", 5000),
]

processes = []

print("\nStarting agents...\n")

for name, cmd, port in agents:
    print(f"  Starting {name} on port {port}...")
    # Start each agent in a new process
    proc = subprocess.Popen(
        cmd,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        creationflags=subprocess.CREATE_NEW_CONSOLE if sys.platform == "win32" else 0
    )
    processes.append((name, proc, port))
    time.sleep(2)  # Give each agent time to start

print("\n" + "=" * 60)
print(" All agents started!")
print("=" * 60)
print("\n Agents running:")
for name, _, port in processes:
    print(f"   - {name}: http://localhost:{port}")

print("\n" + "=" * 60)
print(" NEXT STEPS:")
print("=" * 60)
print("""
 1. Expose Webex Bot to internet:
    ngrok http 5000
    
 2. Copy ngrok URL (e.g., https://abc123.ngrok.io)
 
 3. Register webhook at https://developer.webex.com/my-apps
    - Resource: messages
    - Event: created  
    - Target URL: https://abc123.ngrok.io/webhook
    
 4. Message your bot in Webex!
""")
print("=" * 60)
print(" Press Ctrl+C to stop all agents")
print("=" * 60)

# Wait for Ctrl+C
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\n\nStopping all agents...")
    for name, proc, _ in processes:
        proc.terminate()
        print(f"  Stopped {name}")
    print("Done!")

