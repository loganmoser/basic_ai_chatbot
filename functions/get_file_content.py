import os

def get_file_content(working_directory: str, file_path: str) -> str:

    try:

        abs_dir = os.path.abspath(working_directory)
        target_file_path = os.path.normpath(os.path.join(abs_dir, file_path))

        if os.path.commonpath([abs_dir, target_file_path]) != abs_dir:
            return f'Error: Cannot list "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_file_path):
            return  f'Error: File not found or is not a regular files: "{file_path}"'
    
        MAX_CHARS = 10_000

        with open(target_file_path, "r") as f:
            file_contents = f.read(MAX_CHARS)

            if f.read(1):
                file_contents += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'

        return file_contents

    except Exception as e:
        return f"Error: {e}"


schema_get_file_content = {
    "type": "function",
    "function": {
        "name": "get_file_content",
        "description": "Reads up to 10,000 lines of a file and truncates it if it is longer",
        "parameters": {
            "required": ["file_path"],
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to the file to read, can be in the current directory on contain a file path to a sub directory",
                    },
            },
        },
    },
}
