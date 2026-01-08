# Copyright AGNTCY Contributors (https://github.com/agntcy)
# SPDX-License-Identifier: Apache-2.0
# AgentSwarm - Escalation Agent Card

from a2a.types import (
    AgentCapabilities, 
    AgentCard,
    AgentSkill
)

AGENT_SKILL = AgentSkill(
    id="route_escalation",
    name="Escalation Routing",
    description="Identifies issues requiring human intervention and routes to appropriate specialists based on urgency and complexity.",
    tags=["escalation", "routing", "specialist", "urgent"],
    examples=[
        "Escalate this critical outage to engineering",
        "Route to senior support specialist",
        "This needs immediate attention from security team",
        "Transfer to billing department manager",
    ]
)   

AGENT_CARD = AgentCard(
    name='Escalation Agent',
    id='escalation-agent',
    description='AI agent that detects patterns requiring escalation and routes urgent issues to appropriate human experts.',
    url='',
    version='1.0.0',
    defaultInputModes=["text"],
    defaultOutputModes=["text"],
    capabilities=AgentCapabilities(streaming=True),
    skills=[AGENT_SKILL],
    supportsAuthenticatedExtendedCard=False,
)


