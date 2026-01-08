# Copyright AGNTCY Contributors (https://github.com/agntcy)
# SPDX-License-Identifier: Apache-2.0
# AgentSwarm - Orchestrator FastAPI Server

import logging
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

from ioa_observe.sdk.tracing import session_start

from agents.orchestrator.graph import OrchestratorGraph
from config.config import ORCHESTRATOR_PORT
from config.logging_config import setup_logging

# Setup
setup_logging()
logger = logging.getLogger("agentswarm.orchestrator.main")
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="AgentSwarm Orchestrator",
    description="Multi-Agent Orchestrator for Webex Contact Center",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize orchestrator graph
orchestrator = OrchestratorGraph()

# Request models
class PromptRequest(BaseModel):
    prompt: str

# Routes
@app.post("/agent/prompt")
async def handle_prompt(request: PromptRequest):
    """
    Process customer query through multi-agent orchestrator.
    
    Args:
        request: Contains customer's prompt
        
    Returns:
        dict: Final aggregated response from specialists
    """
    try:
        logger.info(f"Received prompt: {request.prompt[:100]}...")
        session_start()  # Start new tracing session
        
        # Process through orchestrator
        result = await orchestrator.serve(request.prompt)
        
        logger.info("Successfully processed prompt")
        return {"response": result}
        
    except ValueError as ve:
        logger.error(f"ValueError: {ve}", exc_info=True)
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        logger.error(f"Error processing prompt: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Operation failed: {str(e)}")


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "AgentSwarm Orchestrator",
        "version": "1.0.0"
    }


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "service": "AgentSwarm Orchestrator",
        "description": "Multi-Agent Orchestrator for Webex Contact Center",
        "version": "1.0.0",
        "endpoints": {
            "POST /agent/prompt": "Submit customer query for processing",
            "GET /health": "Health check",
            "GET /": "This info page"
        },
        "specialist_agents": [
            "Knowledge Agent (FAQ & troubleshooting)",
            "CRM Agent (Customer information)",
            "Ticket Agent (Support tickets)",
            "Escalation Agent (Urgent routing)"
        ]
    }


@app.get("/.well-known/agent.json")
async def get_capabilities():
    """Agent capabilities endpoint (A2A protocol)."""
    return {
        "capabilities": {"streaming": False},
        "defaultInputModes": ["text"],
        "defaultOutputModes": ["text"],
        "description": "Multi-agent orchestrator that coordinates specialist agents for customer support.",
        "name": "AgentSwarm Orchestrator",
        "preferredTransport": "HTTP",
        "protocolVersion": "0.3.0",
        "skills": [
            {
                "description": "Coordinates multiple specialist agents to provide comprehensive customer support.",
                "examples": [
                    "My internet is slow, order #12345",
                    "How do I reset my password?",
                    "Create a ticket for network outage",
                    "This is urgent, I need immediate help",
                ],
                "id": "orchestrate_support",
                "name": "Multi-Agent Support Orchestration",
                "tags": ["support", "orchestration", "multi-agent"],
            }
        ],
        "supportsAuthenticatedExtendedCard": False,
        "url": f"http://localhost:{ORCHESTRATOR_PORT}",
        "version": "1.0.0",
    }


if __name__ == "__main__":
    try:
        logger.info("=" * 70)
        logger.info(" AgentSwarm Orchestrator - Multi-Agent Coordinator")
        logger.info("=" * 70)
        logger.info(f"Starting server on http://0.0.0.0:{ORCHESTRATOR_PORT}")
        logger.info("")
        logger.info("Coordinating Specialist Agents:")
        logger.info("  - Knowledge Agent (FAQ & troubleshooting)")
        logger.info("  - CRM Agent (customer information)")
        logger.info("  - Ticket Agent (support tickets)")
        logger.info("  - Escalation Agent (urgent routing)")
        logger.info("")
        logger.info("API Endpoints:")
        logger.info(f"  - POST http://localhost:{ORCHESTRATOR_PORT}/agent/prompt")
        logger.info(f"  - GET  http://localhost:{ORCHESTRATOR_PORT}/health")
        logger.info("=" * 70)
        
        uvicorn.run(
            "agents.orchestrator.main:app",
            host="0.0.0.0",
            port=ORCHESTRATOR_PORT,
            reload=False
        )
    except KeyboardInterrupt:
        logger.info("\nShutting down gracefully.")
    except Exception as e:
        logger.error(f"Error occurred: {e}", exc_info=True)


