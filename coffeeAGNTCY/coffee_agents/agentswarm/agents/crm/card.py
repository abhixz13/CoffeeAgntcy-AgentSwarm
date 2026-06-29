# Copyright AGNTCY Contributors (https://github.com/agntcy)
# SPDX-License-Identifier: Apache-2.0
# AgentSwarm - CRM Agent Card

from a2a.types import (
    AgentCapabilities, 
    AgentCard,
    AgentSkill
)

AGENT_SKILL = AgentSkill(
    id="lookup_customer",
    name="Customer Lookup",
    description="Retrieves customer information including account history, subscription tier, and past support interactions.",
    tags=["crm", "customer", "account", "history"],
    examples=[
        "Look up customer account for order #12345",
        "What is the customer's subscription tier?",
        "Show customer interaction history",
        "Is this customer a premium account?",
    ]
)   

AGENT_CARD = AgentCard(
    name='CRM Agent',
    id='crm-agent',
    description='AI agent that retrieves customer information, account details, subscription tiers, and interaction history from CRM system.',
    url='',
    version='1.0.0',
    defaultInputModes=["text"],
    defaultOutputModes=["text"],
    capabilities=AgentCapabilities(streaming=True),
    skills=[AGENT_SKILL],
    supportsAuthenticatedExtendedCard=False,
)


