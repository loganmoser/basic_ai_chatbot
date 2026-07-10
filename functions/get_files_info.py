import os 

def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        working_abspath = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_abspath, directory))

        valid_target_dir = os.path.commonpath([working_abspath, target_dir]) == working_abspath

        if not valid_target_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        elif not os.path.isdir(target_dir):
            return f'Error: {directory} is not a directory'
        else:
            return f'Success: "{directory}" is within the working directory'
    except Exception as e:
        return f'Error: {e}'
