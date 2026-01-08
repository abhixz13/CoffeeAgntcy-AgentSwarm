# Copyright AGNTCY Contributors (https://github.com/agntcy)
# SPDX-License-Identifier: Apache-2.0
# AgentSwarm - Ticket Agent Executor

import logging
from a2a.server.request_handlers import DefaultAgentExecutor
from a2a.types import Message
from agents.ticket.agent import TicketAgent

logger = logging.getLogger("agentswarm.ticket_agent.executor")

class TicketAgentExecutor(DefaultAgentExecutor):
    """Executor for Ticket Agent."""
    
    def __init__(self):
        self.agent = TicketAgent()
        logger.info("Ticket Agent Executor initialized")
    
    async def execute(self, message: Message) -> Message:
        """Execute agent logic and return response message."""
        try:
            logger.info(f"Executing Ticket Agent for message: {message.messageId}")
            
            from langchain_core.messages import HumanMessage
            lc_messages = [HumanMessage(content=part.root.text) for part in message.parts if hasattr(part.root, 'text')]
            
            response = await self.agent.ainvoke(lc_messages)
            
            from a2a.types import Part, TextPart
            response_message = Message(
                messageId=message.messageId,
                role=message.role,
                parts=[Part(TextPart(text=response.content))]
            )
            
            logger.info("Ticket Agent execution completed successfully")
            return response_message
            
        except Exception as e:
            logger.error(f"Error in Ticket Agent execution: {e}", exc_info=True)
            from a2a.types import Part, TextPart
            error_message = Message(
                messageId=message.messageId,
                role=message.role,
                parts=[Part(TextPart(text=f"Ticket Agent Error: {str(e)}"))]
            )
            return error_message


