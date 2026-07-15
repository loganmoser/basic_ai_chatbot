import os
import subprocess

def run_python_file(working_directory: str, file_path: str, args: list[str] | None = None) -> str:

    try:
        absolute_path = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(absolute_path, file_path))

        # Check if the file is in the directory, is a file, and is specifically a pyton file
        if os.path.commonpath([absolute_path, target_file]) != absolute_path:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_file):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if file_path.split('.')[1] != "py":
            return f'Error: "{file_path}" is not a Python file'

        # build subprocess for commands
        command = ["python", target_file]
        
        if args:
            command.extend(args) # If user provided arguments, append them here

        process = subprocess.run(args = command,
                                 cwd = absolute_path,
                                 capture_output=True,
                                 text=True,
                                 timeout=30
                                 )        

        # Build output string
        output: list[str] = []
        if process.returncode != 0:
            output.append(f"Process exited with code {process.returncode}")
        if not process.stdout and not result.stderr:
            output.append("No output produced")
        if process.stdout:
            output.append(f"STDOUT:\n{process.stdout}")
        if process.stderr:
            output.append(f"STDERR:\n{process.stderr}")
        
        return "\n".join(output)

    except Exception as e:
        return f"Error: executing Python file: {e}"


schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Run a given python file with optional parameters",
        "parameters": {
            "required": ["file_path"],
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to file in dierctory or subdirectory to the python file to run"
                },
                "args": {
                    "type": "array",
                    "items": {
                            "type": "str"
                        },
                    "description": "Optional arguments to run with the file",
                }
            }
        }
    }
}
