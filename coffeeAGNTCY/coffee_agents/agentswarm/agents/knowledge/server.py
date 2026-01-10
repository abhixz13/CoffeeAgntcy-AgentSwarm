# Copyright AGNTCY Contributors (https://github.com/agntcy)
# SPDX-License-Identifier: Apache-2.0
# AgentSwarm - Knowledge Agent HTTP Server (No Docker Required!)

import logging
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

from agents.knowledge.agent import KnowledgeAgent
from agents.knowledge.card import AGENT_CARD
from config.config import KNOWLEDGE_AGENT_PORT
from config.logging_config import setup_logging

# Setup
setup_logging()
logger = logging.getLogger("agentswarm.knowledge.server")

# Initialize FastAPI
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

# Initialize agent
agent = KnowledgeAgent()

# Request model
class PromptRequest(BaseModel):
    prompt: str

# Routes
@app.post("/process")
async def process_prompt(request: PromptRequest):
    """Process a customer query and return knowledge base answer."""
    try:
        logger.info(f"Processing: {request.prompt[:50]}...")
        response = await agent.process(request.prompt)
        return {"response": response}
    except Exception as e:
        logger.error(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy", "agent": AGENT_CARD.name}

@app.get("/")
async def root():
    """Agent info endpoint."""
    return {
        "name": AGENT_CARD.name,
        "description": AGENT_CARD.description,
        "port": KNOWLEDGE_AGENT_PORT,
        "endpoints": ["POST /process", "GET /health"]
    }

if __name__ == "__main__":
    print("=" * 60)
    print(f" {AGENT_CARD.name}")
    print(f" Port: {KNOWLEDGE_AGENT_PORT}")
    print("=" * 60)
    uvicorn.run(app, host="0.0.0.0", port=KNOWLEDGE_AGENT_PORT)
