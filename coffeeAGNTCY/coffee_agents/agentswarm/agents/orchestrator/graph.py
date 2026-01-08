# Copyright AGNTCY Contributors (https://github.com/agntcy)
# SPDX-License-Identifier: Apache-2.0
# AgentSwarm - Orchestrator LangGraph

import logging
from langchain_core.messages import AIMessage, SystemMessage
from langchain_core.prompts import PromptTemplate
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode

from ioa_observe.sdk.decorators import agent, graph

from agents.orchestrator.models import OrchestratorState, NodeNames, IntentType
from agents.orchestrator.tools import (
    query_knowledge_agent,
    query_crm_agent,
    query_ticket_agent,
    query_escalation_agent,
    ALL_TOOLS,
)
from common.llm import get_llm

logger = logging.getLogger("agentswarm.orchestrator.graph")

@agent(name="orchestrator_agent")
class OrchestratorGraph:
    """
    Orchestrator Agent - Supervisor that coordinates all specialist agents.
    Uses LangGraph to manage multi-agent workflow.
    """
    
    def __init__(self):
        """Initialize the orchestrator with LangGraph workflow."""
        self.supervisor_llm = None
        self.aggregator_llm = None
        self.graph = self.build_graph()
        logger.info("Orchestrator Graph initialized")
    
    @graph(name="orchestrator_graph")
    def build_graph(self):
        """
        Build the LangGraph workflow for orchestration.
        
        Workflow:
        1. Supervisor: Analyze intent
        2. Route to appropriate specialist agent(s)
        3. Aggregator: Combine responses
        4. Return final answer
        """
        workflow = StateGraph(OrchestratorState)
        
        # Add nodes
        workflow.add_node(NodeNames.SUPERVISOR, self._supervisor_node)
        workflow.add_node(NodeNames.KNOWLEDGE, self._knowledge_node)
        workflow.add_node(NodeNames.CRM, self._crm_node)
        workflow.add_node(NodeNames.TICKET, self._ticket_node)
        workflow.add_node(NodeNames.ESCALATION, self._escalation_node)
        workflow.add_node(NodeNames.AGGREGATOR, self._aggregator_node)
        workflow.add_node(NodeNames.GENERAL, self._general_node)
        
        # Set entry point
        workflow.set_entry_point(NodeNames.SUPERVISOR)
        
        # Add conditional edges from supervisor
        workflow.add_conditional_edges(
            NodeNames.SUPERVISOR,
            self._route_based_on_intent,
            {
                IntentType.FAQ: NodeNames.KNOWLEDGE,
                IntentType.CUSTOMER_LOOKUP: NodeNames.CRM,
                IntentType.TICKET: NodeNames.TICKET,
                IntentType.ESCALATION: NodeNames.ESCALATION,
                IntentType.GENERAL: NodeNames.GENERAL,
            }
        )
        
        # All specialist nodes go to aggregator
        workflow.add_edge(NodeNames.KNOWLEDGE, NodeNames.AGGREGATOR)
        workflow.add_edge(NodeNames.CRM, NodeNames.AGGREGATOR)
        workflow.add_edge(NodeNames.TICKET, NodeNames.AGGREGATOR)
        workflow.add_edge(NodeNames.ESCALATION, NodeNames.AGGREGATOR)
        workflow.add_edge(NodeNames.GENERAL, END)
        workflow.add_edge(NodeNames.AGGREGATOR, END)
        
        return workflow.compile()
    
    async def _supervisor_node(self, state: OrchestratorState) -> dict:
        """
        Supervisor node: Analyzes customer query and determines intent.
        """
        if not self.supervisor_llm:
            self.supervisor_llm = get_llm()
        
        user_message = state["messages"][-1].content if state["messages"] else ""
        logger.info(f"Supervisor analyzing: {user_message[:100]}...")
        
        prompt = PromptTemplate(
            template="""You are an AI supervisor for a customer support system. Analyze the customer's query and determine the primary intent.

Customer Query: {user_message}

Intent Classifications:
- faq: General questions, how-to guides, troubleshooting steps (no customer-specific context needed)
- customer_lookup: Queries referencing order numbers, account status, or customer history
- ticket: Need to create a support ticket, report an issue for tracking
- escalation: Critical/urgent issues, repeated problems, VIP customers, complex technical issues
- general: Greetings, unclear queries, or out-of-scope requests

Respond with ONLY ONE WORD - the intent classification.

Intent:""",
            input_variables=["user_message"]
        )
        
        chain = prompt | self.supervisor_llm
        response = await chain.ainvoke({"user_message": user_message})
        intent = response.content.strip().lower()
        
        # Validate and default to general if invalid
        valid_intents = [IntentType.FAQ, IntentType.CUSTOMER_LOOKUP, IntentType.TICKET, IntentType.ESCALATION, IntentType.GENERAL]
        if intent not in valid_intents:
            logger.warning(f"Invalid intent '{intent}', defaulting to 'general'")
            intent = IntentType.GENERAL
        
        logger.info(f"Supervisor determined intent: {intent}")
        return {"intent": intent}
    
    def _route_based_on_intent(self, state: OrchestratorState) -> str:
        """Route to appropriate node based on intent."""
        intent = state.get("intent", IntentType.GENERAL)
        logger.info(f"Routing to: {intent}")
        return intent
    
    async def _knowledge_node(self, state: OrchestratorState) -> dict:
        """Knowledge node: Query knowledge agent for FAQ answer."""
        logger.info("Knowledge node executing")
        user_message = state["messages"][-1].content
        
        try:
            response = await query_knowledge_agent(user_message)
            logger.info(f"Knowledge agent responded: {response[:100]}...")
            return {"knowledge_response": response}
        except Exception as e:
            logger.error(f"Knowledge agent error: {e}")
            return {"knowledge_response": f"Knowledge agent temporarily unavailable: {e}"}
    
    async def _crm_node(self, state: OrchestratorState) -> dict:
        """CRM node: Query CRM agent for customer information."""
        logger.info("CRM node executing")
        user_message = state["messages"][-1].content
        
        try:
            response = await query_crm_agent(user_message)
            logger.info(f"CRM agent responded: {response[:100]}...")
            return {"crm_response": response}
        except Exception as e:
            logger.error(f"CRM agent error: {e}")
            return {"crm_response": f"CRM system temporarily unavailable: {e}"}
    
    async def _ticket_node(self, state: OrchestratorState) -> dict:
        """Ticket node: Query ticket agent to create/lookup ticket."""
        logger.info("Ticket node executing")
        user_message = state["messages"][-1].content
        
        try:
            response = await query_ticket_agent(user_message)
            logger.info(f"Ticket agent responded: {response[:100]}...")
            return {"ticket_response": response}
        except Exception as e:
            logger.error(f"Ticket agent error: {e}")
            return {"ticket_response": f"Ticketing system temporarily unavailable: {e}"}
    
    async def _escalation_node(self, state: OrchestratorState) -> dict:
        """Escalation node: Query escalation agent for routing decision."""
        logger.info("Escalation node executing")
        user_message = state["messages"][-1].content
        
        try:
            response = await query_escalation_agent(user_message)
            logger.info(f"Escalation agent responded: {response[:100]}...")
            return {"escalation_response": response}
        except Exception as e:
            logger.error(f"Escalation agent error: {e}")
            return {"escalation_response": f"Escalation system temporarily unavailable: {e}"}
    
    async def _aggregator_node(self, state: OrchestratorState) -> dict:
        """
        Aggregator node: Combines responses from specialist agents into final answer.
        """
        if not self.aggregator_llm:
            self.aggregator_llm = get_llm()
        
        logger.info("Aggregator node executing")
        
        # Collect all responses
        responses = []
        if state.get("knowledge_response"):
            responses.append(f"Knowledge Base: {state['knowledge_response']}")
        if state.get("crm_response"):
            responses.append(f"Customer Information: {state['crm_response']}")
        if state.get("ticket_response"):
            responses.append(f"Ticket System: {state['ticket_response']}")
        if state.get("escalation_response"):
            responses.append(f"Escalation Assessment: {state['escalation_response']}")
        
        combined_responses = "\n\n".join(responses)
        user_query = state["messages"][-1].content
        
        prompt = PromptTemplate(
            template="""You are a customer support agent synthesizing information from multiple specialist systems.

Customer Query: {user_query}

Specialist Responses:
{combined_responses}

Create a unified, helpful response that:
1. Directly addresses the customer's question
2. Integrates relevant information from all specialists
3. Is clear, concise, and professional
4. Includes any ticket numbers, escalation info, or next steps

Final Response to Customer:""",
            input_variables=["user_query", "combined_responses"]
        )
        
        chain = prompt | self.aggregator_llm
        response = await chain.ainvoke({
            "user_query": user_query,
            "combined_responses": combined_responses
        })
        
        final_response = response.content.strip()
        logger.info(f"Aggregator created final response: {final_response[:100]}...")
        
        return {
            "messages": [AIMessage(content=final_response)],
            "final_response": final_response
        }
    
    async def _general_node(self, state: OrchestratorState) -> dict:
        """General node: Handle general queries without specialist agents."""
        logger.info("General node executing")
        
        response = "Hello! I'm AgentSwarm, your AI support assistant. I can help you with:\n" \
                   "- Technical support and troubleshooting\n" \
                   "- Account and order information\n" \
                   "- Creating support tickets\n" \
                   "- Routing urgent issues\n\n" \
                   "How can I assist you today?"
        
        return {
            "messages": [AIMessage(content=response)],
            "final_response": response
        }
    
    async def serve(self, prompt: str) -> str:
        """
        Main entry point: Process customer query through orchestrator.
        
        Args:
            prompt: Customer's query
            
        Returns:
            str: Final response
        """
        from langchain_core.messages import HumanMessage
        
        logger.info(f"Orchestrator serving prompt: {prompt[:100]}...")
        
        initial_state = {
            "messages": [HumanMessage(content=prompt)]
        }
        
        result = await self.graph.ainvoke(initial_state)
        final_response = result.get("final_response", "I apologize, but I encountered an issue processing your request.")
        
        logger.info("Orchestrator completed")
        return final_response


