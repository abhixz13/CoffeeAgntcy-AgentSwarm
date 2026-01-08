# Copyright AGNTCY Contributors (https://github.com/agntcy)
# SPDX-License-Identifier: Apache-2.0
# Adapted for AgentSwarm - Webex Contact Center Multi-Agent System

import os
from dotenv import load_dotenv

load_dotenv()  # Automatically loads from `.env` or `.env.local`

# ============================================================================
# AGNTCY Transport Configuration
# ============================================================================
DEFAULT_MESSAGE_TRANSPORT = os.getenv("DEFAULT_MESSAGE_TRANSPORT", "SLIM")
TRANSPORT_SERVER_ENDPOINT = os.getenv("TRANSPORT_SERVER_ENDPOINT", "http://localhost:46357")

# ============================================================================
# LLM Configuration
# ============================================================================
LLM_MODEL = os.getenv("LLM_MODEL", "groq/llama-3.3-70b-versatile")

# OAuth2 OpenAI Provider (if using custom endpoint)
OAUTH2_CLIENT_ID = os.getenv("OAUTH2_CLIENT_ID", "")
OAUTH2_CLIENT_SECRET = os.getenv("OAUTH2_CLIENT_SECRET", "")
OAUTH2_TOKEN_URL = os.getenv("OAUTH2_TOKEN_URL", "")
OAUTH2_BASE_URL = os.getenv("OAUTH2_BASE_URL", "")
OAUTH2_APPKEY = os.getenv("OAUTH2_APPKEY", "")

# ============================================================================
# Webex Configuration
# ============================================================================
WEBEX_BOT_TOKEN = os.getenv("WEBEX_BOT_TOKEN", "")
WEBEX_BOT_EMAIL = os.getenv("WEBEX_BOT_EMAIL", "")
WEBEX_WEBHOOK_URL = os.getenv("WEBEX_WEBHOOK_URL", "http://localhost:8000/webhooks/webex")
WEBEX_ROOM_ID = os.getenv("WEBEX_ROOM_ID", "")  # For testing

# ============================================================================
# Observability Configuration
# ============================================================================
OTLP_HTTP_ENDPOINT = os.getenv("OTLP_HTTP_ENDPOINT", "http://localhost:4318")
LOGGING_LEVEL = os.getenv("LOGGING_LEVEL", "INFO").upper()

# ============================================================================
# Identity & Security Configuration (Optional for hackathon)
# ============================================================================
IDENTITY_AUTH_ENABLED = os.getenv("IDENTITY_AUTH_ENABLED", "false").lower() in ("true", "1", "yes")
IDENTITY_API_KEY = os.getenv("IDENTITY_API_KEY", "")
IDENTITY_API_SERVER_URL = os.getenv("IDENTITY_API_SERVER_URL", "https://api.agent-identity.outshift.com")

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


