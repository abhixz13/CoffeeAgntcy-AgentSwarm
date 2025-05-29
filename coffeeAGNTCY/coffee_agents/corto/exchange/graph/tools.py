import logging

from langchain_core.tools import tool

from clients.a2a.client import send_message
from graph.models import FlavorProfileInput, FlavorProfileOutput

@tool
async def get_flavor_profile_via_a2a(input: FlavorProfileInput) -> FlavorProfileOutput:
    """
    This tool sends a prompt to the A2A agent and returns the flavor profile estimation.

    Args:
        input (FlavorProfileInput): A JSON representation containing the prompt request for flavor profile estimation.
    Returns:
        FlavorProfileOutput: A JSON representation of the flavor profile estimation.
    """
    try:
        if not input.prompt.strip():
            raise ValueError("Invalid input: Prompt must be a non-empty string.")
        resp = await send_message(input.prompt)
        return FlavorProfileOutput(flavor_profile=resp)
    except Exception as e:
        raise RuntimeError(f"Failed to get flavor profile: {str(e)}")
