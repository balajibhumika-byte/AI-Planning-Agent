from core.llm_client import get_ai_response

print("Testing reusable AI connection...")

messages = [
    {
        "role": "system",
        "content": "You are a helpful AI assistant."
    },
    {
        "role": "user",
        "content": "What is task decomposition in Agentic AI?"
    }
]

try:
    answer = get_ai_response(messages)

    print("\nSUCCESS!")
    print("\nAI RESPONSE:")
    print(answer)

except Exception as error:
    print("\nFAILED!")
    print(error)