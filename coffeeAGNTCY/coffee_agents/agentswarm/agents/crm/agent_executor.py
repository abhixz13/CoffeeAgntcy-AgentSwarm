# Copyright AGNTCY Contributors (https://github.com/agntcy)
# SPDX-License-Identifier: Apache-2.0
# AgentSwarm - CRM Agent Executor

import logging
from a2a.server.request_handlers import DefaultAgentExecutor
from a2a.types import Message
from agents.crm.agent import CRMAgent

logger = logging.getLogger("agentswarm.crm_agent.executor")

class CRMAgentExecutor(DefaultAgentExecutor):
    """Executor for CRM Agent."""
    
    def __init__(self):
        self.agent = CRMAgent()
        logger.info("CRM Agent Executor initialized")
    
    async def execute(self, message: Message) -> Message:
        """Execute agent logic and return response message."""
        try:
            logger.info(f"Executing CRM Agent for message: {message.messageId}")
            
            from langchain_core.messages import HumanMessage
            lc_messages = [HumanMessage(content=part.root.text) for part in message.parts if hasattr(part.root, 'text')]
            
            response = await self.agent.ainvoke(lc_messages)
            
            from a2a.types import Part, TextPart
            response_message = Message(
                messageId=message.messageId,
                role=message.role,
                parts=[Part(TextPart(text=response.content))]
            )
            
            logger.info("CRM Agent execution completed successfully")
            return response_message
            
        except Exception as e:
            logger.error(f"Error in CRM Agent execution: {e}", exc_info=True)
            from a2a.types import Part, TextPart
            error_message = Message(
                messageId=message.messageId,
                role=message.role,
                parts=[Part(TextPart(text=f"CRM Agent Error: {str(e)}"))]
            )
            return error_message


