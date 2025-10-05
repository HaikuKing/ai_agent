import os
from google.genai import types


schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Relative path to the file."
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="content to write to the file."
            ),
        },
        required=["file_path", "content"],
    ),
)



def write_file(working_directory, file_path, content):
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))

    # Error Handling
    
    if not (abs_file_path.startswith(os.path.abspath(working_directory) + os.sep) or abs_file_path == os.path.abspath(working_directory)):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    
    try:
        os.makedirs(os.path.dirname(abs_file_path), exist_ok=True)
    
        with open(abs_file_path, "w") as file:
            file.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f'Error: {e}'