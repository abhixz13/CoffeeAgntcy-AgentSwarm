# Copyright AGNTCY Contributors (https://github.com/agntcy)
# SPDX-License-Identifier: Apache-2.0
# Adapted for AgentSwarm

from config.config import LLM_MODEL
from langchain_litellm import ChatLiteLLM

def get_llm():
    """
    Get the LLM provider based on the configuration using ChatLiteLLM.
    Supports multiple providers via LiteLLM (GROQ, OpenAI, Azure, etc.)
    
    Returns:
        ChatLiteLLM: Configured LLM instance
    """
    llm = ChatLiteLLM(model=LLM_MODEL)
    return llm


