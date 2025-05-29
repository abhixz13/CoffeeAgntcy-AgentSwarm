import logging
from uuid import uuid4

from httpx import AsyncClient, Timeout

from a2a.client import A2AClient
from a2a.types import SendMessageRequest, MessageSendParams, Message, Part, TextPart, Role
from config.config import FARM_AGENT_HOST, FARM_AGENT_PORT

logger = logging.getLogger("corto.supervisor.a2a_client")
AGENT_URL = f"http://{FARM_AGENT_HOST}:{FARM_AGENT_PORT}"

async def send_message(prompt: str):
  """
  Sends a message to the flavor profile farm agent via A2A, specifically invoking its `estimate_flavor` skill. 
  Args:
      prompt (str): The user input prompt to send to the agent.
  Returns:
      str: The flavor profile estimation returned by the agent.
  """
  logger.info(f"Sending request to A2A agent at: {AGENT_URL} with payload: {prompt}")
  client = await A2AClient.get_client_from_agent_card_url(
    AsyncClient(timeout=Timeout(15.0)), AGENT_URL
  )

  request = SendMessageRequest(
      params=MessageSendParams(
          skill_id="estimate_flavor",
          sender_id="coffee-exchange-agent",
          receiver_id="flavor-profile-farm-agent",
          message=Message(
            messageId=str(uuid4()),
            role=Role.user,
            parts=[Part(TextPart(text=prompt))],
        )
      )
  )

  response = await client.send_message(request.params)
  logger.info(f"Response received from A2A agent: {response}")
  if response.root.result:
    if not response.root.result.parts:
      raise ValueError("No response parts found in the message.")
    part = response.root.result.parts[0].root
    if hasattr(part, "text"):
      return part.text
  elif response.root.error:
    raise Exception(f"A2A error: {response.error.message}")
  raise Exception("Unknown response type")
