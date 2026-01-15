# Copyright AGNTCY Contributors (https://github.com/agntcy)
# SPDX-License-Identifier: Apache-2.0
# AgentSwarm - Simple HTTP Client for Agent Communication (No Docker Required!)
# OBSERVABILITY: Records metrics for each agent call

import logging
import json
import time
import httpx
from contextlib import asynccontextmanager
from typing import Optional

from config.config import (
    KNOWLEDGE_AGENT_PORT,
    CRM_AGENT_PORT,
    TICKET_AGENT_PORT,
    ESCALATION_AGENT_PORT,
)

# OBSERVABILITY IMPORTS
from common.observability import get_metrics_collector

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
        OBSERVABILITY: Records timing and success/failure metrics.
        
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
        
        # OBSERVABILITY: Start timing
        start_time = time.time()
        metrics = get_metrics_collector()
        
        try:
            logger.info(f"[TRACE] Calling {agent_name} agent at {endpoint}")
            # #region agent log
            with open(r'c:\code\coffeeAgentify\.cursor\debug.log', 'a') as f: f.write(json.dumps({"hypothesisId":"H4","location":"http_client.py:call_agent:start","message":"Calling agent","data":{"agent":agent_name,"endpoint":endpoint,"prompt_len":len(prompt)},"timestamp":int(time.time()*1000),"sessionId":"debug-session"})+'\n')
            # #endregion
            
            # Use context manager for automatic resource cleanup
            async with self._get_client() as client:
                response = await client.post(
                    endpoint,
                    json={"prompt": prompt},
                )
                response.raise_for_status()
                data = response.json()
                result = data.get("response", "No response from agent")
                
                # OBSERVABILITY: Record successful call
                duration_ms = (time.time() - start_time) * 1000
                metrics.record_agent_call(agent_name.upper(), duration_ms, success=True)
                
                # #region agent log
                with open(r'c:\code\coffeeAgentify\.cursor\debug.log', 'a') as f: f.write(json.dumps({"hypothesisId":"H4","location":"http_client.py:call_agent:success","message":"Agent responded","data":{"agent":agent_name,"status":response.status_code,"result_len":len(result),"duration_ms":duration_ms},"timestamp":int(time.time()*1000),"sessionId":"debug-session"})+'\n')
                # #endregion
                logger.info(f"[TRACE] {agent_name} responded in {duration_ms:.1f}ms: {result[:80]}...")
                return result
            
        except httpx.ConnectError:
            # OBSERVABILITY: Record failed call
            duration_ms = (time.time() - start_time) * 1000
            metrics.record_agent_call(agent_name.upper(), duration_ms, success=False)
            logger.warning(f"[TRACE] {agent_name} agent OFFLINE at {endpoint}")
            return f"[{agent_name.upper()} AGENT OFFLINE] - Agent not available"
            
        except httpx.TimeoutException:
            # OBSERVABILITY: Record timeout
            duration_ms = (time.time() - start_time) * 1000
            metrics.record_agent_call(agent_name.upper(), duration_ms, success=False)
            logger.warning(f"[TRACE] {agent_name} agent TIMEOUT after {duration_ms:.1f}ms")
            return f"[{agent_name.upper()} AGENT TIMEOUT] - Please try again"
            
        except Exception as e:
            # OBSERVABILITY: Record error
            duration_ms = (time.time() - start_time) * 1000
            metrics.record_agent_call(agent_name.upper(), duration_ms, success=False)
            logger.error(f"[TRACE] {agent_name} agent ERROR: {e}")
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
