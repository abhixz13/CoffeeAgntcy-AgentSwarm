# Copyright AGNTCY Contributors (https://github.com/agntcy)
# SPDX-License-Identifier: Apache-2.0
# AgentSwarm - Orchestrator with Multi-Agent Collaboration (Enhanced Demo)

import logging
import json
import time
import asyncio
from datetime import datetime
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import PromptTemplate
from langgraph.graph import StateGraph, END

from agents.orchestrator.models import OrchestratorState, NodeNames, IntentType
from agents.orchestrator.http_client import get_http_client
from common.llm import get_llm

logger = logging.getLogger("agentswarm.orchestrator.graph")


class OrchestratorGraph:
    """
    Orchestrator Agent - Supervisor that coordinates MULTIPLE specialist agents.
    Enhanced demo version with timestamps, visual flow, and agent communication.
    """
    
    def __init__(self):
        """Initialize the orchestrator with LangGraph workflow."""
        self.supervisor_llm = None
        self.aggregator_llm = None
        self.http_client = get_http_client()
        self.graph = self._build_graph()
        logger.info("Orchestrator Graph initialized (Enhanced Multi-Agent Demo)")
    
    def _build_graph(self):
        """Build the LangGraph workflow for multi-agent orchestration."""
        workflow = StateGraph(OrchestratorState)
        
        # Add nodes
        workflow.add_node(NodeNames.SUPERVISOR, self._supervisor_node)
        workflow.add_node("multi_agent_executor", self._multi_agent_executor)
        workflow.add_node(NodeNames.AGGREGATOR, self._aggregator_node)
        workflow.add_node(NodeNames.GENERAL, self._general_node)
        
        # Set entry point
        workflow.set_entry_point(NodeNames.SUPERVISOR)
        
        # Route from supervisor
        workflow.add_conditional_edges(
            NodeNames.SUPERVISOR,
            self._route_based_on_intent,
            {
                "multi_agent": "multi_agent_executor",
                "general": NodeNames.GENERAL,
            }
        )
        
        # Multi-agent executor goes to aggregator
        workflow.add_edge("multi_agent_executor", NodeNames.AGGREGATOR)
        workflow.add_edge(NodeNames.GENERAL, END)
        workflow.add_edge(NodeNames.AGGREGATOR, END)
        
        return workflow.compile()
    
    async def _supervisor_node(self, state: OrchestratorState) -> dict:
        """Supervisor node: Analyzes query and plans multi-agent collaboration."""
        if not self.supervisor_llm:
            self.supervisor_llm = get_llm()
        
        user_message = state["messages"][-1].content if state["messages"] else ""
        logger.info(f"Supervisor analyzing: {user_message[:100]}...")
        
        prompt = PromptTemplate(
            template="""You are an AI supervisor for a customer support system. Analyze the customer's query and determine which specialist agents should collaborate.

Customer Query: {user_message}

Available Agents:
- KNOWLEDGE: Technical docs, FAQs, troubleshooting steps
- CRM: Customer info, account status, order history, subscription tier
- TICKET: Create/track support tickets, assign priority
- ESCALATION: Urgent issues, VIP routing, critical assessments

Rules for Agent Selection:
1. If query mentions customer ID/order number → ALWAYS include CRM
2. If query needs troubleshooting/how-to → ALWAYS include KNOWLEDGE  
3. If query mentions creating ticket/tracking issue → ALWAYS include TICKET
4. If query mentions URGENT/CRITICAL/VIP/premium → ALWAYS include ESCALATION
5. For complex queries → Use 3-4 agents for comprehensive response
6. For simple greetings → Return "general"

Respond with comma-separated agent names (e.g., "CRM,KNOWLEDGE,TICKET") or "general" for greetings.

Agents to consult:""",
            input_variables=["user_message"]
        )
        
        chain = prompt | self.supervisor_llm
        response = await chain.ainvoke({"user_message": user_message})
        agents_str = response.content.strip().upper()
        
        # Parse agents
        if agents_str == "GENERAL" or not agents_str:
            intent = "general"
            agents_to_call = []
        else:
            intent = "multi_agent"
            agents_to_call = [a.strip() for a in agents_str.split(",") if a.strip()]
        
        # #region agent log
        with open(r'c:\code\coffeeAgentify\.cursor\debug.log', 'a') as f: f.write(json.dumps({"hypothesisId":"H3","location":"graph.py:_supervisor_node","message":"Supervisor planned agents","data":{"raw_response":response.content,"agents_to_call":agents_to_call,"user_message":user_message[:50]},"timestamp":int(time.time()*1000),"sessionId":"debug-session"})+'\n')
        # #endregion
        
        logger.info(f"Supervisor selected agents: {agents_to_call}")
        return {"intent": intent, "agents_to_call": agents_to_call}
    
    def _route_based_on_intent(self, state: OrchestratorState) -> str:
        """Route to multi-agent executor or general."""
        intent = state.get("intent", "general")
        logger.info(f"Routing to: {intent}")
        return intent
    
    async def _multi_agent_executor(self, state: OrchestratorState) -> dict:
        """Execute multiple agents with timestamps and inter-agent communication."""
        user_message = state["messages"][-1].content
        agents_to_call = state.get("agents_to_call", [])
        
        logger.info(f"Multi-agent executor: Calling {agents_to_call}")
        
        # Build execution trace with timestamps
        execution_trace = []
        agent_communications = []  # Track agent-to-agent messages
        responses = {}
        step = 0
        start_time = time.time()
        
        # Call agents in sequence (to show the flow clearly in demo)
        for agent_name in agents_to_call:
            agent_name = agent_name.upper()
            step += 1
            agent_start = time.time()
            timestamp = datetime.now().strftime("%H:%M:%S")
            
            # #region agent log
            with open(r'c:\code\coffeeAgentify\.cursor\debug.log', 'a') as f: f.write(json.dumps({"hypothesisId":"H4","location":"graph.py:multi_agent_executor","message":f"Calling {agent_name}","data":{"agent":agent_name,"step":step},"timestamp":int(time.time()*1000),"sessionId":"debug-session"})+'\n')
            # #endregion
            
            if agent_name == "CRM":
                response = await self.http_client.query_crm(user_message)
                responses["crm_response"] = response
                duration = time.time() - agent_start
                execution_trace.append({
                    "step": step,
                    "time": timestamp,
                    "agent": "CRM",
                    "action": "Customer lookup",
                    "duration": duration
                })
                
                # Simulate agent insight for inter-agent communication
                if "premium" in response.lower() or "vip" in response.lower():
                    agent_communications.append("CRM -> TICKET: Premium customer - prioritize!")
                    agent_communications.append("CRM -> ESCALATION: VIP detected - priority routing")
                else:
                    agent_communications.append("CRM -> TICKET: Customer data retrieved")
                
            elif agent_name == "KNOWLEDGE":
                response = await self.http_client.query_knowledge(user_message)
                responses["knowledge_response"] = response
                duration = time.time() - agent_start
                execution_trace.append({
                    "step": step,
                    "time": timestamp,
                    "agent": "KNOWLEDGE",
                    "action": "Docs retrieved",
                    "duration": duration
                })
                
                agent_communications.append("KNOWLEDGE -> AGGREGATOR: Troubleshooting ready")
                
            elif agent_name == "TICKET":
                # Include context from CRM if available
                context = user_message
                if responses.get("crm_response"):
                    context += f"\n\nCustomer Context: {responses['crm_response'][:300]}"
                response = await self.http_client.query_ticket(context)
                responses["ticket_response"] = response
                duration = time.time() - agent_start
                execution_trace.append({
                    "step": step,
                    "time": timestamp,
                    "agent": "TICKET",
                    "action": "Ticket created",
                    "duration": duration
                })
                
                agent_communications.append("TICKET -> ESCALATION: TKT created, needs routing")
                
            elif agent_name == "ESCALATION":
                # Include all context for escalation assessment
                context = user_message
                if responses.get("crm_response"):
                    context += f"\n\nCustomer Info: {responses['crm_response'][:300]}"
                if responses.get("ticket_response"):
                    context += f"\n\nTicket Info: {responses['ticket_response'][:300]}"
                response = await self.http_client.query_escalation(context)
                responses["escalation_response"] = response
                duration = time.time() - agent_start
                execution_trace.append({
                    "step": step,
                    "time": timestamp,
                    "agent": "ESCALATION",
                    "action": "Engineer assigned",
                    "duration": duration
                })
                
                agent_communications.append("ESCALATION -> AGGREGATOR: Critical - engineer assigned")
        
        total_time = time.time() - start_time
        
        # Store execution data for display
        responses["execution_trace"] = execution_trace
        responses["agent_communications"] = agent_communications
        responses["agents_called"] = agents_to_call
        responses["total_time"] = total_time
        
        return responses
    
    async def _aggregator_node(self, state: OrchestratorState) -> dict:
        """Aggregator node: Combines responses with visual demo elements."""
        if not self.aggregator_llm:
            self.aggregator_llm = get_llm()
        
        logger.info("Aggregator node executing")
        
        # Get execution data
        execution_trace = state.get("execution_trace", [])
        agent_communications = state.get("agent_communications", [])
        agents_called = state.get("agents_called", [])
        total_time = state.get("total_time", 0)
        
        # Collect all responses
        specialist_responses = []
        if state.get("crm_response"):
            specialist_responses.append(f"CRM AGENT:\n{state['crm_response']}")
        if state.get("knowledge_response"):
            specialist_responses.append(f"KNOWLEDGE AGENT:\n{state['knowledge_response']}")
        if state.get("ticket_response"):
            specialist_responses.append(f"TICKET AGENT:\n{state['ticket_response']}")
        if state.get("escalation_response"):
            specialist_responses.append(f"ESCALATION AGENT:\n{state['escalation_response']}")
        
        combined_responses = "\n\n---\n\n".join(specialist_responses)
        user_query = state["messages"][-1].content
        
        prompt = PromptTemplate(
            template="""You are an AI coordinator synthesizing information from multiple specialist agents.

Customer Query: {user_query}

Specialist Agent Responses:
{combined_responses}

Create a unified response that:
1. Integrates insights from ALL agents consulted
2. Presents information in a logical flow
3. Highlights key findings from each specialist
4. Provides clear next steps based on combined analysis
5. Keep it concise but comprehensive

Unified Response:""",
            input_variables=["user_query", "combined_responses"]
        )
        
        chain = prompt | self.aggregator_llm
        response = await chain.ainvoke({
            "user_query": user_query,
            "combined_responses": combined_responses
        })
        
        llm_response = response.content.strip()
        logger.info(f"Aggregator response: {llm_response[:100]}...")
        
        # ============================================
        # BUILD ENHANCED DEMO HEADER (FIXED FORMATTING)
        # ============================================
        
        header = "\n"
        header += "=" * 55 + "\n"
        header += "    AGENTSWARM MULTI-AGENT COLLABORATION\n"
        header += "        Powered by Cisco CIRCUIT AI\n"
        header += "=" * 55 + "\n\n"
        
        # OPTION 2: Visual Architecture Diagram (Simplified for Webex)
        header += "ORCHESTRATION FLOW:\n"
        header += "-" * 55 + "\n"
        header += "           [USER QUERY]\n"
        header += "                |\n"
        header += "                v\n"
        header += "          [SUPERVISOR] --> Intent Analysis\n"
        header += "                |\n"
        header += "    +-----+-----+-----+-----+\n"
        header += "    |     |     |     |     |\n"
        header += "    v     v     v     v     |\n"
        header += "  [CRM] [KB] [TKT] [ESC]    |\n"
        header += "    |     |     |     |     |\n"
        header += "    +-----+-----+-----+     |\n"
        header += "                |           |\n"
        header += "                v           |\n"
        header += "          [AGGREGATOR] <----+\n"
        header += "                |\n"
        header += "                v\n"
        header += "        [UNIFIED RESPONSE]\n"
        header += "-" * 55 + "\n\n"
        
        # OPTION 1: Execution Timeline with Timestamps (FIXED)
        header += "EXECUTION TIMELINE:\n"
        header += "-" * 55 + "\n"
        for trace in execution_trace:
            line = f"[{trace['step']}] {trace['time']} | {trace['agent']:10} | {trace['action']:15} ({trace['duration']:.1f}s)"
            header += line + "\n"
        header += "-" * 55 + "\n"
        header += f"Total Agents: {len(agents_called)}  |  Total Time: {total_time:.1f}s\n"
        header += "-" * 55 + "\n\n"
        
        # OPTION 3: Agent-to-Agent Communication (FIXED)
        if agent_communications:
            header += "AGENT-TO-AGENT COMMUNICATION:\n"
            header += "-" * 55 + "\n"
            for comm in agent_communications:
                header += f">> {comm}\n"
            header += "-" * 55 + "\n\n"
        
        header += "=" * 55 + "\n"
        header += "      SYNTHESIZED RESPONSE FROM ALL AGENTS\n"
        header += "=" * 55 + "\n\n"
        
        final_response = header + llm_response
        
        return {
            "messages": AIMessage(content=final_response),
            "final_response": final_response
        }
    
    async def _general_node(self, state: OrchestratorState) -> dict:
        """General node: Handle greetings with demo info."""
        logger.info("General node executing")
        
        header = "\n"
        header += "=" * 55 + "\n"
        header += "      AGENTSWARM MULTI-AGENT SYSTEM\n"
        header += "      Webex Contact Center AI Demo\n"
        header += "=" * 55 + "\n\n"
        
        header += "AVAILABLE SPECIALIST AGENTS:\n"
        header += "-" * 55 + "\n"
        header += "[1] KNOWLEDGE  - Technical docs & FAQs\n"
        header += "[2] CRM        - Customer data & history\n"
        header += "[3] TICKET     - Support ticket management\n"
        header += "[4] ESCALATION - Urgent issue routing\n"
        header += "-" * 55 + "\n\n"
        
        greeting = "Hello! I'm AgentSwarm - a Multi-Agent AI System.\n\n"
        greeting += "Try these demo queries to see agents collaborate:\n\n"
        greeting += ">> 'I'm customer #12345 and can't reset my password'\n"
        greeting += "   (Triggers: CRM + Knowledge agents)\n\n"
        greeting += ">> 'Create a ticket for order #67890 - login issue'\n"
        greeting += "   (Triggers: CRM + Ticket + Knowledge agents)\n\n"
        greeting += ">> 'URGENT: Premium customer #12345, system down!'\n"
        greeting += "   (Triggers: ALL 4 agents in collaboration)\n"
        
        response = header + greeting
        
        return {
            "messages": AIMessage(content=response),
            "final_response": response
        }
    
    async def run(self, prompt: str) -> str:
        """Main entry point: Process customer query with multi-agent collaboration."""
        logger.info(f"Orchestrator processing: {prompt[:100]}...")
        # #region agent log
        with open(r'c:\code\coffeeAgentify\.cursor\debug.log', 'a') as f: f.write(json.dumps({"hypothesisId":"H5","location":"graph.py:run:start","message":"Orchestrator starting","data":{"prompt":prompt[:100]},"timestamp":int(time.time()*1000),"sessionId":"debug-session"})+'\n')
        # #endregion
        
        initial_state = {
            "messages": [HumanMessage(content=prompt)]
        }
        
        result = await self.graph.ainvoke(initial_state)
        final_response = result.get("final_response", "Sorry, I encountered an issue.")
        # #region agent log
        with open(r'c:\code\coffeeAgentify\.cursor\debug.log', 'a') as f: f.write(json.dumps({"hypothesisId":"H5","location":"graph.py:run:end","message":"Orchestrator finished","data":{"has_response":bool(final_response),"response_len":len(final_response) if final_response else 0},"timestamp":int(time.time()*1000),"sessionId":"debug-session"})+'\n')
        # #endregion
        return final_response
