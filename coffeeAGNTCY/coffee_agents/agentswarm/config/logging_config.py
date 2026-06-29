# Copyright AGNTCY Contributors (https://github.com/agntcy)
# SPDX-License-Identifier: Apache-2.0
# Adapted for AgentSwarm

import logging
from config.config import LOGGING_LEVEL

def setup_logging():
    """
    Configure logging for AgentSwarm application.
    Sets up format, level, and silences noisy libraries.
    """
    logging.basicConfig(
        level=LOGGING_LEVEL,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        force=True,
    )

    # Set specific logging levels for noisy libraries
    logging.getLogger("openai").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("webexteamssdk").setLevel(logging.INFO)


