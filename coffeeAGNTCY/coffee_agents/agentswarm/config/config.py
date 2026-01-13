# Copyright AGNTCY Contributors (https://github.com/agntcy)
# SPDX-License-Identifier: Apache-2.0
# Adapted for AgentSwarm - Webex Contact Center Multi-Agent System

import os
from dotenv import load_dotenv

load_dotenv()  # Automatically loads from `.env` or `.env.local`

# ============================================================================
# AI Backend Selection
# ============================================================================
# Options: "circuit" (Cisco internal) or "litellm" (OpenAI, GROQ, Azure)
AI_BACKEND = os.getenv("AI_BACKEND", "litellm").lower()

# ============================================================================
# LLM Configuration (for LiteLLM backend)
# ============================================================================
LLM_MODEL = os.getenv("LLM_MODEL", "groq/llama-3.3-70b-versatile")

# ============================================================================
# Cisco CIRCUIT API Configuration (for circuit backend)
# ============================================================================
# Get credentials from CIRCUIT API Portal (VPN required)
# Free tier: gpt-4o-mini (30 req/min) or gpt-4.1 (15 req/min)
CIRCUIT_CLIENT_ID = os.getenv("CIRCUIT_CLIENT_ID", "")
CIRCUIT_CLIENT_SECRET = os.getenv("CIRCUIT_CLIENT_SECRET", "")
CIRCUIT_APPKEY = os.getenv("CIRCUIT_APPKEY", "")
CIRCUIT_MODEL = os.getenv("CIRCUIT_MODEL", "gpt-4o-mini")

# ============================================================================
# AGNTCY Transport Configuration
# ============================================================================
DEFAULT_MESSAGE_TRANSPORT = os.getenv("DEFAULT_MESSAGE_TRANSPORT", "SLIM")
TRANSPORT_SERVER_ENDPOINT = os.getenv("TRANSPORT_SERVER_ENDPOINT", "http://localhost:46357")

# ============================================================================
# Webex Configuration
# ============================================================================
WEBEX_BOT_TOKEN = os.getenv("WEBEX_BOT_TOKEN", "")
WEBEX_BOT_EMAIL = os.getenv("WEBEX_BOT_EMAIL", "")
WEBEX_WEBHOOK_URL = os.getenv("WEBEX_WEBHOOK_URL", "http://localhost:8000/webhooks/webex")
WEBEX_ROOM_ID = os.getenv("WEBEX_ROOM_ID", "")  # For testing
BOT_QUEUE_NAME = os.getenv("BOT_QUEUE_NAME", "")  # For Bot Gateway

# ============================================================================
# Observability Configuration
# ============================================================================
OTLP_HTTP_ENDPOINT = os.getenv("OTLP_HTTP_ENDPOINT", "http://localhost:4318")
LOGGING_LEVEL = os.getenv("LOGGING_LEVEL", "INFO").upper()

# ============================================================================
# AgentSwarm Specific Configuration
# ============================================================================
ORCHESTRATOR_PORT = int(os.getenv("ORCHESTRATOR_PORT", "8000"))
KNOWLEDGE_AGENT_PORT = int(os.getenv("KNOWLEDGE_AGENT_PORT", "8001"))
CRM_AGENT_PORT = int(os.getenv("CRM_AGENT_PORT", "8002"))
TICKET_AGENT_PORT = int(os.getenv("TICKET_AGENT_PORT", "8003"))
ESCALATION_AGENT_PORT = int(os.getenv("ESCALATION_AGENT_PORT", "8004"))

# Enable HTTP for local development
ENABLE_HTTP = os.getenv("ENABLE_HTTP", "true").lower() in ("true", "1", "yes")
