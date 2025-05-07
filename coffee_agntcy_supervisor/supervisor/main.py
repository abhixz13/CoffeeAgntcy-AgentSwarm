# Copyright 2025 Cisco Systems, Inc. and its affiliates
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# SPDX-License-Identifier: Apache-2.0

import argparse
import asyncio
import os

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from supervisor.api.routes import stateless_runs
from supervisor.graph.graph import SupervisorGraph
from uvicorn import Config, Server


def create_app() -> FastAPI:
    """
    Creates and configures a FastAPI application instance.

    Returns:
        FastAPI: An instance of the FastAPI application with configured routes,
        middleware, and metadata.

    The application includes:
    - A title, version, and description for the API.
    - OpenAPI documentation available at `/api/v1/openapi.json`.
    - A router for stateless runs with the prefix `/api/v1`.
    - CORS middleware allowing all origins, credentials, methods, headers, and exposing headers.
    """
    app = FastAPI(
        title="Acorda Agent Supervisor",
        openapi_url="/api/v1/openapi.json",
        version="0.1.0",
        description="Acorda Agent Supervisor API",
    )
    app.include_router(stateless_runs.router, prefix="/api/v1")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["*"],
    )
    return app


def run_server():
    """
    Starts the server for the application.

    This function initializes and runs an ASGI server using the specified
    configuration. The server's host and port are determined by the environment
    variables `ACORDA_AGENT_HOST` and `ACORDA_AGENT_PORT`, with default values
    of "0.0.0.0" and 8125, respectively. If an event loop is already running,
    the server is started as a background task; otherwise, it is run in the
    current thread.

    Environment Variables:
        ACORDA_AGENT_PORT (str): The port number on which the server will run.
                                 Defaults to "8125".
        ACORDA_AGENT_HOST (str): The host address on which the server will run.
                                 Defaults to "0.0.0.0".

    Raises:
        Any exceptions raised during server initialization or execution.

    Note:
        This function uses `asyncio.run` if no event loop is running, which
        should not be called if the function is invoked within an existing
        asynchronous context.
    """
    port = int(os.getenv("ACORDA_AGENT_PORT", "8125"))
    host = os.getenv("ACORDA_AGENT_HOST", "0.0.0.0")
    config = Config(
        app=create_app(),
        host=host,
        port=port,
        log_level="info",
    )
    server = Server(config)
    try:
        if asyncio.get_event_loop().is_running():
            asyncio.ensure_future(server.serve())
        else:
            asyncio.run(server.serve())
    except (OSError, RuntimeError) as e:
        print(f"An error occurred while running the server: {e}")


def run_graph():
    """
    Executes the SupervisorGraph by initializing it, providing a sample user input,
    and printing the result.

    This function creates an instance of the SupervisorGraph class, simulates a user
    input prompt, and calls the `serve` method of the SupervisorGraph to process the
    input. The result of the operation is then printed to the console.

    Returns:
        None
    """
    supervisor_graph = SupervisorGraph()
    user_prompt = "Sample user input for SupervisorGraph"
    result, _ = supervisor_graph.serve(user_prompt)
    print("SupervisorGraph result:", result)


def main():
    """
    Main entry point for the Acorda Agent Supervisor application.
    This function parses command-line arguments to determine the mode of operation.
    It supports two modes:
    1. Running a FastAPI server (`--server` flag).
    2. Invoking the SupervisorGraph directly (default behavior if `--server` is not provided).
    Command-line Arguments:
        --server (optional): If provided, the FastAPI server will be started. 
                             Otherwise, the SupervisorGraph will be executed.
    Returns:
        None
    """
    parser = argparse.ArgumentParser(description="Run Acorda Agent Supervisor")
    parser.add_argument(
        "--server",
        action="store_true",
        help="Run the FastAPI server. If not provided, the SupervisorGraph will be invoked directly.",
    )
    args = parser.parse_args()

    if args.server:
        run_server()
    else:
        run_graph()


if __name__ == "__main__":
    main()
