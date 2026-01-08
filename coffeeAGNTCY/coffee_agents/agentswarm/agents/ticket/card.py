# Copyright AGNTCY Contributors (https://github.com/agntcy)
# SPDX-License-Identifier: Apache-2.0
# AgentSwarm - Ticket Agent Card

from a2a.types import (
    AgentCapabilities, 
    AgentCard,
    AgentSkill
)

AGENT_SKILL = AgentSkill(
    id="manage_ticket",
    name="Ticket Management",
    description="Creates, updates, and prioritizes support tickets based on customer issues and urgency.",
    tags=["ticket", "support", "priority", "tracking"],
    examples=[
        "Create a support ticket for internet outage",
        "What's the status of ticket #789?",
        "Prioritize this ticket as urgent",
        "Create high priority ticket for VIP customer",
    ]
)   

AGENT_CARD = AgentCard(
    name='Ticket Agent',
    id='ticket-agent',
    description='AI agent that creates, tracks, and prioritizes support tickets with automatic urgency assessment.',
    url='',
    version='1.0.0',
    defaultInputModes=["text"],
    defaultOutputModes=["text"],
    capabilities=AgentCapabilities(streaming=True),
    skills=[AGENT_SKILL],
    supportsAuthenticatedExtendedCard=False,
)


