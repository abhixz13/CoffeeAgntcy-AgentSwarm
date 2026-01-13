# Copyright AGNTCY Contributors (https://github.com/agntcy)
# SPDX-License-Identifier: Apache-2.0
# AgentSwarm - Cisco CIRCUIT API Integration
#
# Adapted from: C:\code\windsurf\webex-cdets-bot-python\services\circuit_ai_service.py
#
# CIRCUIT API - Cisco's internal LLM service
# - FREE for hackathons (no rate limits like OpenAI free tier)
# - VPN Required
# - OAuth2 via Okta (client_id + client_secret)
#
# Free Tier Models:
#   - gpt-4o-mini: 30 req/min, 500M tokens/month (recommended)
#   - gpt-4.1: 15 req/min, 50M tokens/month

import os
import json
import time
import base64
import logging
from typing import Any, List, Optional

import requests
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, SystemMessage
from langchain_core.outputs import ChatResult, ChatGeneration

logger = logging.getLogger("agentswarm.circuit_llm")


class CircuitChatModel(BaseChatModel):
    """
    LangChain-compatible wrapper for Cisco CIRCUIT API.
    Drop-in replacement for ChatOpenAI/ChatLiteLLM.
    """
    
    # Circuit API endpoints
    TOKEN_URL: str = "https://id.cisco.com/oauth2/default/v1/token"
    CHAT_URL: str = "https://chat-ai.cisco.com/openai/deployments/{model}/chat/completions"
    
    # Configuration
    client_id: str = ""
    client_secret: str = ""
    appkey: str = ""
    model: str = "gpt-4o-mini"
    temperature: float = 0.3
    max_tokens: int = 2000
    
    # Token management
    _access_token: Optional[str] = None
    _token_expires_at: float = 0
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.client_id = os.getenv('CIRCUIT_CLIENT_ID', '')
        self.client_secret = os.getenv('CIRCUIT_CLIENT_SECRET', '')
        self.appkey = os.getenv('CIRCUIT_APPKEY', '')
        self.model = os.getenv('CIRCUIT_MODEL', 'gpt-4o-mini')
        
        if self.is_available():
            logger.info(f"[Circuit] Initialized with model: {self.model}")
        else:
            logger.warning("[Circuit] Missing credentials - check CIRCUIT_CLIENT_ID, CIRCUIT_CLIENT_SECRET, CIRCUIT_APPKEY")
    
    @property
    def _llm_type(self) -> str:
        return "circuit"
    
    def is_available(self) -> bool:
        """Check if Circuit API is configured."""
        return bool(self.client_id and self.client_secret and self.appkey)
    
    def _get_access_token(self) -> Optional[str]:
        """
        Get OAuth2 access token from Cisco Okta.
        Token is valid for 1 hour, cached and refreshed automatically.
        """
        # #region agent log
        with open(r'c:\code\coffeeAgentify\.cursor\debug.log', 'a') as f: f.write(json.dumps({"hypothesisId":"H1","location":"circuit_llm.py:_get_access_token:entry","message":"Getting OAuth token","data":{"has_cached":bool(self._access_token),"client_id_len":len(self.client_id)},"timestamp":int(time.time()*1000),"sessionId":"debug-session"})+'\n')
        # #endregion
        # Return cached token if still valid (with 5 min buffer)
        if self._access_token and time.time() < (self._token_expires_at - 300):
            return self._access_token
        
        try:
            # Create Basic auth header
            credentials = f"{self.client_id}:{self.client_secret}"
            base64_credentials = base64.b64encode(credentials.encode()).decode()
            
            headers = {
                'Accept': '*/*',
                'Content-Type': 'application/x-www-form-urlencoded',
                'Authorization': f'Basic {base64_credentials}'
            }
            
            data = {'grant_type': 'client_credentials'}
            
            response = requests.post(
                self.TOKEN_URL,
                headers=headers,
                data=data,
                timeout=30
            )
            response.raise_for_status()
            
            token_data = response.json()
            self._access_token = token_data.get('access_token')
            
            # Token expires in 1 hour (3600 seconds)
            expires_in = token_data.get('expires_in', 3600)
            self._token_expires_at = time.time() + expires_in
            
            logger.info(f"[Circuit] Access token obtained, expires in {expires_in}s")
            # #region agent log
            with open(r'c:\code\coffeeAgentify\.cursor\debug.log', 'a') as f: f.write(json.dumps({"hypothesisId":"H1","location":"circuit_llm.py:_get_access_token:success","message":"Token obtained","data":{"expires_in":expires_in,"token_len":len(self._access_token) if self._access_token else 0},"timestamp":int(time.time()*1000),"sessionId":"debug-session"})+'\n')
            # #endregion
            return self._access_token
            
        except requests.exceptions.RequestException as e:
            logger.error(f"[Circuit] Failed to get access token: {e}")
            return None
        except Exception as e:
            logger.error(f"[Circuit] Unexpected error getting token: {e}")
            return None
    
    def _convert_messages(self, messages: List[BaseMessage]) -> List[dict]:
        """Convert LangChain messages to OpenAI format."""
        result = []
        for msg in messages:
            if isinstance(msg, SystemMessage):
                result.append({"role": "system", "content": msg.content})
            elif isinstance(msg, HumanMessage):
                result.append({"role": "user", "content": msg.content})
            elif isinstance(msg, AIMessage):
                result.append({"role": "assistant", "content": msg.content})
            else:
                # Default to user
                result.append({"role": "user", "content": str(msg.content)})
        return result
    
    def _call_circuit_api(self, messages: List[dict]) -> Optional[str]:
        """Call Circuit Chat Completions API."""
        # #region agent log
        with open(r'c:\code\coffeeAgentify\.cursor\debug.log', 'a') as f: f.write(json.dumps({"hypothesisId":"H2","location":"circuit_llm.py:_call_circuit_api:entry","message":"Calling Circuit API","data":{"num_messages":len(messages),"model":self.model},"timestamp":int(time.time()*1000),"sessionId":"debug-session"})+'\n')
        # #endregion
        token = self._get_access_token()
        if not token:
            logger.error("[Circuit] No access token available")
            return None
        
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json',
            'api-key': token,  # Some Azure OpenAI endpoints expect this
        }
        
        # OpenAI-compatible payload with required 'user' field containing appkey
        payload = {
            'messages': messages,
            'temperature': self.temperature,
            'max_tokens': self.max_tokens,
            'user': json.dumps({'appkey': self.appkey}),  # Required by Circuit API
        }
        
        # Build endpoint URL with model name
        url = self.CHAT_URL.format(model=self.model)
        
        try:
            response = requests.post(
                url,
                headers=headers,
                json=payload,
                timeout=60
            )
            response.raise_for_status()
            
            data = response.json()
            
            # OpenAI-compatible response format
            if 'choices' in data and len(data['choices']) > 0:
                content = data['choices'][0]['message']['content']
                # #region agent log
                with open(r'c:\code\coffeeAgentify\.cursor\debug.log', 'a') as f: f.write(json.dumps({"hypothesisId":"H2","location":"circuit_llm.py:_call_circuit_api:success","message":"API response received","data":{"content_len":len(content),"content_preview":content[:100] if content else None},"timestamp":int(time.time()*1000),"sessionId":"debug-session"})+'\n')
                # #endregion
                return content
            
            logger.warning(f"[Circuit] Unexpected response format: {data}")
            return None
            
        except requests.exceptions.HTTPError as e:
            logger.error(f"[Circuit] HTTP Error: {e}")
            if e.response is not None:
                logger.error(f"[Circuit] Response: {e.response.text[:500]}")
            return None
        except requests.exceptions.RequestException as e:
            logger.error(f"[Circuit] Request Error: {e}")
            return None
        except Exception as e:
            logger.error(f"[Circuit] Unexpected error: {e}")
            return None
    
    def _generate(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        run_manager: Optional[Any] = None,
        **kwargs
    ) -> ChatResult:
        """Generate a response from the Circuit API."""
        openai_messages = self._convert_messages(messages)
        
        content = self._call_circuit_api(openai_messages)
        
        if content is None:
            content = "[CIRCUIT ERROR] Failed to get response. Check VPN connection and credentials."
        
        message = AIMessage(content=content)
        generation = ChatGeneration(message=message)
        
        return ChatResult(generations=[generation])
    
    async def _agenerate(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        run_manager: Optional[Any] = None,
        **kwargs
    ) -> ChatResult:
        """Async version - uses sync call (Circuit API is sync)."""
        # Circuit API is synchronous, so we just call the sync version
        # For true async, would need httpx.AsyncClient
        return self._generate(messages, stop, run_manager, **kwargs)


def get_circuit_llm() -> CircuitChatModel:
    """Get a configured Circuit LLM instance."""
    return CircuitChatModel()


# Check if Circuit is available
def is_circuit_available() -> bool:
    """Check if CIRCUIT API credentials are configured."""
    return bool(
        os.getenv('CIRCUIT_CLIENT_ID') and 
        os.getenv('CIRCUIT_CLIENT_SECRET') and 
        os.getenv('CIRCUIT_APPKEY')
    )
