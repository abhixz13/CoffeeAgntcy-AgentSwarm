import logging

from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.events import EventQueue
from a2a.utils.errors import ServerError
from a2a.types import (
    UnsupportedOperationError,
    InternalError,
    InvalidParamsError,
    Task)

from a2a.utils import (
    new_agent_text_message,
    new_task,
)

from agent import FarmAgent
from agent_executor import FarmAgent

logger = logging.getLogger("corto.farm_agent.a2a_executor")

class FarmAgentExecutor(AgentExecutor):
    def __init__(self):
        self.agent = FarmAgent()

    def _validate_request(self, context: RequestContext) -> bool:
        return False
    
    async def execute(
        self,
        context: RequestContext,
        event_queue: EventQueue,
    ) -> None:
        error = self._validate_request(context)
        if error:
            raise ServerError(error=InvalidParamsError())
        
        prompt = context.get_user_input()
        task = context.current_task
        if not task:
            task = new_task(context.message)
            event_queue.enqueue_event(task)

        try:
            output = await self.agent.ainvoke(prompt)
            if output.get("error_message") is not None and output.get("error_message") != "":
                logger.error("Error in agent response: %s", output.get("error_message"))
                message = new_agent_text_message(
                    output.get("error_message", "Failed to generate flavor profile"),
                )
                event_queue.enqueue_event(message)
                return

            flavor = output.get("flavor_notes", "No flavor profile returned")
            logger.info("Flavor profile generated: %s", flavor)
            event_queue.enqueue_event(new_agent_text_message(flavor))
        except Exception as e:
            logger.error(f'An error occurred while streaming the flavor profile response: {e}')
            raise ServerError(error=InternalError()) from e
        
    async def cancel(
        self, request: RequestContext, event_queue: EventQueue
    ) -> Task | None:
        raise ServerError(error=UnsupportedOperationError())