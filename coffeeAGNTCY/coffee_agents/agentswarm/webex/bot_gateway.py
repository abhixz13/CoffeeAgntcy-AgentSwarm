# Copyright AGNTCY Contributors (https://github.com/agntcy)
# SPDX-License-Identifier: Apache-2.0
# AgentSwarm - Webex Bot using Cisco Bot Gateway (RabbitMQ)
# No ngrok or public webhooks required!

"""
SETUP INSTRUCTIONS:
1. Go to https://scripts.cisco.com/app/quicker_bots/
2. Add your bot token to create a listener
3. Run this script - it will consume messages from RabbitMQ
"""

import json
import ssl
import logging
import sys
import os
import asyncio

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
load_dotenv()

import pika
import httpx

from config.config import WEBEX_BOT_TOKEN, ORCHESTRATOR_PORT
from config.logging_config import setup_logging

setup_logging()
logger = logging.getLogger("agentswarm.webex.bot_gateway")

# Cisco Bot Gateway RabbitMQ Settings (Ascension AMQP aaS)
RMQ_HOST = "ascension-amqp-aas.cisco.com"
RMQ_PORT = 5671
RMQ_USER = "bot"
RMQ_PW = "Cisc0123$"
RMQ_VHOST = "Webex-Teams-Bot-Gateway"

# Webex API
WEBEX_API_URL = "https://webexapis.com/v1"


def get_bot_info() -> dict:
    """Get bot's own information."""
    response = httpx.get(
        f"{WEBEX_API_URL}/people/me",
        headers={"Authorization": f"Bearer {WEBEX_BOT_TOKEN}"}
    )
    response.raise_for_status()
    return response.json()


def send_webex_message(room_id: str, text: str):
    """Send a message to a Webex room."""
    response = httpx.post(
        f"{WEBEX_API_URL}/messages",
        headers={
            "Authorization": f"Bearer {WEBEX_BOT_TOKEN}",
            "Content-Type": "application/json"
        },
        json={"roomId": room_id, "text": text}
    )
    response.raise_for_status()
    logger.info(f"Message sent to room {room_id[:20]}...")
    return response.json()


def call_orchestrator_sync(prompt: str) -> str:
    """Call AgentSwarm Orchestrator synchronously."""
    try:
        response = httpx.post(
            f"http://localhost:{ORCHESTRATOR_PORT}/agent/prompt",
            json={"prompt": prompt},
            timeout=60.0
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


def main():
    """Main function - consume messages from RabbitMQ Bot Gateway."""
    print("=" * 60)
    print(" AgentSwarm Webex Bot (Cisco Bot Gateway)")
    print("=" * 60)
    
    if not WEBEX_BOT_TOKEN:
        print(" [ERROR] WEBEX_BOT_TOKEN not set in .env!")
        print(" Get one at: https://developer.webex.com/my-apps")
        sys.exit(1)
    
    # Get bot info
    print("\nGetting bot info...")
    bot_info = get_bot_info()
    bot_id = bot_info.get("id")
    bot_name = bot_info.get("displayName", "")
    bot_email = bot_info.get("emails", [""])[0]
    
    print(f" Bot Name: {bot_name}")
    print(f" Bot Email: {bot_email}")
    
    # Queue name is bot's display name (lowercase, spaces -> hyphens)
    queue_name = bot_name.lower().replace(" ", "-")
    print(f" Queue Name: {queue_name}")
    
    print("\n" + "=" * 60)
    print(" IMPORTANT: Register your bot first!")
    print(" Go to: https://scripts.cisco.com/app/quicker_bots/")
    print(" Add your bot token to create a listener")
    print("=" * 60)
    
    # Setup SSL/TLS for RabbitMQ
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE
    
    print(f"\nConnecting to RabbitMQ at {RMQ_HOST}:{RMQ_PORT}...")
    
    try:
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=RMQ_HOST,
                port=RMQ_PORT,
                virtual_host=RMQ_VHOST,
                credentials=pika.PlainCredentials(RMQ_USER, RMQ_PW),
                ssl_options=pika.SSLOptions(context),
                heartbeat=600
            )
        )
        channel = connection.channel()
        
        print(f" Connected! Listening to queue: {queue_name}")
        print("\n" + "=" * 60)
        print(" Bot is ready! Send a message in Webex to test.")
        print(" Press Ctrl+C to stop.")
        print("=" * 60 + "\n")
        
        def callback(ch, method, properties, body):
            """Process incoming messages from RabbitMQ."""
            try:
                payload = json.loads(body.decode("utf-8"))
                
                # Only process new messages (not from bot itself)
                if payload.get("resource") == "messages":
                    data = payload.get("data", {})
                    person_id = data.get("personId")
                    room_id = data.get("roomId")
                    text = data.get("text", "").strip()
                    
                    # Ignore messages from the bot itself
                    if person_id == bot_id:
                        return
                    
                    # Remove bot mention if present
                    if text.startswith(bot_name):
                        text = text[len(bot_name):].strip()
                    
                    if not text or not room_id:
                        return
                    
                    logger.info(f"Received message: {text[:50]}...")
                    
                    # Send acknowledgment
                    send_webex_message(room_id, "Processing your request...")
                    
                    # Call orchestrator
                    response = call_orchestrator_sync(text)
                    
                    # Send response
                    send_webex_message(room_id, response)
                    logger.info("Response sent!")
                    
            except Exception as e:
                logger.error(f"Error processing message: {e}", exc_info=True)
        
        # Start consuming messages
        channel.basic_consume(
            queue=queue_name,
            on_message_callback=callback,
            auto_ack=True
        )
        channel.start_consuming()
        
    except pika.exceptions.ProbableAuthenticationError:
        print("\n[ERROR] Authentication failed!")
        print("Make sure you've registered your bot at:")
        print("  https://scripts.cisco.com/app/quicker_bots/")
        sys.exit(1)
    except pika.exceptions.AMQPConnectionError as e:
        print(f"\n[ERROR] Could not connect to RabbitMQ: {e}")
        print("Make sure you're on Cisco VPN and bot is registered.")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n\nShutting down...")
        connection.close()
        print("Done!")


if __name__ == "__main__":
    main()

