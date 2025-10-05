# Python
import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.write_file import schema_write_file
from functions.run_python_file import schema_run_python_file

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

# AI configuration
system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""
# Define available functions/tools
available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_write_file,
        schema_run_python_file,
    ]
)

if len(sys.argv) == 1:
    print("Usage: uv run main.py <query>")
    sys.exit(1)

# Checks for "--verbose" argument
is_verbose = False
if "--verbose" in sys.argv:
    is_verbose = True

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
# Handle function calls
    try:
        if response.function_calls:

            for call in response.function_calls:
                function_call_result = call_function(call, verbose=is_verbose)
                function_response = function_call_result.parts[0].function_response.response
                if not function_response:
                    raise Exception("No response from function.")
                elif function_response and is_verbose:

                    print(f'-> {function_response}')

        else:
# Fallback to printing the text if no function calls occurred
            print(response.text)
    except Exception as e:
        print(f"Error: {e}")

# Print metadata of response
    usage_metadata = dict(response.usage_metadata)
    if is_verbose:
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {usage_metadata['prompt_token_count']}")
        print(f"Response tokens: {usage_metadata['candidates_token_count']}")

# Function to call other Functions
def call_function(function_call_part, verbose=False):
    # Import functions
    from functions.get_files_info import get_files_info
    from functions.get_file_content import get_file_content
    from functions.write_file import write_file
    from functions.run_python_file import run_python_file
    
    # Set variables
    function_name = function_call_part.name
    function_args = function_call_part.args
    function_args_with_wd = {**function_args,
        "working_directory": "./calculator"
    }
    FUNCTIONS = {
        "get_files_info": get_files_info,
        "get_file_content": get_file_content,
        "write_file": write_file,
        "run_python_file": run_python_file,
    }
    

    try:
# Check for error
        if function_name not in FUNCTIONS:
            return types.Content(
                        role="tool",
                        parts=[
                            types.Part.from_function_response(
                                name=function_name,
                                response={"error": f"Unknown function: {function_name}"},
                            )
                        ],
                    )
        use_name = FUNCTIONS.get(function_name)
# Check if the "--verbose" arguement was provided
        if verbose:
            print(f"Calling function: {function_name}({function_args})")
        if not verbose:
            print(f" - Calling function: {function_name}")
# Call function
        function_result = use_name(**function_args_with_wd)

        return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": function_result},
            )
        ],
    )
    except Exception as e:
        print(f'Error: {e}')
# Run if directly called
if __name__ == "__main__":
    main()
