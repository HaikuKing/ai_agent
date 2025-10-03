import os

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