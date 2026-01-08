# Copyright AGNTCY Contributors (https://github.com/agntcy)
# SPDX-License-Identifier: Apache-2.0
# AgentSwarm - Knowledge Agent A2A Server

import asyncio
import logging

from a2a.server.apps import A2AStarletteApplication
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore
from dotenv import load_dotenv
from uvicorn import Config, Server

from agntcy_app_sdk.semantic.a2a.protocol import A2AProtocol
from agntcy_app_sdk.app_sessions import AppContainer

from config.config import (
    DEFAULT_MESSAGE_TRANSPORT,
    TRANSPORT_SERVER_ENDPOINT,
    KNOWLEDGE_AGENT_PORT,
    ENABLE_HTTP,
)
from config.logging_config import setup_logging
from agents.knowledge.agent import factory
from agents.knowledge.agent_executor import KnowledgeAgentExecutor
from agents.knowledge.card import AGENT_CARD

# Setup logging
setup_logging()
logger = logging.getLogger("agentswarm.knowledge_agent.server")

load_dotenv()

async def run_http_server(server, port):
    """Run the HTTP/REST server."""
    try:
        logger.info(f"Starting Knowledge Agent HTTP server on port {port}")
        config = Config(app=server.build(), host="0.0.0.0", port=port, loop="asyncio")
        userver = Server(config)
        await userver.serve()
    except Exception as e:
        logger.error(f"HTTP server encountered an error: {e}", exc_info=True)

async def run_transport(server, transport_type, endpoint):
    """Run the transport bridge."""
    try:
        personal_topic = A2AProtocol.create_agent_topic(AGENT_CARD)
        logger.info(f"Knowledge Agent topic: {personal_topic}")
        
        transport = factory.create_transport(
            transport_type, 
            endpoint=endpoint, 
            name=f"default/default/{personal_topic}"
        )

        # Create application session
        app_session = factory.create_app_session(max_sessions=1)
        
        # Add container for personal topic
        app_session.add_app_container(
            "knowledge_session", 
            AppContainer(
                server,
                transport=transport,
                topic=personal_topic,
            )
        )

        logger.info("Starting Knowledge Agent transport session")
        await app_session.start_session("knowledge_session")
        
        # Keep running
        while True:
            await asyncio.sleep(1)

    except Exception as e:
        logger.error(f"Transport encountered an error: {e}", exc_info=True)
        await app_session.stop_all_sessions()

async def main(enable_http: bool):
    """Run the A2A server with both HTTP and transport logic."""
    logger.info("Initializing Knowledge Agent server")
    
    request_handler = DefaultRequestHandler(
        agent_executor=KnowledgeAgentExecutor(),
        task_store=InMemoryTaskStore(),
    )

    server = A2AStarletteApplication(
        agent_card=AGENT_CARD, 
        http_handler=request_handler
    )

    logger.info(f"Knowledge Agent Configuration:")
    logger.info(f"  - Transport: {DEFAULT_MESSAGE_TRANSPORT}")
    logger.info(f"  - Endpoint: {TRANSPORT_SERVER_ENDPOINT}")
    logger.info(f"  - HTTP Port: {KNOWLEDGE_AGENT_PORT}")
    logger.info(f"  - HTTP Enabled: {enable_http}")

    # Run HTTP server and transport logic concurrently
    async with asyncio.TaskGroup() as tg:
        if enable_http:
            tg.create_task(run_http_server(server, KNOWLEDGE_AGENT_PORT))
        tg.create_task(run_transport(server, DEFAULT_MESSAGE_TRANSPORT, TRANSPORT_SERVER_ENDPOINT))

if __name__ == '__main__':
    try:
        logger.info("=" * 60)
        logger.info("AgentSwarm - Knowledge Agent Starting")
        logger.info("=" * 60)
        asyncio.run(main(ENABLE_HTTP))
    except KeyboardInterrupt:
        logger.info("\nShutting down gracefully on keyboard interrupt.")
    except Exception as e:
        logger.error(f"Error occurred: {e}", exc_info=True)


