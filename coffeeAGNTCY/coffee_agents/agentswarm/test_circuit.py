# Test CIRCUIT API Connection
# Run: python test_circuit.py

import asyncio
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from dotenv import load_dotenv
load_dotenv()

async def main():
    print("=" * 60)
    print(" AgentSwarm - CIRCUIT API Test")
    print("=" * 60)
    
    # Check environment
    print("\n[1] Checking environment variables...")
    
    client_id = os.getenv('CIRCUIT_CLIENT_ID', '')
    client_secret = os.getenv('CIRCUIT_CLIENT_SECRET', '')
    appkey = os.getenv('CIRCUIT_APPKEY', '')
    model = os.getenv('CIRCUIT_MODEL', 'gpt-4o-mini')
    
    if client_id:
        print(f"    CIRCUIT_CLIENT_ID: {client_id[:10]}...")
    else:
        print("    [ERROR] CIRCUIT_CLIENT_ID not set!")
        
    if client_secret:
        print(f"    CIRCUIT_CLIENT_SECRET: {client_secret[:5]}...")
    else:
        print("    [ERROR] CIRCUIT_CLIENT_SECRET not set!")
        
    if appkey:
        print(f"    CIRCUIT_APPKEY: {appkey[:10]}...")
    else:
        print("    [ERROR] CIRCUIT_APPKEY not set!")
    
    print(f"    CIRCUIT_MODEL: {model}")
    
    if not all([client_id, client_secret, appkey]):
        print("\n[ERROR] Missing CIRCUIT credentials!")
        print("Get them from the CIRCUIT API Portal (VPN required)")
        return
    
    # Test LLM
    print("\n[2] Testing CIRCUIT API connection...")
    
    from common.circuit_llm import CircuitChatModel
    
    llm = CircuitChatModel()
    
    if not llm.is_available():
        print("    [ERROR] CIRCUIT not available!")
        return
    
    print("    [OK] CIRCUIT credentials loaded")
    
    print("\n[3] Getting OAuth token...")
    token = llm._get_access_token()
    
    if token:
        print(f"    [OK] Token obtained: {token[:20]}...")
    else:
        print("    [ERROR] Failed to get token!")
        print("    Make sure you are on Cisco VPN")
        return
    
    print("\n[4] Testing chat completion...")
    
    response = await llm.ainvoke("Say 'AgentSwarm is ready!' in exactly 4 words.")
    print(f"    Response: {response.content}")
    
    print("\n" + "=" * 60)
    print(" [SUCCESS] CIRCUIT API is working!")
    print("=" * 60)
    print("\nTo use CIRCUIT in AgentSwarm, set in .env:")
    print("    AI_BACKEND=circuit")


if __name__ == "__main__":
    asyncio.run(main())
