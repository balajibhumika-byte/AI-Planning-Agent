import os
from dotenv import load_dotenv
from openai import OpenAI

# 1. Load environment variables from .env
load_dotenv()

# 2. Read API key and model
api_key = os.getenv("OPENROUTER_API_KEY")
model = os.getenv("OPENROUTER_MODEL", "openrouter/free")

# 3. Check API key
if not api_key:
    raise ValueError(
        "API key not found. Check your .env file."
    )

# 4. Connect to OpenRouter
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key
)

# 5. Send a test question
try:
    print("\nConnecting to OpenRouter...\n")

    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": "You are a helpful AI assistant."
            },
            {
                "role": "user",
                "content": "Explain what a planning agent is in two sentences."
            }
        ],
        max_tokens=150,
        temperature=0.3
    )

    # 6. Display AI response
    answer = response.choices[0].message.content

    print("CONNECTION SUCCESSFUL!")
    print("--------------------------------")
    print("AI MODEL:", response.model)
    print("--------------------------------")
    print("AI RESPONSE:")
    print(answer)
    print("--------------------------------")

except Exception as error:
    print("\nCONNECTION FAILED!")
    print("Error:", error)