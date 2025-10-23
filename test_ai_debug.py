"""
Script de debug pour tester l'intégration Ollama
"""

import ollama
from ai_tools import TOOLS
from ai_config import SYSTEM_MESSAGE, GENERATION_PARAMS

# Test avec un prompt simple
messages = [
    {
        "role": "system",
        "content": SYSTEM_MESSAGE
    },
    {
        "role": "user",
        "content": "Crée un projet 'Test Debug'"
    }
]

print("=== Test de l'appel Ollama avec tools ===\n")
print("Prompt:", messages[1]["content"])
print("\nEnvoi à Ollama...\n")

response = ollama.chat(
    model="llama3.2",
    messages=messages,
    tools=TOOLS,
    options={
        "temperature": GENERATION_PARAMS["temperature"],
        "top_p": GENERATION_PARAMS["top_p"],
        "top_k": GENERATION_PARAMS["top_k"],
    }
)

print("Réponse complète:")
print(response)
print("\n" + "="*50)

# Analyser la réponse
if response.get("message"):
    msg = response["message"]
    print("\nMessage content:", msg.get("content"))
    print("Tool calls:", msg.get("tool_calls"))

    if msg.get("tool_calls"):
        for tc in msg["tool_calls"]:
            print("\nTool call détails:")
            print("  - Nom:", tc["function"]["name"])
            print("  - Arguments:", tc["function"]["arguments"])
            print("  - Type arguments:", type(tc["function"]["arguments"]))
