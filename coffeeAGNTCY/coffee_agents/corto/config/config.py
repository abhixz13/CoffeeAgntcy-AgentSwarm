import os
from dotenv import load_dotenv

load_dotenv()  # Automatically loads from `.env` or `.env.local`

# --- Corto ---
DEFAULT_MESSAGE_TRANSPORT = os.getenv("DEFAULT_MESSAGE_TRANSPORT", "AGP")
TRANSPORT_SERVER_ENDPOINT = os.getenv("TRANSPORT_SERVER_ENDPOINT", "http://localhost:46357")
FARM_AGENT_HOST = os.getenv("FARM_AGENT_HOST", "localhost")
FARM_AGENT_PORT = int(os.getenv("FARM_AGENT_PORT", "9999"))
LLM_PROVIDER = os.getenv("LLM_PROVIDER")
LOGGING_LEVEL = os.getenv("LOGGING_LEVEL", "INFO").upper()
