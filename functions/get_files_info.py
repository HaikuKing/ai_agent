import os
from google.genai import types

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)

def get_files_info(working_directory, directory="."):
    try:
        abs_working = os.path.abspath(working_directory)
        abs_directory = os.path.abspath(os.path.join(abs_working, directory))

        if not (abs_directory.startswith(abs_working + os.sep) or abs_directory == abs_working):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        if not os.path.isdir(abs_directory):
            return f'Error: "{directory}" is not a directory'


        lines = []
        for file in os.listdir(abs_directory):
            file_entry = os.path.join(abs_directory, file)
            lines.append(f'- {file}: file_size={os.path.getsize(file_entry)} bytes, is_dir={os.path.isdir(file_entry)}')
        return "\n".join(lines)
    
    except Exception as e:
        return f"Error: {e}"