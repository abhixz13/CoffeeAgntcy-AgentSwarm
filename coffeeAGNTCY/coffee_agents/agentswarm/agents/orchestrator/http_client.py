# Copyright AGNTCY Contributors (https://github.com/agntcy)
# SPDX-License-Identifier: Apache-2.0
# AgentSwarm - Simple HTTP Client for Agent Communication (No Docker Required!)

import logging
import httpx
from contextlib import asynccontextmanager
from typing import Optional

from config.config import (
    KNOWLEDGE_AGENT_PORT,
    CRM_AGENT_PORT,
    TICKET_AGENT_PORT,
    ESCALATION_AGENT_PORT,
)

logger = logging.getLogger("agentswarm.orchestrator.http_client")

# Agent endpoints
AGENT_ENDPOINTS = {
    "knowledge": f"http://localhost:{KNOWLEDGE_AGENT_PORT}/process",
    "crm": f"http://localhost:{CRM_AGENT_PORT}/process",
    "ticket": f"http://localhost:{TICKET_AGENT_PORT}/process",
    "escalation": f"http://localhost:{ESCALATION_AGENT_PORT}/process",
}

# Default timeout
DEFAULT_TIMEOUT = 30.0


class HTTPAgentClient:
    """
    Simple HTTP client for calling specialist agents.
    Uses per-request client creation to avoid resource leaks.
    """
    
    def __init__(self, timeout: float = DEFAULT_TIMEOUT):
        """Initialize client configuration (no resources allocated yet)."""
        self.timeout = timeout
    
    @asynccontextmanager
    async def _get_client(self):
        """Context manager for HTTP client - ensures proper cleanup."""
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            yield client
    
    async def call_agent(self, agent_name: str, prompt: str) -> str:
        """
        Call a specialist agent via HTTP.
        
        Args:
            agent_name: Name of agent (knowledge, crm, ticket, escalation)
            prompt: Query to send
            
        Returns:
            str: Agent's response
        """
        endpoint = AGENT_ENDPOINTS.get(agent_name)
        if not endpoint:
            logger.error(f"Unknown agent: {agent_name}")
            return f"Error: Unknown agent '{agent_name}'"
        
        try:
            logger.info(f"Calling {agent_name} agent at {endpoint}")
            
            # Use context manager for automatic resource cleanup
            async with self._get_client() as client:
                response = await client.post(
                    endpoint,
                    json={"prompt": prompt},
                )
                response.raise_for_status()
                data = response.json()
                result = data.get("response", "No response from agent")
                logger.info(f"{agent_name} agent responded: {result[:100]}...")
                return result
            
        except httpx.ConnectError:
            logger.warning(f"{agent_name} agent not running at {endpoint}")
            return f"[{agent_name.upper()} AGENT OFFLINE] - Agent not available"
            
        except httpx.TimeoutException:
            logger.warning(f"{agent_name} agent timed out")
            return f"[{agent_name.upper()} AGENT TIMEOUT] - Please try again"
            
        except Exception as e:
            logger.error(f"Error calling {agent_name}: {e}")
            return f"[{agent_name.upper()} AGENT ERROR] - {str(e)}"
    
    async def query_knowledge(self, prompt: str) -> str:
        """Query Knowledge Agent for FAQ answers."""
        return await self.call_agent("knowledge", prompt)
    
    async def query_crm(self, prompt: str) -> str:
        """Query CRM Agent for customer information."""
        return await self.call_agent("crm", prompt)
    
    async def query_ticket(self, prompt: str) -> str:
        """Query Ticket Agent to create/lookup tickets."""
        return await self.call_agent("ticket", prompt)
    
    async def query_escalation(self, prompt: str) -> str:
        """Query Escalation Agent for routing decisions."""
        return await self.call_agent("escalation", prompt)


# Singleton instance (lightweight - no resources held)
_client: Optional[HTTPAgentClient] = None

def get_http_client() -> HTTPAgentClient:
    """Get or create the HTTP client singleton."""
    global _client
    if _client is None:
        _client = HTTPAgentClient()
    return _client
