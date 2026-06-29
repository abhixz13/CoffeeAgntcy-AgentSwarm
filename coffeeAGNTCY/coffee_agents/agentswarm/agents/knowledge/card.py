# Copyright AGNTCY Contributors (https://github.com/agntcy)
# SPDX-License-Identifier: Apache-2.0
# AgentSwarm - Knowledge Base Agent Card

from a2a.types import (
    AgentCapabilities, 
    AgentCard,
    AgentSkill
)

AGENT_SKILL = AgentSkill(
    id="answer_faq",
    name="Answer FAQ",
    description="Answers customer questions from knowledge base with troubleshooting steps and solutions.",
    tags=["support", "knowledge", "faq", "troubleshooting"],
    examples=[
        "How do I reset my password?",
        "My internet is slow, what should I do?",
        "How to configure my router?",
        "What are your support hours?",
    ]
)   

AGENT_CARD = AgentCard(
    name='Knowledge Base Agent',
    id='knowledge-agent',
    description='AI agent that retrieves documentation, troubleshooting steps, and FAQ answers for customer support.',
    url='',
    version='1.0.0',
    defaultInputModes=["text"],
    defaultOutputModes=["text"],
    capabilities=AgentCapabilities(streaming=True),
    skills=[AGENT_SKILL],
    supportsAuthenticatedExtendedCard=False,
)


