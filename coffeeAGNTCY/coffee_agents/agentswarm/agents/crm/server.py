# Copyright AGNTCY Contributors (https://github.com/agntcy)
# SPDX-License-Identifier: Apache-2.0
# AgentSwarm - CRM Agent HTTP Server (No Docker Required!)

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

from agents.crm.agent import CRMAgent
from agents.crm.card import AGENT_CARD
from config.config import CRM_AGENT_PORT
from config.logging_config import setup_logging

setup_logging()
logger = logging.getLogger("agentswarm.crm.server")

app = FastAPI(
    title=AGENT_CARD.name,
    description=AGENT_CARD.description,
    version=AGENT_CARD.version
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

agent = CRMAgent()

class PromptRequest(BaseModel):
    prompt: str

@app.post("/process")
async def process_prompt(request: PromptRequest):
    """Process a customer query and return CRM data."""
    try:
        logger.info(f"Processing: {request.prompt[:50]}...")
        response = await agent.process(request.prompt)
        return {"response": response}
    except Exception as e:
        logger.error(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health():
    return {"status": "healthy", "agent": AGENT_CARD.name}

@app.get("/")
async def root():
    return {
        "name": AGENT_CARD.name,
        "description": AGENT_CARD.description,
        "port": CRM_AGENT_PORT,
        "endpoints": ["POST /process", "GET /health"]
    }

if __name__ == "__main__":
    print("=" * 60)
    print(f" {AGENT_CARD.name}")
    print(f" Port: {CRM_AGENT_PORT}")
    print("=" * 60)
    uvicorn.run(app, host="0.0.0.0", port=CRM_AGENT_PORT)
