# Python
import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

# AI configuration
system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""
# Define available functions/tools
available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
    ]
)

if len(sys.argv) == 1:
    print("Usage: uv run main.py <query>")
    sys.exit(1)

def main():
    user_prompt = sys.argv[1]
    print("Hello from ai-agent!")
    
    # Prepares messages for the LLM
    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)])
    ]
    
    # Generate LLM response
    response = client.models.generate_content(
    model="gemini-2.0-flash-001",
    contents=messages,
    config=types.GenerateContentConfig(
        tools=[available_functions], system_instruction=system_prompt
    ),
)
    # Check for function calls
    try:
        if hasattr(response, "function_calls") and response.function_calls:
            # function_calls should be a list?
             for call in response.function_calls:
                function_name, function_parameters = call.name, call.args
            
                print(f"Calling function: {function_name}({function_parameters})")
        else:
            # Fallback to printing the text if no function calls occurred
            print(response.text)
    except Exception as e:
        print(f"Error: {e}")

    # Print metadata of response
    usage_metadata = dict(response.usage_metadata)
    if '--verbose' in sys.argv:
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {usage_metadata['prompt_token_count']}")
        print(f"Response tokens: {usage_metadata['candidates_token_count']}")


if __name__ == "__main__":
    main()
