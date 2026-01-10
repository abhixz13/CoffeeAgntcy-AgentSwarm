# Copyright AGNTCY Contributors (https://github.com/agntcy)
# SPDX-License-Identifier: Apache-2.0
# AgentSwarm - Webex Bot Integration

import logging
import os
import sys
import httpx
from typing import Optional

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

from config.config import WEBEX_BOT_TOKEN, ORCHESTRATOR_PORT
from config.logging_config import setup_logging

setup_logging()
logger = logging.getLogger("agentswarm.webex.bot")

# Webex API
WEBEX_API_URL = "https://webexapis.com/v1"

app = FastAPI(
    title="AgentSwarm Webex Bot",
    description="Webex Bot for Multi-Agent Contact Center Demo",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Bot info cache
_bot_info: Optional[dict] = None

async def get_bot_info() -> dict:
    """Get bot's own information (cached)."""
    global _bot_info
    if _bot_info is None:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{WEBEX_API_URL}/people/me",
                headers={"Authorization": f"Bearer {WEBEX_BOT_TOKEN}"}
            )
            response.raise_for_status()
            _bot_info = response.json()
            logger.info(f"Bot info: {_bot_info.get('displayName')} ({_bot_info.get('emails', [''])[0]})")
    return _bot_info

async def send_webex_message(room_id: str, text: str, markdown: str = None):
    """Send a message to a Webex room."""
    async with httpx.AsyncClient() as client:
        payload = {
            "roomId": room_id,
            "text": text,
        }
        if markdown:
            payload["markdown"] = markdown
        
        response = await client.post(
            f"{WEBEX_API_URL}/messages",
            headers={
                "Authorization": f"Bearer {WEBEX_BOT_TOKEN}",
                "Content-Type": "application/json"
            },
            json=payload
        )
        response.raise_for_status()
        logger.info(f"Message sent to room {room_id[:20]}...")
        return response.json()

async def get_message_details(message_id: str) -> dict:
    """Get full message details (webhook only sends ID)."""
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{WEBEX_API_URL}/messages/{message_id}",
            headers={"Authorization": f"Bearer {WEBEX_BOT_TOKEN}"}
        )
        response.raise_for_status()
        return response.json()

async def call_orchestrator(prompt: str) -> str:
    """Send prompt to AgentSwarm Orchestrator and get response."""
    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                f"http://localhost:{ORCHESTRATOR_PORT}/agent/prompt",
                json={"prompt": prompt}
            )
            response.raise_for_status()
            data = response.json()
            return data.get("response", "Sorry, I couldn't process that.")
    except httpx.ConnectError:
        logger.error("Orchestrator not running!")
        return "[ERROR] AgentSwarm Orchestrator is not running. Please start it first."
    except Exception as e:
        logger.error(f"Orchestrator error: {e}")
        return f"[ERROR] Failed to process: {str(e)}"

# Webhook payload model
class WebhookPayload(BaseModel):
    id: str
    name: str
    resource: str
    event: str
    data: dict

@app.post("/webhook")
async def handle_webhook(request: Request):
    """Handle incoming Webex webhook events."""
    try:
        payload = await request.json()
        logger.info(f"Webhook received: {payload.get('resource')} - {payload.get('event')}")
        
        # Only handle message created events
        if payload.get("resource") != "messages" or payload.get("event") != "created":
            return {"status": "ignored"}
        
        message_id = payload.get("data", {}).get("id")
        if not message_id:
            return {"status": "no message id"}
        
        # Get full message details
        message = await get_message_details(message_id)
        
        # Get bot info to check if message is from bot itself
        bot_info = await get_bot_info()
        bot_id = bot_info.get("id")
        
        # Ignore messages from the bot itself
        if message.get("personId") == bot_id:
            logger.debug("Ignoring message from self")
            return {"status": "ignored self"}
        
        # Get message text
        text = message.get("text", "").strip()
        room_id = message.get("roomId")
        
        if not text or not room_id:
            return {"status": "no text or room"}
        
        # Remove bot mention if present (in group spaces)
        bot_name = bot_info.get("displayName", "")
        if text.startswith(bot_name):
            text = text[len(bot_name):].strip()
        
        logger.info(f"Processing message: {text[:50]}...")
        
        # Send typing indicator (acknowledged message)
        await send_webex_message(room_id, "Processing your request...")
        
        # Call orchestrator
        response = await call_orchestrator(text)
        
        # Format response with markdown
        markdown_response = f"**AgentSwarm Response:**\n\n{response}"
        
        # Send response back to Webex
        await send_webex_message(room_id, response, markdown_response)
        
        return {"status": "processed"}
        
    except Exception as e:
        logger.error(f"Webhook error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy", "service": "AgentSwarm Webex Bot"}

@app.get("/")
async def root():
    """Bot info endpoint."""
    try:
        bot_info = await get_bot_info()
        return {
            "service": "AgentSwarm Webex Bot",
            "bot_name": bot_info.get("displayName"),
            "bot_email": bot_info.get("emails", [""])[0],
            "status": "ready",
            "webhook_url": "/webhook"
        }
    except Exception as e:
        return {
            "service": "AgentSwarm Webex Bot",
            "status": "error",
            "error": str(e)
        }

if __name__ == "__main__":
    print("=" * 60)
    print(" AgentSwarm Webex Bot")
    print("=" * 60)
    
    if not WEBEX_BOT_TOKEN:
        print(" [ERROR] WEBEX_BOT_TOKEN not set in .env!")
        print(" Get one at: https://developer.webex.com/my-apps")
        sys.exit(1)
    
    print(" Starting bot server on port 5000...")
    print(" Webhook URL: http://localhost:5000/webhook")
    print("")
    print(" To expose to internet, use ngrok:")
    print("   ngrok http 5000")
    print("=" * 60)
    
    uvicorn.run(app, host="0.0.0.0", port=5000)

