# Copyright AGNTCY Contributors (https://github.com/agntcy)
# SPDX-License-Identifier: Apache-2.0
# AgentSwarm - Escalation Agent Logic

import logging
from langchain_core.messages import AIMessage
from langchain_core.prompts import PromptTemplate

from agntcy_app_sdk.factory import AgntcyFactory
from ioa_observe.sdk.decorators import agent

from config.config import DEFAULT_MESSAGE_TRANSPORT, TRANSPORT_SERVER_ENDPOINT
from common.llm import get_llm

logger = logging.getLogger("agentswarm.escalation_agent")

factory = AgntcyFactory("agentswarm.escalation", enable_tracing=True)

@agent(name="escalation_agent")
class EscalationAgent:
    """
    Escalation Agent - Routes urgent issues to human experts.
    Simulated escalation logic for hackathon demo.
    """
    
    def __init__(self):
        """Initialize the Escalation Agent with LLM."""
        self.llm = None
        logger.info("Escalation Agent initialized")
    
    async def process(self, user_message: str) -> str:
        """
        Determine if escalation is needed and route accordingly.
        
        Args:
            user_message: Issue context and customer information
            
        Returns:
            str: Escalation decision and routing info
        """
        if not self.llm:
            self.llm = get_llm()
        
        logger.info(f"Escalation Agent analyzing: {user_message}")
        
        prompt = PromptTemplate(
            template="""You are an escalation routing specialist agent.

Context: {user_message}

Analyze the situation and determine:
1. Does this require human intervention?
2. What level of escalation is needed?
3. Which team/specialist should handle it?

Escalation Criteria:
- CRITICAL: System outages, security breaches, data loss, VIP customer major issues
- HIGH: Repeated failures (3+ issues), premium customer escalations, service degradation
- MEDIUM: Complex technical issues beyond FAQ, billing disputes, specialized requests
- LOW/NONE: Standard support queries, common issues with known solutions

Routing Teams:
- Network Engineering: Connectivity, infrastructure, outages
- Security Team: Security incidents, breaches, vulnerabilities  
- Senior Support: Complex technical issues, VIP customers
- Billing Department: Payment issues, refunds, account problems
- Product Team: Feature requests, bugs, product feedback

Response Format:
🚨 Escalation Assessment

Escalation Level: [CRITICAL/HIGH/MEDIUM/LOW/NONE]
Requires Human: [YES/NO]

Routing Decision:
Team: [team name]
Specialist Type: [role]
Priority: [Immediate/Within 1 hour/Within 4 hours/Standard]
Reason: [brief justification]

Recommended Action:
[specific next steps for human specialist]

If NO escalation needed, explain why the issue can be handled by automated agents.

Assessment:""",
            input_variables=["user_message"]
        )
        
        chain = prompt | self.llm
        response = await chain.ainvoke({"user_message": user_message})
        
        assessment = response.content.strip()
        logger.info(f"Escalation Agent assessment: {assessment[:150]}...")
        
        return assessment
    
    async def ainvoke(self, messages: list) -> AIMessage:
        """Standard A2A interface."""
        user_message = messages[-1].content if messages else "No message provided"
        assessment = await self.process(user_message)
        return AIMessage(content=assessment)


