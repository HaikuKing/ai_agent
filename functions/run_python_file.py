import os
import subprocess
import sys

def run_python_file(working_directory, file_path, args=[]):
    
    abs_working = os.path.abspath(working_directory)
    abs_path = os.path.abspath(os.path.join(abs_working, file_path))

    if not (abs_path.startswith(abs_working + os.sep) or abs_path == abs_working):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.exists(abs_path):
        return f'Error: File "{file_path}" not found.'
    if not file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'
    try:
        arguments = [sys.executable, abs_path] + list(map(str, args))
        completed_process = subprocess.run(arguments, timeout=30, capture_output=True, cwd=abs_working, text=True)
        out, err, code = completed_process.stdout, completed_process.stderr, completed_process.returncode
        
        
        if not out and not err:
            return "No output produced."
        return format_result(out, err, code)
    except subprocess.TimeoutExpired as e:
        return f"Error: executing Python file: timed out after {e.timeout}s"
    except Exception as e:
        return f"Error: executing Python file: {e}"
    
def format_result(stdout, stderr, code=None, one_line=False):
    out = stdout.rstrip("\n")
    err = stderr.rstrip("\n")
    parts = [f"STDOUT: {out}", f"STDERR: {err}"]
    if code not in (None, 0):
        parts.append(f"Process exited with code {code}")
    sep = " " if one_line else "\n"
    return sep.join(parts)