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


