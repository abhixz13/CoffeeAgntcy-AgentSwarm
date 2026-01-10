# Quick test script for AgentSwarm Orchestrator
# Tests the LLM connection and basic graph flow without SLIM

import asyncio
import os
import sys

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from dotenv import load_dotenv
load_dotenv()

async def test_llm():
    """Test basic LLM connectivity."""
    print("=" * 60)
    print(" AgentSwarm - Quick LLM Test")
    print("=" * 60)
    
    from common.llm import get_llm
    
    llm = get_llm()
    print(f"\n[OK] LLM initialized: {os.getenv('LLM_MODEL', 'default')}")
    
    # Test a simple prompt
    print("\nTesting LLM with a simple prompt...")
    response = await llm.ainvoke("Say 'Hello from AgentSwarm!' in exactly 5 words.")
    print(f"[OK] LLM Response: {response.content}")
    
    return True

async def test_supervisor_classification():
    """Test the supervisor's intent classification."""
    print("\n" + "=" * 60)
    print(" Testing Supervisor Intent Classification")
    print("=" * 60)
    
    from common.llm import get_llm
    from langchain_core.prompts import PromptTemplate
    
    llm = get_llm()
    
    test_queries = [
        ("How do I reset my password?", "faq"),
        ("Check order #12345", "customer_lookup"),
        ("Create a ticket for network issue", "ticket"),
        ("URGENT: System completely down!", "escalation"),
        ("Hello there!", "general"),
    ]
    
    prompt = PromptTemplate(
        template="""You are an AI supervisor for a customer support system. Analyze the customer's query and determine the primary intent.

Customer Query: {user_message}

Intent Classifications:
- faq: General questions, how-to guides, troubleshooting steps
- customer_lookup: Queries referencing order numbers, account status
- ticket: Need to create a support ticket
- escalation: Critical/urgent issues, repeated problems
- general: Greetings, unclear queries

Respond with ONLY ONE WORD - the intent classification.

Intent:""",
        input_variables=["user_message"]
    )
    
    chain = prompt | llm
    
    print("\nQuery                              | Expected | Got")
    print("-" * 60)
    
    correct = 0
    for query, expected in test_queries:
        response = await chain.ainvoke({"user_message": query})
        got = response.content.strip().lower()
        match = "[Y]" if got == expected else "[N]"
        if got == expected:
            correct += 1
        print(f"{query[:35]:35} | {expected:10} | {got} {match}")
    
    print(f"\nAccuracy: {correct}/{len(test_queries)} ({100*correct//len(test_queries)}%)")
    return correct >= 3  # Pass if at least 3/5 correct

async def test_knowledge_agent_standalone():
    """Test Knowledge Agent without A2A transport."""
    print("\n" + "=" * 60)
    print(" Testing Knowledge Agent (Standalone)")
    print("=" * 60)
    
    from agents.knowledge.agent import KnowledgeAgent
    
    agent = KnowledgeAgent()
    
    test_prompt = "How do I reset my password?"
    print(f"\nQuery: {test_prompt}")
    
    # Use the process method
    response = await agent.process(test_prompt)
    print(f"\n[OK] Response: {response[:200]}...")
    
    return True

async def main():
    """Run all tests."""
    print("\n" + "=" * 60)
    print(" AgentSwarm - Day 2 Quick Tests")
    print("=" * 60)
    
    tests_passed = 0
    total_tests = 3
    
    try:
        # Test 1: LLM
        if await test_llm():
            tests_passed += 1
            print("\n[PASS] Test 1: LLM connectivity")
        else:
            print("\n[FAIL] Test 1: LLM connectivity")
    except Exception as e:
        print(f"\n[FAIL] Test 1: {e}")
    
    try:
        # Test 2: Supervisor
        if await test_supervisor_classification():
            tests_passed += 1
            print("\n[PASS] Test 2: Supervisor classification")
        else:
            print("\n[FAIL] Test 2: Supervisor classification")
    except Exception as e:
        print(f"\n[FAIL] Test 2: {e}")
    
    try:
        # Test 3: Knowledge Agent
        if await test_knowledge_agent_standalone():
            tests_passed += 1
            print("\n[PASS] Test 3: Knowledge Agent")
        else:
            print("\n[FAIL] Test 3: Knowledge Agent")
    except Exception as e:
        print(f"\n[FAIL] Test 3: {e}")
    
    print("\n" + "=" * 60)
    print(f" RESULTS: {tests_passed}/{total_tests} tests passed")
    print("=" * 60)
    
    if tests_passed == total_tests:
        print("\n[SUCCESS] All tests passed! Ready to proceed.")
    else:
        print("\n[WARNING] Some tests failed. Check errors above.")

if __name__ == "__main__":
    asyncio.run(main())
