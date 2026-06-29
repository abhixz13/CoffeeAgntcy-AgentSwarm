# Copyright AGNTCY Contributors (https://github.com/agntcy)
# SPDX-License-Identifier: Apache-2.0
# AgentSwarm - Orchestrator A2A Client Tools

import logging
from uuid import uuid4
from typing import Any

from a2a.types import (
    AgentCard,
    SendMessageRequest,
    MessageSendParams,
    Message,
    Part,
    TextPart,
    Role,
)
from langchain_core.tools import tool
from ioa_observe.sdk.decorators import tool as ioa_tool_decorator

from agntcy_app_sdk.semantic.a2a.protocol import A2AProtocol
from agntcy_app_sdk.factory import AgntcyFactory

from agents.knowledge.card import AGENT_CARD as knowledge_card
from agents.crm.card import AGENT_CARD as crm_card
from agents.ticket.card import AGENT_CARD as ticket_card
from agents.escalation.card import AGENT_CARD as escalation_card

from config.config import DEFAULT_MESSAGE_TRANSPORT, TRANSPORT_SERVER_ENDPOINT

logger = logging.getLogger("agentswarm.orchestrator.tools")

# Global factory and transport
factory = AgntcyFactory("agentswarm.orchestrator", enable_tracing=True)
transport = factory.create_transport(
    DEFAULT_MESSAGE_TRANSPORT,
    endpoint=TRANSPORT_SERVER_ENDPOINT,
    name="default/default/orchestrator"
)

class AgentCommunicationError(Exception):
    """Exception for A2A communication errors."""
    pass

async def call_agent(card: AgentCard, prompt: str) -> str:
    """
    Generic function to call any A2A agent.
    
    Args:
        card: Agent card of the target agent
        prompt: Query to send to the agent
        
    Returns:
        str: Agent's response
        
    Raises:
        AgentCommunicationError: If communication fails
    """
    try:
        logger.info(f"Calling {card.name} with prompt: {prompt[:100]}...")
        
        # Create A2A client
        client = await factory.create_client(
            "A2A",
            agent_topic=A2AProtocol.create_agent_topic(card),
            transport=transport,
        )

        # Create request message
        request = SendMessageRequest(
            id=str(uuid4()),
            params=MessageSendParams(
                message=Message(
                    messageId=str(uuid4()),
                    role=Role.user,
                    parts=[Part(TextPart(text=prompt))],
                ),
            )
        )

        # Send message and get response
        response = await client.send_message(request)
        logger.info(f"Received response from {card.name}")
        
        # Extract text from response
        if response.root.result and response.root.result.parts:
            part = response.root.result.parts[0].root
            if hasattr(part, "text"):
                return part.text.strip()
            else:
                raise AgentCommunicationError(f"{card.name} returned non-text response")
        elif response.root.error:
            logger.error(f"A2A error from {card.name}: {response.root.error.message}")
            raise AgentCommunicationError(f"Error from {card.name}: {response.root.error.message}")
        else:
            logger.error(f"Unknown response type from {card.name}")
            raise AgentCommunicationError(f"Unknown response type from {card.name}")
            
    except Exception as e:
        logger.error(f"Failed to communicate with {card.name}: {e}", exc_info=True)
        raise AgentCommunicationError(f"Failed to communicate with {card.name}: {e}")


@tool
@ioa_tool_decorator(name="query_knowledge_agent")
async def query_knowledge_agent(query: str) -> str:
    """
    Query the Knowledge Agent for FAQ answers and troubleshooting steps.
    
    Args:
        query: Customer's question
        
    Returns:
        str: Knowledge base answer
    """
    logger.info(f"Tool: query_knowledge_agent - {query[:50]}...")
    return await call_agent(knowledge_card, query)


@tool
@ioa_tool_decorator(name="query_crm_agent")
async def query_crm_agent(query: str) -> str:
    """
    Query the CRM Agent for customer information and history.
    
    Args:
        query: Customer lookup query (with order number or customer ID)
        
    Returns:
        str: Customer information from CRM
    """
    logger.info(f"Tool: query_crm_agent - {query[:50]}...")
    return await call_agent(crm_card, query)


@tool
@ioa_tool_decorator(name="query_ticket_agent")
async def query_ticket_agent(query: str) -> str:
    """
    Query the Ticket Agent to create or lookup support tickets.
    
    Args:
        query: Ticket creation or lookup request
        
    Returns:
        str: Ticket information
    """
    logger.info(f"Tool: query_ticket_agent - {query[:50]}...")
    return await call_agent(ticket_card, query)


@tool
@ioa_tool_decorator(name="query_escalation_agent")
async def query_escalation_agent(query: str) -> str:
    """
    Query the Escalation Agent to determine if human intervention is needed.
    
    Args:
        query: Issue context for escalation assessment
        
    Returns:
        str: Escalation assessment and routing decision
    """
    logger.info(f"Tool: query_escalation_agent - {query[:50]}...")
    return await call_agent(escalation_card, query)


# Export all tools
ALL_TOOLS = [
    query_knowledge_agent,
    query_crm_agent,
    query_ticket_agent,
    query_escalation_agent,
]


