import os
import time
from dotenv import load_dotenv
from openai import OpenAI


# Load environment variables
load_dotenv()

# Read OpenRouter configuration
API_KEY = os.getenv("OPENROUTER_API_KEY")
MODEL = os.getenv("OPENROUTER_MODEL", "openrouter/free")

# Check API key
if not API_KEY:
    raise ValueError(
        "OPENROUTER_API_KEY not found. Check your .env file."
    )

# Create reusable OpenRouter client
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=API_KEY,
    default_headers={
        "X-Title": "AI Planning Agent"
    }
)
def get_ai_response(messages, temperature=0.3, max_tokens=1500):
    """
    Send messages to OpenRouter.
    Automatically retry if the response is empty
    or a temporary API error occurs.
    """

    max_attempts = 3
    last_error = None

    for attempt in range(1, max_attempts + 1):
        try:
            print(
                f"\nOpenRouter attempt {attempt}/{max_attempts}"
            )

            response = client.chat.completions.create(
                model=MODEL,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens
            )

            content = response.choices[0].message.content

            if content and content.strip():
                print("OpenRouter response received successfully.")
                return content.strip()

            last_error = "OpenRouter returned an empty response."

        except Exception as error:
            last_error = str(error)

        if attempt < max_attempts:
            wait_time = attempt * 2

            print(
                f"Attempt failed. Retrying in {wait_time} seconds..."
            )

            time.sleep(wait_time)

    raise RuntimeError(
        f"OpenRouter failed after {max_attempts} attempts. "
        f"Last error: {last_error}"
    )


    