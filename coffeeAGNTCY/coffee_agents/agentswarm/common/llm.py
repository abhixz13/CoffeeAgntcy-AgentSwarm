# Copyright AGNTCY Contributors (https://github.com/agntcy)
# SPDX-License-Identifier: Apache-2.0
# Adapted for AgentSwarm

import os
from config.config import LLM_MODEL, AI_BACKEND

def get_llm():
    """
    Get the LLM provider based on the configuration.
    
    Supports:
    - circuit: Cisco CIRCUIT API (FREE, internal, VPN required)
    - openai/groq/azure: Via LiteLLM
    
    Set AI_BACKEND in .env:
    - AI_BACKEND=circuit  -> Uses Cisco CIRCUIT API
    - AI_BACKEND=litellm  -> Uses LiteLLM (OpenAI, GROQ, Azure, etc.)
    
    Returns:
        BaseChatModel: Configured LLM instance
    """
    
    if AI_BACKEND == "circuit":
        # Use Cisco CIRCUIT API (FREE for hackathons!)
        from common.circuit_llm import CircuitChatModel, is_circuit_available
        
        if is_circuit_available():
            print("[LLM] Using Cisco CIRCUIT API")
            return CircuitChatModel()
        else:
            print("[LLM] CIRCUIT not configured, falling back to LiteLLM")
    
    # Default: Use LiteLLM (supports OpenAI, GROQ, Azure, etc.)
    from langchain_litellm import ChatLiteLLM
    print(f"[LLM] Using LiteLLM with model: {LLM_MODEL}")
    return ChatLiteLLM(model=LLM_MODEL)
