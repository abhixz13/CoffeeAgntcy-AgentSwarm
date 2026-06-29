# Copyright AGNTCY Contributors (https://github.com/agntcy)
# SPDX-License-Identifier: Apache-2.0
# AgentSwarm - Knowledge Base Agent Logic

import logging
from langchain_core.messages import AIMessage
from langchain_core.prompts import PromptTemplate

from agntcy_app_sdk.factory import AgntcyFactory
from ioa_observe.sdk.decorators import agent

from config.config import DEFAULT_MESSAGE_TRANSPORT, TRANSPORT_SERVER_ENDPOINT
from common.llm import get_llm

logger = logging.getLogger("agentswarm.knowledge_agent")

# Initialize factory with tracing
factory = AgntcyFactory("agentswarm.knowledge", enable_tracing=True)

@agent(name="knowledge_agent")
class KnowledgeAgent:
    """
    Knowledge Base Agent - Answers customer FAQs and provides troubleshooting steps.
    Simulated knowledge base for hackathon demo.
    """
    
    def __init__(self):
        """Initialize the Knowledge Agent with LLM."""
        self.llm = None
        logger.info("Knowledge Agent initialized")
    
    async def process(self, user_message: str) -> str:
        """
        Process customer query and return knowledge base answer.
        
        Args:
            user_message: Customer's question
            
        Returns:
            str: Answer from knowledge base
        """
        if not self.llm:
            self.llm = get_llm()
        
        logger.info(f"Knowledge Agent processing query: {user_message}")
        
        # Prompt with simulated knowledge base context
        prompt = PromptTemplate(
            template="""You are a knowledgeable technical support agent with access to a comprehensive knowledge base.

Customer Question: {user_message}

Provide a helpful, accurate answer including:
1. Direct solution or answer
2. Step-by-step troubleshooting if applicable
3. Any relevant tips or warnings

Knowledge Base Context (Simulated for Demo):
- Password Reset: Go to Settings > Account > Reset Password, click "Forgot Password", check email for reset link
- Slow Internet: 1) Restart router/modem, 2) Check for bandwidth-heavy apps, 3) Run speed test, 4) Contact ISP if issues persist  
- Router Config: Access router at 192.168.1.1, default login: admin/admin, configure via web interface
- Support Hours: 24/7 for critical issues, 9AM-5PM PT for general support
- VPN Setup: Download VPN client, install, login with credentials, connect to preferred server
- Email Issues: Check spam folder, verify server settings (IMAP: mail.example.com:993, SMTP: mail.example.com:587)

Be concise but thorough. If the question isn't in the knowledge base, provide general guidance and suggest contacting specialist support.

Answer:""",
            input_variables=["user_message"]
        )
        
        chain = prompt | self.llm
        response = await chain.ainvoke({"user_message": user_message})
        
        answer = response.content.strip()
        logger.info(f"Knowledge Agent generated answer: {answer[:100]}...")
        
        return answer
    
    async def ainvoke(self, messages: list) -> AIMessage:
        """
        Standard A2A interface - processes messages and returns AIMessage.
        
        Args:
            messages: List of conversation messages
            
        Returns:
            AIMessage: Response message
        """
        # Extract last user message
        user_message = messages[-1].content if messages else "No message provided"
        
        # Process and get answer
        answer = await self.process(user_message)
        
        return AIMessage(content=answer)


