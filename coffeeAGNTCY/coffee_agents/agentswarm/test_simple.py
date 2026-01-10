# Simple test - just verify LLM connection
import asyncio
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from dotenv import load_dotenv
load_dotenv()

async def main():
    print("=" * 60)
    print(" AgentSwarm - Simple LLM Test")
    print("=" * 60)
    
    from common.llm import get_llm
    
    llm = get_llm()
    print(f"\nLLM Model: {os.getenv('LLM_MODEL', 'default')}")
    
    print("\nTesting LLM...")
    response = await llm.ainvoke("Say 'AgentSwarm is ready!' in exactly 4 words.")
    print(f"Response: {response.content}")
    
    print("\n" + "=" * 60)
    print(" [SUCCESS] LLM is working! You can proceed.")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(main())

