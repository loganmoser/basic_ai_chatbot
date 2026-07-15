import os

def write_file(working_directory: str, file_path: str, content: str) -> str:

    try:  
        abs_path = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(abs_path, file_path))


        if os.path.commonpath([abs_path, target_file]) != abs_path:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        if os.path.isdir(target_file):
            return f'Error: Cannot write to "{file_path}" as it is a directory'

        os.makedirs(os.path.dirname(target_file), exist_ok=True) # Create any missing directories for the file 

        with open(target_file, "w") as f:
            f.write(content)

    except Exception as e:
        return f'Error: {e}'

    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

schema_write_file = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "Writes given contents to a particular file",
        "parameters": {
            "required": ["file_path", "content"],
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "path to a given file in a directory to write to",
                },
                "content": {
                    "type": "string",
                    "description": "Content that is written to the given file"
                }
            },
        },
    },
}
