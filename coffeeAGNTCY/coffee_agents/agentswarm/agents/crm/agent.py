# Copyright AGNTCY Contributors (https://github.com/agntcy)
# SPDX-License-Identifier: Apache-2.0
# AgentSwarm - CRM Agent Logic

import logging
from langchain_core.messages import AIMessage
from langchain_core.prompts import PromptTemplate

from agntcy_app_sdk.factory import AgntcyFactory
from ioa_observe.sdk.decorators import agent

from config.config import DEFAULT_MESSAGE_TRANSPORT, TRANSPORT_SERVER_ENDPOINT
from common.llm import get_llm

logger = logging.getLogger("agentswarm.crm_agent")

factory = AgntcyFactory("agentswarm.crm", enable_tracing=True)

@agent(name="crm_agent")
class CRMAgent:
    """
    CRM Agent - Retrieves customer information and interaction history.
    Simulated CRM data for hackathon demo.
    """
    
    def __init__(self):
        """Initialize the CRM Agent with LLM."""
        self.llm = None
        logger.info("CRM Agent initialized")
    
    async def process(self, user_message: str) -> str:
        """
        Lookup customer information from CRM system.
        
        Args:
            user_message: Query with customer identifier
            
        Returns:
            str: Customer information from CRM
        """
        if not self.llm:
            self.llm = get_llm()
        
        logger.info(f"CRM Agent processing query: {user_message}")
        
        prompt = PromptTemplate(
            template="""You are a CRM specialist agent with access to customer database.

Query: {user_message}

Analyze the query and provide relevant customer information. Use the simulated CRM data below:

CRM Database (Simulated for Demo):
- Order #12345: Customer John Doe, Premium tier, Account since 2020, 3 recent issues (slow internet, billing question, router config)
- Order #67890: Customer Jane Smith, Standard tier, Account since 2023, 1 recent issue (password reset)
- Order #11111: Customer Bob Johnson, Enterprise tier, Account since 2019, VIP support, 5 recent interactions, all resolved
- General lookup: Extract customer ID/order number from query and provide relevant details

Response Format:
- Customer Name: [name]
- Subscription Tier: [Standard/Premium/Enterprise]
- Account Since: [year]
- Recent Issues: [count and brief summary]
- Priority Level: [Standard/Priority/VIP]
- Support Notes: [relevant context]

If order/customer not found in simulated data, generate realistic sample data maintaining consistency.

Customer Information:""",
            input_variables=["user_message"]
        )
        
        chain = prompt | self.llm
        response = await chain.ainvoke({"user_message": user_message})
        
        info = response.content.strip()
        logger.info(f"CRM Agent retrieved customer info: {info[:100]}...")
        
        return info
    
    async def ainvoke(self, messages: list) -> AIMessage:
        """
        Standard A2A interface.
        
        Args:
            messages: List of conversation messages
            
        Returns:
            AIMessage: Response message
        """
        user_message = messages[-1].content if messages else "No message provided"
        info = await self.process(user_message)
        return AIMessage(content=info)


