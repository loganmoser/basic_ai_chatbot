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
        command = ["python", absolute_path]
        
        if args is not None:
            command.extend(args) # If user provided arguments, append them here

        process = subprocess.run(args = command, stdout = True, stderr = True, text=True, timeout=30)

        # Build output string
        output = ""
        if process.returncode != 0:
            output += f"Process exited with code {process.returncode} "
        if process.stdout is None and process.stderr is None:
            output += "No output produced "
        else:
            output += f"STDOUT: {process.stdout} STDERR: {process.stderr}"

        return output

    except Exception as e:
        return f"Error: executing Python file: {e}"

