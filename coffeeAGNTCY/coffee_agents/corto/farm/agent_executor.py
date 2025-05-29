import logging
from uuid import uuid4

from a2a.server.agent_execution import BaseAgentExecutor
from a2a.server.events import EventQueue
from a2a.types import (Message, Part, Role,
                       SendMessageRequest, Task, TextPart)
from typing_extensions import override

from agent import FarmAgent  # Import message_node
from agent_executor import FarmAgent

logger = logging.getLogger("corto.farm_agent.a2a_executor")

class FarmAgentExecutor(BaseAgentExecutor):
    def __init__(self):
        self.agent = FarmAgent()

    @override
    async def on_message_send(
            self,
            request: SendMessageRequest,
            event_queue: EventQueue,
            task: Task | None,
    ) -> None:
        """
        Handle incoming message requests to generate a flavor profile for coffee beans.
        This method processes the request, invokes the FarmAgent to generate a flavor profile,
        and enqueues the response message to the event queue.

        Args:
            request (SendMessageRequest): The incoming message request containing the agent message.
            event_queue (EventQueue): The event queue to enqueue the response message.
            task (Task | None): Optional task context, not used in this implementation.
        """
        logger.info("Received message request: %s", request)

        params = request.params
        if not params or not params.message or not params.message.parts:
            logger.error("Invalid request parameters: %s", params)
            message = self._error_message("invalid_input", "Missing agent message")
            event_queue.enqueue_event(message)
            return
        prompt = params.message.parts[0].root.text
        try:
            output = await self.agent.ainvoke(prompt)
            if output.get("error_message") is not None and output.get("error_message") != "":
                logger.error("Error in agent response: %s", output.get("error_message"))
                message = self._error_message(
                    output.get("error_type", "internal_error"),
                    output.get("error_message", "Failed to generate flavor profile"),
                )
                event_queue.enqueue_event(message)
                return
            flavor = output.get("flavor_notes", "No flavor profile returned")
            logger.info("Flavor profile generated: %s", flavor)
            message = self._build_message(flavor)
        except Exception as e:
            logger.error("Error during flavor profile generation: %s", e)
            message = self._error_message("internal_error", "Failed to generate flavor profile")

        event_queue.enqueue_event(message)

    def _build_message(self, text: str) -> Message:
        """
        Build a message with the given text to be sent as a response.
        Args:
            text (str): The text content of the message.
        Returns:
            Message: A Message object containing the text as a part.
        """
        return Message(
            role=Role.agent,
            parts=[Part(TextPart(text=text))],
            messageId=str(uuid4()),
        )

    def _error_message(self, code: str, msg: str) -> Message:
        """
        Build an error message with the given code and message.
        Args:
            code (str): The error code.
            msg (str): The error message.
        Returns:
            Message: A Message object containing the error information.
        """
        return Message(
            role=Role.agent,
            parts=[Part(TextPart(text=f"{code}: {msg}"))],
            messageId=str(uuid4()),
        )
