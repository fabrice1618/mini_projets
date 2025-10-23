"""
Test direct de la fonction execute_tool_call
"""

from ai_assistant import execute_tool_call

# Test 1: Créer un projet
print("=== Test 1: Créer un projet ===")
result = execute_tool_call("creer_projet", {"titre": "Test Direct", "description": "Description test"})
print(f"Success: {result['success']}")
print(f"Message: {result['message']}")
print(f"Modified: {result['modified']}")
print()

# Test 2: Lister les projets
print("=== Test 2: Lister les projets ===")
result = execute_tool_call("lister_projets", {})
print(f"Success: {result['success']}")
print(f"Message: {result['message']}")
print(f"Data count: {len(result['data']) if result['data'] else 0}")
print()
