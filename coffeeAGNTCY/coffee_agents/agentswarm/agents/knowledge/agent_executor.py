# Copyright AGNTCY Contributors (https://github.com/agntcy)
# SPDX-License-Identifier: Apache-2.0
# AgentSwarm - Knowledge Agent Executor

import logging
from a2a.server.request_handlers import DefaultAgentExecutor
from a2a.types import Message
from agents.knowledge.agent import KnowledgeAgent

logger = logging.getLogger("agentswarm.knowledge_agent.executor")

class KnowledgeAgentExecutor(DefaultAgentExecutor):
    """
    Executor for Knowledge Agent - handles A2A message processing.
    """
    
    def __init__(self):
        """Initialize with Knowledge Agent instance."""
        self.agent = KnowledgeAgent()
        logger.info("Knowledge Agent Executor initialized")
    
    async def execute(self, message: Message) -> Message:
        """
        Execute agent logic and return response message.
        
        Args:
            message: Incoming A2A message
            
        Returns:
            Message: Response message
        """
        try:
            logger.info(f"Executing Knowledge Agent for message: {message.messageId}")
            
            # Convert A2A message to LangChain format
            from langchain_core.messages import HumanMessage
            lc_messages = [HumanMessage(content=part.root.text) for part in message.parts if hasattr(part.root, 'text')]
            
            # Process through agent
            response = await self.agent.ainvoke(lc_messages)
            
            # Convert back to A2A message format
            from a2a.types import Part, TextPart
            response_message = Message(
                messageId=message.messageId,
                role=message.role,
                parts=[Part(TextPart(text=response.content))]
            )
            
            logger.info("Knowledge Agent execution completed successfully")
            return response_message
            
        except Exception as e:
            logger.error(f"Error in Knowledge Agent execution: {e}", exc_info=True)
            # Return error message
            from a2a.types import Part, TextPart
            error_message = Message(
                messageId=message.messageId,
                role=message.role,
                parts=[Part(TextPart(text=f"Knowledge Agent Error: Unable to process request. {str(e)}"))]
            )
            return error_message


