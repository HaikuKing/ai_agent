import os
import sys
from dotenv import load_dotenv
from google import genai

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

if len(sys.argv) != 2:
    print("Usage: uv run main.py <query>")
    sys.exit(1)

def main():
    print("Hello from ai-agent!")
    # generate and print response
    response = client.models.generate_content(
    model="gemini-2.0-flash-001", contents=f"{sys.argv}"
)
    print(response.text)

    # print metadata of response
    usage_metadata = dict(response.usage_metadata)
    print(f"Prompt tokens: {usage_metadata["prompt_token_count"]}")
    print(f"Response tokens: {usage_metadata["candidates_token_count"]}")


if __name__ == "__main__":
    main()
