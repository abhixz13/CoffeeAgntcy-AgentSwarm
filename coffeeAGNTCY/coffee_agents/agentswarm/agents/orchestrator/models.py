# Copyright AGNTCY Contributors (https://github.com/agntcy)
# SPDX-License-Identifier: Apache-2.0
# AgentSwarm - Orchestrator Models

from typing import Literal
from pydantic import BaseModel, Field
from langgraph.graph import MessagesState

# Pydantic models for tool arguments
class AgentQueryArgs(BaseModel):
    """Arguments for querying specialist agents."""
    query: str = Field(description="The query to send to the agent")

# Graph state
class OrchestratorState(MessagesState):
    """
    State passed between nodes in the orchestrator graph.
    Extends MessagesState with custom fields.
    """
    next_node: str = ""
    intent: str = ""  # faq, customer_lookup, ticket, escalation, general
    knowledge_response: str = ""
    crm_response: str = ""
    ticket_response: str = ""
    escalation_response: str = ""
    final_response: str = ""

# Node names as constants
class NodeNames:
    """Node identifiers for the orchestrator graph."""
    SUPERVISOR = "supervisor"
    KNOWLEDGE = "knowledge_node"
    CRM = "crm_node"
    TICKET = "ticket_node"
    ESCALATION = "escalation_node"
    AGGREGATOR = "aggregator_node"
    GENERAL = "general_node"

# Intent types
class IntentType:
    """Customer query intent classifications."""
    FAQ = "faq"
    CUSTOMER_LOOKUP = "customer_lookup"
    TICKET = "ticket"
    ESCALATION = "escalation"
    GENERAL = "general"


