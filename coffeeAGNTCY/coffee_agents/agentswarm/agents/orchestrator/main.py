# Copyright AGNTCY Contributors (https://github.com/agntcy)
# SPDX-License-Identifier: Apache-2.0
# AgentSwarm - Orchestrator HTTP Server (No Docker Required!)

import logging
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

from agents.orchestrator.graph import OrchestratorGraph
from config.config import ORCHESTRATOR_PORT
from config.logging_config import setup_logging

setup_logging()
logger = logging.getLogger("agentswarm.orchestrator.main")

app = FastAPI(
    title="AgentSwarm Orchestrator",
    description="Multi-Agent Orchestrator for Webex Contact Center",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize orchestrator
orchestrator = OrchestratorGraph()

class PromptRequest(BaseModel):
    prompt: str

@app.post("/agent/prompt")
async def handle_prompt(request: PromptRequest):
    """Process customer query through multi-agent orchestrator."""
    import json
    import time as _time
    # #region agent log
    with open(r'c:\code\coffeeAgentify\.cursor\debug.log', 'a') as f: f.write(json.dumps({"hypothesisId":"H5","location":"main.py:handle_prompt:entry","message":"Orchestrator HTTP request received","data":{"prompt":request.prompt[:50]},"timestamp":int(_time.time()*1000),"sessionId":"debug-session"})+'\n')
    # #endregion
    try:
        logger.info(f"Received: {request.prompt[:50]}...")
        result = await orchestrator.run(request.prompt)
        # #region agent log
        with open(r'c:\code\coffeeAgentify\.cursor\debug.log', 'a') as f: f.write(json.dumps({"hypothesisId":"H5","location":"main.py:handle_prompt:success","message":"Orchestrator returning response","data":{"result_len":len(result) if result else 0,"result_preview":result[:100] if result else None},"timestamp":int(_time.time()*1000),"sessionId":"debug-session"})+'\n')
        # #endregion
        return {"response": result}
    except Exception as e:
        logger.error(f"Error: {e}", exc_info=True)
        # #region agent log
        with open(r'c:\code\coffeeAgentify\.cursor\debug.log', 'a') as f: f.write(json.dumps({"hypothesisId":"H5","location":"main.py:handle_prompt:exception","message":"Orchestrator exception","data":{"error":str(e),"error_type":type(e).__name__},"timestamp":int(_time.time()*1000),"sessionId":"debug-session"})+'\n')
        # #endregion
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health():
    return {"status": "healthy", "service": "AgentSwarm Orchestrator"}

@app.get("/")
async def root():
    return {
        "service": "AgentSwarm Orchestrator",
        "description": "Multi-Agent System for Webex Contact Center",
        "version": "1.0.0",
        "mode": "HTTP (No Docker Required)",
        "endpoints": {
            "POST /agent/prompt": "Submit customer query",
            "GET /health": "Health check"
        },
        "agents": {
            "knowledge": "http://localhost:8001 - FAQ & troubleshooting",
            "crm": "http://localhost:8002 - Customer data",
            "ticket": "http://localhost:8003 - Support tickets",
            "escalation": "http://localhost:8004 - Urgent routing"
        }
    }

if __name__ == "__main__":
    print("=" * 60)
    print(" AgentSwarm Orchestrator")
    print(" Multi-Agent System for Webex Contact Center")
    print("=" * 60)
    print(f" Port: {ORCHESTRATOR_PORT}")
    print(" Mode: HTTP (No Docker Required!)")
    print("=" * 60)
    print(" Specialist Agents:")
    print("   - Knowledge: http://localhost:8001")
    print("   - CRM:       http://localhost:8002")
    print("   - Ticket:    http://localhost:8003")
    print("   - Escalation:http://localhost:8004")
    print("=" * 60)
    uvicorn.run(app, host="0.0.0.0", port=ORCHESTRATOR_PORT)
