# Copyright AGNTCY Contributors (https://github.com/agntcy)
# SPDX-License-Identifier: Apache-2.0
# AgentSwarm - Ticket Agent Logic

import logging
import random
from langchain_core.messages import AIMessage
from langchain_core.prompts import PromptTemplate

from agntcy_app_sdk.factory import AgntcyFactory
from ioa_observe.sdk.decorators import agent

from config.config import DEFAULT_MESSAGE_TRANSPORT, TRANSPORT_SERVER_ENDPOINT
from common.llm import get_llm

logger = logging.getLogger("agentswarm.ticket_agent")

factory = AgntcyFactory("agentswarm.ticket", enable_tracing=True)

@agent(name="ticket_agent")
class TicketAgent:
    """
    Ticket Agent - Creates and manages support tickets with priority assessment.
    Simulated ticketing system for hackathon demo.
    """
    
    def __init__(self):
        """Initialize the Ticket Agent with LLM."""
        self.llm = None
        logger.info("Ticket Agent initialized")
    
    async def process(self, user_message: str) -> str:
        """
        Create or lookup support tickets.
        
        Args:
            user_message: Ticket request or query
            
        Returns:
            str: Ticket information
        """
        if not self.llm:
            self.llm = get_llm()
        
        logger.info(f"Ticket Agent processing: {user_message}")
        
        prompt = PromptTemplate(
            template="""You are a ticketing system specialist agent.

Request: {user_message}

Analyze the request and create/lookup a support ticket. Generate realistic ticket details:

Ticket Creation Guidelines:
- Determine priority: Low, Medium, High, or Critical based on issue urgency
- Generate unique ticket ID (format: TKT-XXXXX where X is digit)
- Assign category: Network, Account, Technical, Billing, etc.
- Estimate resolution time based on priority
- Add relevant tags

Priority Assessment:
- Critical: System down, security breach, VIP customer major issue
- High: Service degraded, multiple users affected, premium customer
- Medium: Single user issue, workaround available
- Low: Enhancement request, general inquiry

Response Format:
✅ Ticket Created Successfully

Ticket ID: [TKT-XXXXX]
Priority: [Critical/High/Medium/Low]
Category: [category]
Status: Open
Created: [current timestamp]
Assigned To: [team/person based on category]
Estimated Resolution: [timeframe]

Issue Summary: [brief summary of problem]
Next Steps: [what will happen next]

If this is a status lookup, provide realistic ticket status information.

Ticket Details:""",
            input_variables=["user_message"]
        )
        
        chain = prompt | self.llm
        response = await chain.ainvoke({"user_message": user_message})
        
        ticket_info = response.content.strip()
        logger.info(f"Ticket Agent created/retrieved ticket: {ticket_info[:100]}...")
        
        return ticket_info
    
    async def ainvoke(self, messages: list) -> AIMessage:
        """Standard A2A interface."""
        user_message = messages[-1].content if messages else "No message provided"
        ticket_info = await self.process(user_message)
        return AIMessage(content=ticket_info)


