#!/usr/bin/env python3
"""
Automated test runner for SQL Agent test questions.
Run this script to test the agent with predefined questions.
"""

import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from backend.core.agent import SchemaAwareAgent
from backend.database.connection import get_database_engine

def main():
    # Test questions (subset from test_questions.md)
    test_questions = [
        "Show me all load balancers in us-east",
        "Display load balancer names along with their VIP member addresses",
        "List all VIP members with port 8080",
        "Show me VIPs that use port 443",
        "Find load balancers in US-EAST",  # Case insensitive test
        "How many load balancers are in each location?",
        "Show me all load balancers and their VIP addresses"
    ]
    
    # Initialize agent
    engine = get_database_engine()
    agent = SchemaAwareAgent(engine)
    
    print("🤖 SQL Agent Test Runner")
    print("=" * 50)
    
    passed = 0
    failed = 0
    
    for i, question in enumerate(test_questions, 1):
        print(f"\n{i}. Testing: {question}")
        print("-" * 40)
        
        try:
            result, sql_query = agent.run(question)
            
            if sql_query and result:
                print(f"✅ PASS")
                print(f"SQL: {sql_query}")
                print(f"Result: {result[:100]}..." if len(str(result)) > 100 else f"Result: {result}")
                passed += 1
            else:
                print(f"❌ FAIL: No SQL query generated")
                failed += 1
                
        except Exception as e:
            print(f"❌ FAIL: {str(e)}")
            failed += 1
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed} passed, {failed} failed")
    print(f"Success rate: {passed/(passed+failed)*100:.1f}%")

if __name__ == "__main__":
    main() 